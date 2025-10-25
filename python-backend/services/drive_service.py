import re
import os
import json
from typing import List, Dict
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ----------------------
# CONFIG
# ----------------------
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Load service account from environment variable
creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if not creds_json:
    raise Exception("Missing environment variable: GOOGLE_APPLICATION_CREDENTIALS_JSON")

creds_dict = json.loads(creds_json)
creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Initialize Google Drive API client
service = build('drive', 'v3', credentials=creds)

# ----------------------
# Helper Functions
# ----------------------
def extract_folder_id(drive_link: str) -> str:
    patterns = [
        r'folders/([a-zA-Z0-9-_]+)',
        r'id=([a-zA-Z0-9-_]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, drive_link)
        if match:
            return match.group(1)
    raise ValueError('Invalid Google Drive folder link')

def fetch_drive_images(drive_link: str) -> List[Dict[str, str]]:
    folder_id = extract_folder_id(drive_link)

    query = (
        f"'{folder_id}' in parents and "
        "(mimeType contains 'image/jpeg' or mimeType contains 'image/png' or mimeType contains 'image/jpg')"
    )

    try:
        results = service.files().list(
            q=query,
            fields="files(id, name, webViewLink, webContentLink)"
        ).execute()

        files = results.get('files', [])
        images = []

        for file in files:
            images.append({
                'fileName': file['name'],
                'fileId': file['id'],
                'driveLink': f"https://drive.google.com/file/d/{file['id']}/view",
                'directLink': f"https://drive.google.com/uc?export=view&id={file['id']}"
            })

        return images

    except Exception as e:
        print("Error fetching Drive images:", e)
        raise Exception(f"Failed to fetch from Google Drive API: {str(e)}")
