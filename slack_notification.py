from abstra.forms import *
from abstra.workflows import *
import requests
import os, pathlib
from dotenv import load_dotenv

# Get env variables
slack_token = os.getenv('SLACK_BOT_TOKEN')

# Get thread info
register_info = get_data('register_info')
signatory_info = get_data('signatory_info')

# Send slack notification
slack_response = requests.post(
    "https://slack.com/api/chat.postMessage",
    json={
        "channel":"partners",
        "text": 
            f"The company {register_info['name']} filled out the form to generate the Commercial Agreement Minute. The document was sent to the signatories, including {signatory_info['email']}.",
        },
        headers={
            "Authorization":"Bearer "+slack_token,
            "Content-type": "application/json; charset=utf-8"
        })

print(slack_response.json())