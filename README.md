# Commercial Partnership Agreement Template
## How it works:

This project includes a commercial partnership agreement generator process implemented with Abstra and Python scripts. The new partner's personal information, along with the company information, is collected, and a contract is automatically generated based on it.

Integrations: 
  - Docusign
  - Slack

To customize this template for your team and build a lot more, [book a demonstration here.](https://meet.abstra.app/sophia-solo?url=template-commercial-partnership-agreement)

![A commercial partnership agreement generator workflow built in Abstra](https://github.com/user-attachments/assets/9cbcfdf7-9308-432b-a7d2-3079d814354a)

## Initial Configuration:
To use this project, some initial configurations are necessary:
1. **Python Version**: Ensure Python version 3.9 or higher is installed on your system.
2. **Environment Variables**:

    The following environment variables are required for both local development and online deployment:
  
    - `SLACK_BOT_TOKEN`: Slack Tocken to notify the partners about the new partnership agreement on Slack
    - `DOCUSIGN_ACCESS_TOKEN`: DocuSign Acess Token used for sending the contract to sign
    - `DOCUSIGN_API_ID`: DocuSign API account ID used for sending the contract to sign
    - `DOCUSIGN_AUTH_SERVER`: DocuSign Authentication Key for sending the contract to sign 
    - `API_BASE_PATH`: Base path where the contract will be uploaded on DocuSign service
  
   In the scripts, we assume that the manager is the signer involved in the partner adimission process. Below are some informations regarding the manager. If another party is involved, please change the key name or add new ones as needed on the .env file:

   - `MANAGER_NAME`: Manager`s name
   - `MANAGER_EMAIL`: Manager`s email
  
    For local development, create a `.env` file at the root of the project and add the variables listed above (as in `.env.examples`). For online deployment, configure these variables in your [environment settings](https://docs.abstra.io/cloud/envvars). 

4. **Dependencies**: To install the necessary dependencies for this project, a `requirements.txt` file is provided. This file includes all the required libraries.

   Follow these steps to install the dependencies:

   1. Open your terminal and navigate to the project directory.
   2. Run the following command to install the dependencies from `requirements.txt`:
  
      ```sh
      pip install -r requirements.txt
      ```
5. **Commercial Partnership Agreement Template**: In the files, there is an agreement template called `Commercial Partnership Agreement.docx`. If you want to use your own agreement template, please replace ours with yours. Use the following tags in the document where you want specific information to be inserted:

    - {{partner_name}}, {{partner_ein}}, {{partner_email}}, {{partner_address}}, {{partner_zipcode}}, {{partner_state}}, {{partner_beneficiary}}, {{partner_bank}}, {{partner_account}}, {{date}}
   
## General Workflow:
To implement this system use the following scripts:

### Commercial Partnership Agreement Generation:
For collecting information about the new partner, along with the company, and with it create a commercial partnership agreement, use:
  - **generate_commercial_agreement.py**: Script to generate a form for collecting information and, based on that information, generate a partnership contract that is available for download at the end of the form.

### Commercial Partnership Agreement Signing:
For sending the contract to be signed by the parties involved, use:
  - **clicksign_post.py**: Script to send the contract to be signed by the parties involved using DocuSign API.

### Slack Notification:
  - **slack_notification.py**: Script to send a notification on Slack about the contract generation and pending signatures.

If you're interested in customizing this template for your team in under 30 minutes, [book a customization session here.](https://meet.abstra.app/sophia-solo?url=template-commercial-partnership-agreement)
