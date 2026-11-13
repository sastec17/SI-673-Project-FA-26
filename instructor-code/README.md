# Instructor Code

Here's what runs behind the scenes. **You don't need to deploy or modify any of this** — it's here if you're curious how your device's data reaches you.

- `lambda-gateway-forwarder.py` — The Lambda behind the instructor API Gateway. It reads `X-Device-ID` and `X-Data-Type` from each device request, looks up your registered endpoints in DynamoDB, forwards the data to you, and relays your JSON response back to the device.
- `firmware/SI673_Cloud_Sensor/` — Arduino sketch running on your XIAO ESP32-S3 Sense. It captures photos and light readings, sends them to the forwarder, and applies your `message` / `light` / `buzzer` response.
- `firmware/OLED_Test/` — A small sketch we use to check that a device's screen works.
- `device-registration/` - The registration gateway is a static site served via S3. Form submission sends a request to an API gateway with a Lambda integration. The site's HTML and corresponding Lambda function are included here.
