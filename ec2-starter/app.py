"""
SI 673 Final Project - EC2 (Flask) starter

Receives data forwarded from your ESP32 at POST /data and shows the
latest light reading and image at GET /.

Every request has two headers that tell you what arrived:

    X-Device-ID   your device's ID
    X-Data-Type   "light" or "image"

Light requests have a JSON body:  {"type": "light", "value": 0-4095}
Image requests have a raw JPEG body.

Whatever JSON you return is sent back to your device.

Run with:  python app.py
"""

import logging
from datetime import datetime

from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Latest data, kept in memory only. This is lost when the app restarts,
# which is why you'll need persistent storage (see TODOs below).
latest = {
    "device_id": None,
    "light_value": None,
    "light_time": None,
    "image_bytes": None,
    "image_time": None,
}


@app.route("/data", methods=["POST"])
def receive_data():
    device_id = request.headers.get("X-Device-ID")
    data_type = request.headers.get("X-Data-Type")
    # Milliseconds, so two images in the same second still look different.
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    latest["device_id"] = device_id

    if data_type == "light":
        reading = request.get_json(force=True)
        app.logger.info("Light reading from %s: %s", device_id, reading["value"])
        latest["light_value"] = reading["value"]
        latest["light_time"] = now

        # TODO: Process the reading with your own logic
        #       (e.g. compare against a threshold, detect changes over time).

        # TODO: Store readings in persistent storage (e.g. DynamoDB)
        #       under some condition you choose.

    elif data_type == "image":
        image_bytes = request.get_data()
        app.logger.info("Image from %s: %d bytes", device_id, len(image_bytes))
        latest["image_bytes"] = image_bytes
        latest["image_time"] = now

        # TODO: Process the image, e.g. with Amazon Rekognition:
        #       boto3.client("rekognition").detect_labels(Image={"Bytes": image_bytes})

        # TODO: Store images in persistent storage (e.g. S3) under some
        #       condition you choose (e.g. only images containing people).

    else:
        return jsonify(error=f"Unknown data type: {data_type}"), 400

    # TODO: Customize what your device shows/does based on your results.
    #       "message" appears on the OLED; "light" and "buzzer" are on/off.
    return jsonify(message="Data received!", light=False, buzzer=False)


@app.route("/")
def dashboard():
    return render_template("index.html", **latest)


@app.route("/latest.json")
def latest_json():
    # The dashboard polls this to update without reloading the page.
    # Image bytes aren't JSON; the page loads them from /latest.jpg.
    return jsonify(
        device_id=latest["device_id"],
        light_value=latest["light_value"],
        light_time=latest["light_time"],
        image_time=latest["image_time"],
    )


@app.route("/latest.jpg")
def latest_image():
    if latest["image_bytes"] is None:
        return "No image yet", 404
    return Response(latest["image_bytes"], mimetype="image/jpeg")


if __name__ == "__main__":
    # 0.0.0.0 makes the app reachable from outside the instance.
    app.run(host="0.0.0.0", port=5000)
