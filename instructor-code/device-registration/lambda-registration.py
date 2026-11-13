import json
import os
from urllib.parse import urlparse

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("TABLE_NAME", "cam-registration"))


def response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def valid_endpoint(url):
    if not url:
        return True  # Blank means disabled

    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
        )
    except ValueError:
        return False


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body") or "{}")

        device_id = body.get("id")
        image_endpoint = body.get("imageEndpoint")
        light_endpoint = body.get("lightEndpoint")

        # Check input types
        if not isinstance(device_id, str):
            return response(400, {"error": "Device ID is required."})

        if not all(
            value is None or isinstance(value, str)
            for value in (image_endpoint, light_endpoint)
        ):
            return response(400, {"error": "Invalid endpoint value."})

        device_id = device_id.strip()
        image_endpoint = (image_endpoint or "").strip()
        light_endpoint = (light_endpoint or "").strip()

        if not device_id or len(device_id) > 100:
            return response(400, {"error": "Invalid device ID."})

        if not image_endpoint and not light_endpoint:
            return response(400, {"error": "Provide at least one endpoint."})

        for endpoint in (image_endpoint, light_endpoint):
            if not valid_endpoint(endpoint):
                return response(
                    400, {"error": "Endpoints must be valid HTTP or HTTPS URLs."}
                )

        # Create the replacement registration
        item = {"id": device_id}

        if image_endpoint:
            item["image_endpoint"] = image_endpoint

        if light_endpoint:
            item["light_endpoint"] = light_endpoint

        # Replaces the entire previous registration
        table.put_item(Item=item)

        return response(
            200,
            {
                "message": "Device registered successfully.",
                "id": device_id,
                "image_enabled": bool(image_endpoint),
                "light_enabled": bool(light_endpoint),
            },
        )

    except (ValueError, TypeError, json.JSONDecodeError):
        return response(400, {"error": "Invalid request body."})

    except Exception:
        print("Registration failed", flush=True)
        return response(500, {"error": "Unable to register device."})
