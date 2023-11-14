from abstra.forms import *
from abstra.workflows import *
from docxtpl import DocxTemplate
from datetime import date, datetime, timedelta
import base64
import os, pathlib
from dotenv import load_dotenv
from time import sleep

# Get env variables
load_dotenv()
PERSISTANT_FOLDER = pathlib.Path(os.getenv("ABSTRA_FILES_FOLDER", "/tmp"))
minutas_folder = PERSISTANT_FOLDER / "minutas"
minutas_folder.mkdir(parents=True, exist_ok=True)

# Set initial variables
current_date = date.today()
date = current_date.strftime("%d/%m/%Y")
deadline = (datetime.now() + timedelta(days=89)).strftime("%Y-%m-%dT%H:%M:%S-03:00")
next = "Next"
doc = DocxTemplate("Commercial Agreement.docx")

# Get stage
stage = get_stage()

# Get company info
info_register = (
    Page()
    .display_markdown(
        """
# Dados cadastrais
    """
    )
    .read("What is the company's corporate name?", key="corporate_name")
    .read("What is the company's trade name?", key="trade_name")
    .read("What is the company's ID number?", key="id")
    .read_email("What is the company's email", key="email")
    .run(next)
)

# Save company info to stage
stage["info_register"] = info_register

# Get company address info
info_address = (
    Page()
    .display_markdown(
        """
# Commercial address
    """
    )
    .read(
        "What is the company's commercial address?",
        placeholder="Avenue ABC, nº 123 - Neighbourhood",
        key="address",
    )
    .read_dropdown(
        "State",
        [
            "AL",
            "AK",
            "AZ",
            "AR",
            "CA",
            "CO",
            "CT",
            "DE",
            "FL",
            "GA",
            "HI",
            "ID",
            "IL",
            "IN",
            "IA",
            "KS",
            "KY",
            "LA",
            "ME",
            "MD",
            "MA",
            "MI",
            "MN",
            "MS",
            "MO",
            "MT",
            "NE",
            "NV",
            "NH",
            "NJ",
            "NM",
            "NY",
            "NC",
            "ND",
            "OH",
            "OK",
            "OR",
            "PA",
            "RI",
            "SC",
            "SD",
            "TN",
            "TX",
            "UT",
            "VT",
            "VA",
            "WA",
            "WV",
            "WI",
            "WY",
        ],
        key="state",
    )
    .read("City", key="city")
    .run(next)
)

# Add address info to stage
stage["info_address"] = info_address

# Get payment info
info_payment = (
    Page()
    .display_markdown(
        """
# Bank data
    """
    )
    .read(
        "Beneficiary Name",
        intial_value=info_register["corporate_name"],
        key="beneficiary",
    )
    .read("Bank", key="bank")
    .read("Agency", key="agency")
    .read("Account", key="account")
    .run(next)
)

# Save payment info to stage
stage["info_payment"] = info_payment

# Get signer data
info_signer = (
    Page()
    .display_markdown(
        """
# Signatory data
"""
    )
    .read(
        "What is the full name of the company's legal representative who will sign the Commercial Agreement",
        key="name",
    )
    .read_email("What is the signatory's email", key="email")
    .run(next)
)

# Save signer data to stage
stage["info_signer"] = info_signer

# Display progress bar while document is being created
for i in range(10):
    display_progress(i, 10, text="Generating agreement...")
    sleep(1)

# Create document from template
context = {
    "partner_corporatename": info_register["corporate_name"],
    "partner_tradename": info_register["trade_name"],
    "partner_id": info_register["id"],
    "partner_email": info_register["email"],
    "partner_address": info_address["address"],
    "partner_cep": info_address["cep"],
    "partner_state": info_address["state"],
    "partner_city": info_address["city"],
    "partner_beneficiary": info_payment["beneficiary"],
    "partner_bank": info_payment["bank"],
    "partner_agency": info_payment["agency"],
    "partner_account": info_payment["account"],
    "date": date,
}

doc.render(context)
filepath = minutas_folder / f"{info_register['trade_name']}.docx"

# Save as new file
doc.save(filepath)

# Convert document to base64
with filepath.open("rb") as docx_file:
    base64_encoded = base64.b64encode(docx_file.read()).decode("utf-8")
    stage["base64_file"] = base64_encoded


# Save document to stage
stage["filepath"] = str(filepath.name)

# Allow user to download generated file copy
Page().display("Commercial agreement generated! 🚀", size="large").display(
    f"The agreement will be automatically sent for your signature, you will receive it in the emails {info_register['email']} e {info_signer['email']}. Download a copy of the document here:",
    size="medium",
).display_file(filepath.open("rb")).run(next)
