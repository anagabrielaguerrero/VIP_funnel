from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st


gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

# ID of the folder containing the spreadsheet
folder_id = '1CeVVklJOxqcOBu3qnOFeZuTTmrKkaAGF'

# Create a new file inside the specified folder
file_metadata = {
    'title': 'Holamundo_streamlit.txt',  # Title of the file
    'parents': [{'id': folder_id}]  # Specify the folder where the file will be created
}

# Create the file
new_file = drive.CreateFile(file_metadata)
new_file.Upload()

print(f"File '{new_file['title']}' created successfully in folder with ID '{folder_id}'")


s