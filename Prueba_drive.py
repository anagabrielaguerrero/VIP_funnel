from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import json


# Authenticate using the service account credentials
gauth = GoogleAuth()
gauth.service_account_email = 'drive-prueba@theta-actor-415016.iam.gserviceaccount.com'

gauth.credentials = ServiceAccountCredentials(service_account_email = st.secrets.credentials.client_email, scopes='',
                                               private_key_id=st.secrets.credentials.private_key_id,
                                                 client_id=st.secrets.credentials.client_id, 
                                                 user_agent=None, 
                                                 token_uri=st.secrets.credentials.token_uri, revoke_uri='https://accounts.google.com/o/oauth2/revoke')
# gauth.credentials = ServiceAccountCredentials.from_json(json.dumps(cred)) #, ['https://www.googleapis.com/auth/drive'])
gauth.Authorize()


# Initialize GoogleDrive instance
drive = GoogleDrive(gauth)

# Define folder metadata
folder_metadata = {
    'title': 'Your New Folder',
    'mimeType': 'application/vnd.google-apps.folder'
}

# Create the folder
folder = drive.CreateFile(folder_metadata)
folder.Upload()

print(f"Folder '{folder['title']}' created successfully (ID: {folder['id']})")

# Share the folder with specific email addresses
emails_to_share = ['gabriela.guerrero@undostres.com.mx', 'ernesto.servin@undostres.com.mx']

for email in emails_to_share:
    permission = {
        'type': 'user',
        'role': 'writer',  # Can be 'owner', 'writer', 'reader'
        'value': email
    }
    folder.InsertPermission(permission)

    print(f"Folder '{folder['title']}' shared with {email} successfully.")
