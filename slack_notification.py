from abstra.forms import *
from abstra.workflows import *
from abstra.connectors import get_access_token
import requests
import os
import dotenv

dotenv.load_dotenv()

# Get env variables
slack_token = get_access_token("slack").token

# Get thread info
register_info = get_data('register_info')
signatory_info = get_data('signatory_info')

# Send slack notification
slack_response = requests.post(
    "https://slack.com/api/chat.postMessage",
    json={
        "channel":os.getenv("SLACK_CHANNEL_NAME"),
        "text": 
            f"The company {register_info['name']} filled out the form to generate the Commercial Agreement Minute. The document was sent to the signatories, including {signatory_info['email']}.",
        },
        headers={
            "Authorization":"Bearer "+slack_token,
            "Content-type": "application/json; charset=utf-8"
        })

print(slack_response.json())