# Commercial Partnership Agreement Template

Use Abstra Workflows to build custom commercial agreement processes.

This is a functional template with the following steps:

- An onboarding form that collects signer data and company registration, address, and payment information. In the end, it automatically generates a commercial agreement with the provided data
- A Python script that sends the commercial agreement to the provided email addresses and requests signatures
- A Python script that notifies the people involved in a Slack channel called "partners"

![A credit onboarding workflow built in Abstra](https://github.com/user-attachments/assets/9cbcfdf7-9308-432b-a7d2-3079d814354a)
This template integrates with Slack and Clicksign. To make these integrations work, you must add your own API Key for these services.

API Key`s required:

- `CLICKSIGN_TOKEN`
- `CEO_SIGNER_KEY`
- `CFO_SIGNER_KEY`
- `COO_SIGNER_KEY`
- `SLACK_BOT_TOKEN`
  
If you're interested in customizing this template for your team in under 30 minutes, [book a customization session here.](https://meet.abstra.app/sophia-solo?url=github-template-credit-onboarding)
