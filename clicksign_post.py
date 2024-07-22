from abstra.forms import *
from abstra.workflows import *
import requests
from datetime import date, datetime, timedelta
import os

# Get env variables
cs_token = os.getenv('CLICKSIGN_TOKEN')
cs_subdomain = 'app'
ceo_signer_key = os.getenv("CEO_SIGNER_KEY")
cfo_signer_key = os.getenv("CFO_SIGNER_KEY")
coo_signer_key = os.getenv("COO_SIGNER_KEY")

# Set initial variables 
current_date = date.today()
formatted_date = current_date.strftime("%d/%m/%Y")
deadline = (datetime.now() + timedelta(days=89)).strftime('%Y-%m-%dT%H:%M:%S-03:00') 
next = "Next"
headers = { 
    "Content-Type":"application/json",
    "Accept":"application/json"
}

# Get stage info
register_info = get_data('register_info')
address_info = get_data('address_info')
filepath = get_data('filepath')
base64_file = get_data('base64_file')
signatory_info = get_data('signatory_info')

# Create document object
document_data = {
    "document":{
        "path": f"/Partners Minutes/{filepath}",
        "content_base64":f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_file}",
        "deadline_at":deadline,
        "auto_close":True,
        "locale":"pt-BR",
        "sequence_enabled":True,
        "block_after_refusal": False
    }
}

# Upload document to Clicksign
upload_document_response = requests.post(
    f"https://{cs_subdomain}.clicksign.com/api/v1/documents?access_token={cs_token}",
    headers=headers,
    json=document_data)

print(upload_document_response.json())
document_key = upload_document_response.json()['document']['key']

# Create signer object
signer_data = {
    "signer":{
        "email":signatory_info['email'],
        "auths":[
            "email"
            ],
        "name": signatory_info['name'],
        "documentation": "",
        "birthday":"",
        "phone_number": "",
        "has_documentation": False,
        "selfie_enabled": False,
        "handwritten_enabled": False,
        "official_document_enabled": False, 
        "liveness_enabled": False,
        "facial_biometrics_enabled": False
    }
}

# Create signer in Clicksign
create_signer_response = requests.post(
    f'https://{cs_subdomain}.clicksign.com/api/v1/signers?access_token={cs_token}', 
    headers=headers, 
    json=signer_data)

print(create_signer_response)
signer_key = create_signer_response.json()['signer']['key']

all_signer_keys = [signer_key, ceo_signer_key, cfo_signer_key, coo_signer_key]

# Create function to call attribute signer for each signer
def add_signer(signer_key):
    body = {
        "list": {
            "document_key": document_key, 
            "signer_key": signer_key,
            "sign_as": "sign",
            "refusable": False,
            "group": 1,
            "message": "",
        }
    }
    attribute_signer_response = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/lists?access_token={cs_token}",
        headers=headers,
        json= body
    )

    notification_body = {
        "request_signature_key": attribute_signer_response.json()['list']['request_signature_key'],
        "message": f"Dear, \n please sign this Commercial Agreement Minute between Abstra and {register_info['name']}. \n\n If you have any questions, please contact sophia@abstra.app."
    }

    notification_response = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/notifications?access_token={cs_token}",
        headers=headers,
        json= notification_body
    )

    return attribute_signer_response, notification_response

for key in all_signer_keys:
    response = add_signer(key)
    print(response)