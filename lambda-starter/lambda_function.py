"""
SI 673 Final Project - Lambda starter

Receives data forwarded from your ESP32 through API Gateway.
Every request has two headers that tell you what arrived:

    X-Device-ID   your device's ID
    X-Data-Type   "light" or "image"

Light requests have a JSON body:  {"type": "light", "value": 825}
Image requests have a raw JPEG body (API Gateway base64-encodes it)

Whatever JSON you return is sent back to your device
"""

import base64
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    headers = {
        key.lower(): value for key, value in (event.get("headers") or {}).items()
    }
    device_id = headers.get("x-device-id")
    data_type = headers.get("x-data-type")

    # Binary bodies (images) arrive base64-encoded
    raw_body = event.get("body") or ""
    if event.get("isBase64Encoded", False):
        body = base64.b64decode(raw_body)
    else:
        body = raw_body.encode("utf-8")

    if data_type == "light":
        reading = json.loads(body)
        logger.info("Light reading from %s: %s", device_id, reading["value"])

        # TODO: Process the reading with your own logic
        #       (e.g. compare against a threshold, detect changes over time)

        # TODO: Store readings in persistent storage (e.g. DynamoDB)
        #       under some condition you choose.

    elif data_type == "image":
        logger.info("Image from %s: %d bytes", device_id, len(body))

        # TODO: Process the image, e.g. with Amazon Rekognition:
        #       boto3.client("rekognition").detect_labels(Image={"Bytes": body})

        # TODO: Store images in persistent storage (e.g. S3) under some
        #       condition you choose (e.g. only images containing people)

    else:
        return respond(400, {"error": f"Unknown data type: {data_type}"})

    # TODO: Customize what your device shows/does based on your results.
    #       "message" appears on the OLED; "light" and "buzzer" are on/off

    return respond(
        200,
        {
            "message": "Data received!",
            "light": False,
            "buzzer": False,
        },
    )
