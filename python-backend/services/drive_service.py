import re
import requests
from typing import List, Dict

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
    try:
        folder_id = extract_folder_id(drive_link)
    except ValueError as e:
        raise ValueError(f'Could not extract folder ID from link: {str(e)}')

    api_url = f'https://www.googleapis.com/drive/v3/files'
    params = {
        'q': f"'{folder_id}' in parents and (mimeType contains 'image/jpeg' or mimeType contains 'image/png' or mimeType contains 'image/jpg')",
        'fields': 'files(id, name, webViewLink, webContentLink)',
        'key': 'YOUR_GOOGLE_API_KEY'
    }

    images = []

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        files = data.get('files', [])

        for file in files:
            file_id = file['id']
            file_name = file['name']

            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                images.append({
                    'fileName': file_name,
                    'fileId': file_id,
                    'driveLink': f"https://drive.google.com/file/d/{file_id}/view",
                    'directLink': f"https://drive.google.com/uc?export=view&id={file_id}"
                })

        return images

    except requests.exceptions.RequestException as e:
        raise Exception(f'Failed to fetch from Google Drive API: {str(e)}')
