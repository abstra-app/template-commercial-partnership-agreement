from abstra.forms import *
from abstra.workflows import *
import requests
import os

# Get env variables
slack_token = os.getenv("SLACK_BOT_TOKEN")

# Get stage info
stage = get_stage()
info_register = stage["info_register"]
info_signer = stage["info_signer"]

# Send slack notification
slack_response = requests.post(
    "https://slack.com/api/chat.postMessage",
    json={
        "channel": "partners",
        "text": f"The company {info_register['nome_fantasia']} has filled the form to generate a Commercial Agreement. The document was sent to be signed to {info_signer['email']}.",
    },
    headers={
        "Authorization": "Bearer " + slack_token,
        "Content-type": "application/json; charset=utf-8",
    },
)

print(slack_response.json())
