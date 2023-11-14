from abstra.forms import *
from abstra.workflows import *
import requests
from datetime import date, datetime, timedelta
import os

# Get env variables
cs_token = os.getenv("CLICKSIGN_TOKEN")
cs_subdomain = "app"  # if os.getenv("ABSTRA_ENVIRONMENT") != "production" else 'app'
manager_signer_key = os.getenv("MANAGER_SIGNER_KEY")
analyst_signer_key = os.getenv("ANALYST_SIGNER_KEY")
finance_signer_key = os.getenv("FINANCE_SIGNER_KEY")

# Set initial variables
current_date = date.today()
date = current_date.strftime("%d/%m/%Y")
deadline = (datetime.now() + timedelta(days=89)).strftime("%Y-%m-%dT%H:%M:%S-03:00")
next = "Next"
headers = {"Content-Type": "application/json", "Accept": "application/json"}

# Get stage info
stage = get_stage()
info_register = stage["info_register"]
info_address = stage["info_address"]
filepath = stage["filepath"]
base64_file = stage["base64_file"]
info_signer = stage["info_signer"]

# Create document object
document_data = {
    "document": {
        "path": f"/Minutas Parceiros/{filepath}",
        "content_base64": f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_file}",
        "deadline_at": deadline,
        "auto_close": True,
        "locale": "pt-BR",
        "sequence_enabled": True,
        "block_after_refusal": False,
    }
}

# Upload document to Clicksign
upload_document_response = requests.post(
    f"https://{cs_subdomain}.clicksign.com/api/v1/documents?access_token={cs_token}",
    headers=headers,
    json=document_data,
)

print(upload_document_response.json())
document_key = upload_document_response.json()["document"]["key"]


# Create signer object
signer_data = {
    "signer": {
        "email": info_signer["email"],
        "auths": ["email"],
        "name": info_signer["name"],
        "documentation": "",
        "birthday": "",
        "phone_number": "",
        "has_documentation": False,
        "selfie_enabled": False,
        "handwritten_enabled": False,
        "official_document_enabled": False,
        "liveness_enabled": False,
        "facial_biometrics_enabled": False,
    }
}

# Create signer in Clicksign
create_signer_response = requests.post(
    f"https://{cs_subdomain}.clicksign.com/api/v1/signers?access_token={cs_token}",
    headers=headers,
    json=signer_data,
)

print(create_signer_response)
signer_key = create_signer_response.json()["signer"]["key"]

all_signer_keys = [
    signer_key,
    manager_signer_key,
    analyst_signer_key,
    finance_signer_key,
]

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
        json=body,
    )

    notification_body = {
        "request_signature_key": attribute_signer_response.json()["list"][
            "request_signature_key"
        ],
        "message": f"Dearest, \n please sign this Commercial Agreement between our company and {info_register['trade_name']}. \n\n If you have any questions, reach us at sophia@abstra.app.",
    }

    notification_response = requests.post(
        f"https://{cs_subdomain}.clicksign.com/api/v1/notifications?access_token={cs_token}",
        headers=headers,
        json=notification_body,
    )

    return attribute_signer_response, notification_response


for key in all_signer_keys:
    response = add_signer(key)
    print(response)
