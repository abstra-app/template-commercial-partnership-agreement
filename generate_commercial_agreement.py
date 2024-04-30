from abstra.forms import *
from abstra.workflows import set_data
from abstra.common import get_persistent_dir
import requests
import pandas as pd
from zipfile import ZipFile
from docxtpl import DocxTemplate
from datetime import date, datetime, timedelta
import json
import base64
import os, pathlib
from dotenv import load_dotenv
from time import sleep

# Get env variables
load_dotenv()
persist_dir = get_persistent_dir()
minutes_folder = persist_dir / "minutes"
minutes_folder.mkdir(parents=True, exist_ok=True)

# Set initial variables
current_date = date.today()
date = current_date.strftime("%d/%m/%Y")
deadline = (datetime.now() + timedelta(days=89)).strftime('%Y-%m-%dT%H:%M:%S-03:00') 
next = "Next"
doc = DocxTemplate("Commercial Partnership Agreement.docx")


# Get company info 
register_info = Page()\
    .display_markdown("""
# Registration data
    """)\
    .read("What is the company's name?", key = "name")\
    .read("What is the company's EIN?", key = "ein", mask = "0000000000")\
    .read_email("What is the company's email?", key = "email")\
    .run(next)

# Save company info to stage
set_data('register_info', register_info)

# Get company address info
address_info = Page()\
    .display_markdown("""
# Commercial address
    """)\
    .read("What is the company's commercial address?", placeholder = "ABC Avenue, No. 123 - Neighborhood", key = "address")\
    .read("Zip code?", placeholder = "90210", key = "zipcode")\
    .read_dropdown(
        "State",
        [
            'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL',
            'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT',
            'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
            'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
        ],
        key = "state"
    )\
    .run(next)

# Add address info to stage
set_data('address_info', address_info)

# Get payment info
payment_info = Page()\
    .display_markdown("""
# Bank data
    """)\
    .read("Beneficiary's name", initial_value = register_info['name'], key = "beneficiary")\
    .read("Bank name", key = "bank")\
    .read("Account", key = "account")\
    .run(next)

# Save payment info to stage
set_data("payment_info", payment_info)  

# Get signer data
signatory_info = Page() \
    .display_markdown("""
# Signatory data
""") \
    .read("What is the full name of the company's legal representative who will sign the Commercial Agreement?", key="name") \
    .read_email("What is the signatory's email?", key="email") \
    .run(next)

# Save signer data to stage
set_data('signatory_info', signatory_info)

# Display progress bar while document is being created
for i in range(10):
    display_progress(i, 10, text="Generating customized minute...")
    sleep(1)

# Create document from template
context = {
    "partner_name": register_info['name'],
    "partner_ein": register_info['ein'],
    "partner_email": register_info['email'],
    "partner_address": address_info['address'],
    "partner_zipcode": address_info['zipcode'],
    "partner_state": address_info['state'],
    "partner_beneficiary": payment_info['beneficiary'],
    "partner_bank": payment_info['bank'],
    "partner_account": payment_info['account'],
    "date": date,
    }

doc.render(context)
filepath = minutes_folder / f"{register_info['name']}.docx"

# Save as new file
doc.save(filepath)

# Convert document to base64
with filepath.open("rb") as docx_file:
    base64_encoded = base64.b64encode(docx_file.read()).decode('utf-8')
    set_data('base64_file', base64_encoded)

# Save document to stage
set_data('filepath', str(filepath.name))

# Allow user to download generated file copy
Page() \
    .display("Commercial agreement minute generated! 🚀", size='large') \
    .display(f"The minute will be sent for your signature automatically, you will receive it at the emails {register_info['email']} and {signatory_info['email']}. Download here a copy of the document:", size='medium') \
    .display_file(filepath.open('rb')) \
    .run(next)
