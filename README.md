# SI 673 Final Project

Borromean Digital needs you to build a cloud application that receives, processes, stores, and responds to data from an ESP32 camera/light-sensor device. Full requirements, due dates, and checkpoints are in [`final-project-spec.md`](final-project-spec.md).

## Connecting to Your Device

1. Plug your device into power using a USB-C cable. It should automatically connect to the university's Wi-Fi network.
2. Navigate to the instructor-provided [device registration portal](http://si673-camera-project-fall-2026.s3-website-us-east-1.amazonaws.com/).
3. Enter your assigned device ID (shown on the second line of the device's screen) and the endpoint(s) for your cloud application.
4. Register your device to begin forwarding data.

The instructor's infrastructure will forward data from your device to the endpoints you provide.

```
ESP32  ──►  Instructor forwarder  ──►  Your endpoint (Lambda or EC2)
  ▲                                           │
  └───────────── your JSON response ──────────┘
```

### What your endpoint receives

Every request is an HTTP `POST` with these headers:

| Header | Value |
| --- | --- |
| `X-Device-ID` | Your device ID |
| `X-Data-Type` | `light` or `image` |
| `Content-Type` | `application/json` (light) or `image/jpeg` (image) |

- **Light** body: `{"type": "light", "value": 1850}` — value ranges from 0 (dark) to 4095 (bright)
- **Image** body: the raw JPEG bytes

### What your endpoint should return

Return JSON to control the device. Every field is optional:

```json
{ "message": "Person detected!", "light": true, "buzzer": false }
```

- `message` — text shown on the OLED screen (keep it short)
- `light` — turn the LED on/off
- `buzzer` — turn the buzzer on/off

Respond within **10 seconds**, or the forwarder will give up on your request

## Project Option A: API Gateway + Lambda

1. Create a Lambda function (Python 3.12+) and paste in `lambda-starter/lambda_function.py`.
2. Create an **HTTP API** in API Gateway with a `POST /` route integrated with your Lambda.
3. Register the API's invoke URL in the portal.
4. Test in the Lambda console using `lambda-starter/test-event-light.json` as a test event.
5. View incoming data in **CloudWatch Logs** for your function.

## Project Option B: Flask on EC2

1. Launch an EC2 instance and allow inbound TCP on port **5000** in its security group
2. Copy `ec2-starter/` onto the instance, then:
   ```bash
   cd ec2-starter
   python3 -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
3. Register `http://<your-instance-public-ip>:5000/data` in the portal
4. Open `http://<your-instance-public-ip>:5000/` in a browser to see the latest reading and photo

## Tips

- **Never hardcode AWS credentials.** Your Lambda/EC2 should use the IAM role provided in your Vocareum account; `boto3` picks it up automatically.
- Devices send data every few seconds — think about *when* to store data, not just how.
- Run into a permissions wall? Talk to the instructional team.
