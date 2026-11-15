# SI 673 — Final Project Specification

Borromean Digital has recently acquired a collection of Internet of Things (IoT) devices equipped with cameras, light sensors, and small displays.

The hardware team has already programmed these devices to collect data and communicate over Wi-Fi. However, the devices currently lack the cloud infrastructure needed to process, store, and act on the information they collect.

Your job is to design and build a cloud-powered application that uses data collected by one of these devices.

Your application might analyze photographs, monitor environmental conditions, detect changes over time, or combine multiple sources of data to produce useful information.

Unlike previous assignments, this project is intentionally open-ended. You will propose an application, design its AWS architecture, implement the necessary cloud services, and demonstrate a working system.

## Requirements

Your completed application must:

- **Receive device data:** Configure either an EC2 instance or an API Gateway endpoint with an AWS Lambda function to receive data from your assigned ESP32.
- **Process data:** Perform a meaningful operation on incoming images, light measurements, or both.
  - We strongly encourage the use of Rekognition and/or Bedrock in this project!
- **Store data:** Use persistent storage for either light or image data under some condition (for example, only store images containing people).
- **Produce an output:** Generate a useful result, such as an OLED message, dashboard, alert, or stored record.
- **Document your architecture:** Create a diagram showing how data flows between your device and AWS services.
- **Demonstrate your application:** Provide evidence that your application works end to end.

You are welcome to use additional AWS services beyond these minimum requirements.

## Example Project Ideas

You may choose one of the following ideas or propose something entirely different:

- **Smart Security Monitor:** Analyze photographs to detect people or objects and generate alerts.
- **Smart Room Monitor:** Combine image analysis and light measurements to determine the status of a room.
- **Environmental Monitor:** Track light measurements over time and identify unusually bright or dark conditions.
- **IoT Data Dashboard:** Collect sensor measurements and display results on a webpage.
- **Automated Image Archive:** Store photographs, analyze their contents, and organize them using detected labels.

These examples are intended to help you get started, not limit your application design.

## Project Checkpoints

### Checkpoint 1: Establish Cloud Connectivity

> **In-class work:** Monday, November 16  
> **Due:** Monday, November 23 at 11:59 PM

Before developing your application, you'll establish a working connection between your ESP32 and AWS.

In this checkpoint, you must:

- Create an API Gateway endpoint connected to a Lambda function.
- Register your device through the instructor-provided portal.
- Verify that your Lambda function successfully receives data from your device.
- Return a basic acknowledgment from Lambda to your device.

**Deliverable:** Include screenshots showing your API Gateway configuration, successful Lambda execution (including received device data), and Cloudwatch logs. You must also include a selfie with your device to prove in-class participation.

### Checkpoint 2: Project Proposal

> **Due:** Monday, November 23 at 11:59 PM

Submit a short proposal describing your intended application.

Include:

- **Application overview:** What are you building? Describe its purpose in 2–3 sentences.
- **Device data:** Will you use images, light measurements, or both?
- **AWS services:** Which services will you use, and what role will each play?
- **Expected output:** What will your application produce?
- **Architecture diagram:** Show how your device and AWS services will communicate.

Your proposed architecture may evolve as you begin implementation.

### Checkpoint 3: Implementation and Demonstration

Implement your proposed application and demonstrate that it works.

Your written final submission should include:

- **Application overview:** Briefly describe what you built.
- **Architecture diagram:** Show your final AWS architecture and the flow of data.
- **Infrastructure screenshots:** Demonstrate your configured AWS resources.
- **Working demonstration:** Provide screenshots or other evidence of your application processing real device data and producing the expected output.
- **Technical explanation:** Explain how your AWS services work together.
- **Work log:** Summarize your implementation process, challenges, and troubleshooting.

Students are expected to demonstrate their working prototype in the last class session on **Monday, December 7**.

## Working with Your Device

Each student or group will receive an instructor-provided ESP32 device with the following capabilities:

- **Camera:** Captures photographs every 2 seconds and transmits them to your cloud application.
- **Light sensor:** Measures ambient light levels and transmits readings.
- **OLED display:** Displays short text messages returned by your application.

The devices are preprogrammed and configured to connect to the University of Michigan's Wi-Fi network.

You do not need to program the ESP32 or configure Wi-Fi. Your responsibility is to build the cloud infrastructure that receives and processes device data.

### Connecting to Your Device

1. Plug your device into power using a USB-C cable. It should automatically connect to the university's Wi-Fi network.
2. Navigate to the instructor-provided device registration portal.
3. Enter your assigned device ID and the endpoint(s) for your cloud application.
4. Register your device to begin forwarding data.

The instructor's infrastructure will forward data from your device to the endpoints you provide.

### Sending Data Back to Your Device

Your cloud application can send instructions back to the ESP32, allowing it to respond to the data it collects.

The device supports three types of output:

- **OLED display:** Display a short text message.
- **LED light:** Turn a light on or off.
- **Buzzer:** Turn a buzzer on or off.

Your application can control these outputs by returning a JSON response.

For example, after detecting a person in a photograph:

```json
{
  "message": "Person detected!",
  "light": true,
  "buzzer": true
}
```

Or, after detecting low ambient light:

```json
{
  "message": "Low light detected",
  "light": true,
  "buzzer": false
}
```

Each output can be controlled independently. Your application might display a status message, activate an alert, or combine multiple outputs based on the data it receives.

You are not required to use all three outputs. Choose whichever are appropriate for your application.

## Additional Considerations

### AI Usage

You may use AI to aid in the completion of this project, but we want its use to be thoughtful.

To encourage the intentional use of AI models, you must document the following in your final submission **if you opt to use it**:

1. Why did you reach for AI in this project?
2. How did you use AI in this project?
3. What challenges did you encounter while using AI with this project (for example, hallucinations or vague responses)? How did you navigate them?

> **Note:** You must be able to explain how your system works in your final demonstration—“because my agent said so” is not a sufficient answer.

### AWS Permissions

Your application will run in the Vocareum AWS environment. You must work within the permissions and resources available in your account.

> **Important:** Do not hardcode AWS credentials. If you don't have permission to use a tool, chat with the instructional team. We may be able to grant access.

### Troubleshooting

Use Lambda logs, API Gateway responses, and other AWS debugging tools to investigate problems.

Document significant challenges and how you resolved them in your work log.

### Creativity and Scope

You do not need to invent an entirely new application. You may implement one of the suggested projects or design your own.

We are primarily interested in your ability to design an appropriate cloud architecture, integrate AWS services, and demonstrate a working system.
