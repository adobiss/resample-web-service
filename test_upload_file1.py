import requests
import uvicorn
import os

url = 'http://127.0.0.1:8000/resample/'
audio_to_resample_path = r"C:\Users\AD\Desktop\You Tell Me.wav" # add local file path

# File upload and resampling
file = {'inFile': open(audio_to_resample_path, 'rb')}
response = requests.post(url=url, files=file)
file = {'inFile': (open(audio_to_resample_path, 'rb')).close()}
json_data = response.json()

# Resampled file download to working directory
download_file_path = json_data['file_path']
resampled_file_name = json_data['file_name']

working_dir = json_data['working_dir']

client_download_file_path = resampled_file_name + '-resampled.mp3'
client_download_file_path_full = working_dir + '\\' + client_download_file_path

query_params = {'file_path': download_file_path}

download_response = requests.get(url=url, params=query_params)
open(client_download_file_path, 'wb').write(download_response.content)

# Delete temp file
os.remove(download_file_path) 

print('Audio resampled successfully: ' + client_download_file_path_full)