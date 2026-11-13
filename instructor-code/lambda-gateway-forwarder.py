import base64
import json
import logging
import os
import urllib.error
import urllib.request

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("ROUTES_TABLE"))


def respond(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    # 1. Read device information from headers
    headers = {
        key.lower(): value for key, value in (event.get("headers") or {}).items()
    }

    device_id = headers.get("x-device-id")
    data_type = headers.get("x-data-type")

    if not device_id:
        return respond(400, {"error": "Missing x-device-id header"})

    if data_type not in ("image", "light"):
        return respond(400, {"error": "X-Data-Type must be image or light"})

    # 2. Look up the registered device
    try:
        result = table.get_item(Key={"id": device_id})
        device = result.get("Item")
    except Exception:
        logger.exception("DynamoDB lookup failed")
        return respond(500, {"error": "Unable to look up device"})

    if not device:
        return respond(404, {"error": "Device not registered"})

    # 3. Select the registered destination
    destination = device.get(f"{data_type}_endpoint")

    if not destination:
        logger.info(
            "Forwarding disabled for device %s, type %s",
            device_id,
            data_type,
        )

        return respond(
            200,
            {
                "status": "skipped",
                "reason": f"{data_type} endpoint disabled",
            },
        )

    # Reject malformed registrations (typos, missing scheme) up front;
    # urllib raises ValueError on these, which would otherwise surface
    # to the device as a bare API Gateway 500.
    if not isinstance(destination, str) or not destination.startswith(
        ("http://", "https://")
    ):
        logger.warning(
            "Invalid %s endpoint for device %s: %r",
            data_type,
            device_id,
            destination,
        )

        return respond(
            400,
            {
                "error": f"Invalid {data_type} endpoint; "
                "must start with http:// or https://",
            },
        )

    # 4. Decode the incoming request body
    raw_body = event.get("body") or ""

    try:
        if event.get("isBase64Encoded", False):
            payload = base64.b64decode(raw_body)
        else:
            payload = raw_body.encode("utf-8")
    except (ValueError, TypeError):
        return respond(400, {"error": "Invalid request body"})

    # 5. Forward the payload
    try:
        request = urllib.request.Request(
            destination,
            data=payload,
            headers={
                "Content-Type": headers.get(
                    "content-type",
                    "application/octet-stream",
                ),
                "X-Device-ID": device_id,
                "X-Data-Type": data_type,
            },
            method="POST",
        )

        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as upstream:
            status = upstream.status
            response_body = upstream.read()

        logger.info(
            "Forwarded %s data for %s: HTTP %s",
            data_type,
            device_id,
            status,
        )

        # Relay student JSON response to ESP32
        try:
            student_response = json.loads(response_body.decode("utf-8"))

            if isinstance(student_response, dict):
                return respond(200, student_response)

        except (ValueError, UnicodeDecodeError):
            pass

        # Fallback when student response isn't JSON
        return respond(
            200,
            {
                "status": "forwarded",
                "upstream_status": status,
            },
        )

    except urllib.error.HTTPError as error:
        logger.warning(
            "Student endpoint returned HTTP %s",
            error.code,
        )

        return respond(
            502,
            {
                "error": "Student endpoint returned an error",
                "upstream_status": error.code,
            },
        )

    except ValueError:
        # Passed the scheme check but still unparseable (e.g. "https://").
        logger.warning(
            "Malformed %s endpoint for device %s: %r",
            data_type,
            device_id,
            destination,
        )

        return respond(
            400,
            {
                "error": f"Invalid {data_type} endpoint URL",
            },
        )

    except (
        urllib.error.URLError,
        TimeoutError,
        OSError,
    ):
        logger.exception("Forwarding request failed")

        return respond(502, {"error": "Unable to reach student endpoint"})
