from abstra.forms import *
from abstra.workflows import *
from datetime import date, datetime, timedelta
from uuid import uuid4 as creates_uuid
from loguru import logger
from docusign_esign import ApiException, ApiClient, EnvelopesApi, Document, Signer, SignHere, Tabs, Recipients, EnvelopeDefinition
from abstra.connectors import get_access_token
import os
import dotenv
import requests
import base64

dotenv.load_dotenv()

# get .env docsign tockens
ACCESS_TOKEN = get_access_token("docusign").token
DOCUSIGN_AUTH_SERVER = os.getenv('DOCUSIGN_AUTH_SERVER')
API_BASE_PATH = os.getenv('API_BASE_PATH')
ACCOUNT_ID = os.getenv("DOCUSIGN_API_ID")
MANAGER_EMAIL = os.getenv("MANAGER_EMAIL")
MANAGER_NAME = os.getenv("MANAGER_NAME")

# Get stage info
register_info = get_data('register_info')
address_info = get_data('address_info')
filepath = get_data('filepath')
base64_file = get_data('base64_file')
signatory_info = get_data('signatory_info')


# creates envelope
# expects the manager and the new partner as signers
def make_envelope(signer_data):
    with open(filepath, "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode("ascii")

    # Create a document obj
    document = Document(
        document_base64=base64_file_content,
        name=filepath,
        file_extension="docx",
        document_id="1"
    )

    # Create models for the signers
    partner_signer = Signer(
        email=signer_data["partner_signer_email"],
        name=signer_data["partner_signer_name"],
        recipient_id=str(creates_uuid()),
        routing_order="1"
    )

    manager_signer = Signer(
        email=signer_data["manager_signer_email"],
        name=signer_data["manager_signer_name"],
        recipient_id=str(creates_uuid()),
        routing_order="2"
    )

    # Create the tabs for the signers
    sign_here_partner = SignHere(
        anchor_string="/sign_intern/",
        anchor_units="pixels",
        anchor_y_offset="10",
        anchor_x_offset="20"
    )
    sign_here_signer = SignHere(
        anchor_string="/sign_extern/",
        anchor_units="pixels",
        anchor_y_offset="10",
        anchor_x_offset="20"
    )

    # Add the tab models (including the sign here tab) to the signers
    partner_signer.tabs = Tabs(sign_here_tabs=[sign_here_partner])
    manager_signer.tabs = Tabs(sign_here_tabs=[sign_here_signer])

    envelope_definition = EnvelopeDefinition(
        email_subject=f"Please sign the following commercial agreement",
        documents=[document],
        recipients=Recipients(signers=[partner_signer, manager_signer]),
        status="sent"
    )

    return envelope_definition


# Create signer object
signer_data = {
    "partner_signer_email": signatory_info['email'],
    "partner_signer_name": signatory_info['name'],
    "manager_signer_email": MANAGER_EMAIL,
    "manager_signer_name": MANAGER_NAME
}

api_client = ApiClient()
api_client.host = API_BASE_PATH
api_client.set_default_header("Authorization", f"Bearer {ACCESS_TOKEN}")

envelope_definition = make_envelope(signer_data)
envelopes_api = EnvelopesApi(api_client)

try:
    results = envelopes_api.create_envelope(
        ACCOUNT_ID, envelope_definition=envelope_definition)
    logger.success(f"Sign Requested. Envelope ID: {results.envelope_id}. Status: {results.status}")
except ApiException as e:
    logger.error(f"Error regarding docsign EnvelopesApi use: {e}")