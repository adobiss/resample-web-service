import requests
import os

url = 'http://127.0.0.1:8000/files/'

# File upload and resampling
file = {'inFile': open(r"C:\Users\AD\Desktop\You Tell Me.mp3", 'rb')}
response = requests.post(url=url, files=file)
file = {'inFile': (open(r"C:\Users\AD\Desktop\You Tell Me.mp3", 'rb')).close()}
json_data = response.json()

print(json_data)

# Resampled file download
download_file_path = json_data['file path']
query_params = {'file_path': download_file_path}
download_response = requests.get(url=url, params=query_params)
open(download_file_path, 'wb').write(download_response.content)


# upload to temp or project folder
# download to temp/ project/ user-specified foler
