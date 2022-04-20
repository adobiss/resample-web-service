import requests
import uvicorn
import os

# Utils
url = 'http://127.0.0.1:8000/resample/' # endpoint for both resampling and client download
audio_to_resample_path = r"C:\Users\AD\Desktop\You Tell Me.wav" # add local file path
 
def resample_and_download(url, audio_to_resample_path):
    """
    Execute two path operations: POST - to upload file, resample and save on server and 
    GET - resampled file client download 
    """
    # Upload audio, resample and save to working directory under temp file name (server download)
    file = {'inFile': open(audio_to_resample_path, 'rb')}
    response = requests.post(url=url, files=file)
    file = {'inFile': (open(audio_to_resample_path, 'rb')).close()}
    json_data = response.json()
    print(json_data)    
    
    # Resampled file download to working directory (client download) 
    download_file_path = json_data['resampled_server_file_path']
    resampled_file_name = json_data['original_file_name']
    
    working_dir = os.getcwd()
    
    client_download_file_path = resampled_file_name + '-resampled.mp3'
    client_download_file_path_full = working_dir + '\\' + client_download_file_path
    
    query_params = {'file_path': download_file_path} # to declare function parameters as query parameters
    
    download_response = requests.get(url=url, params=query_params)
    open(client_download_file_path, 'wb').write(download_response.content)
    
    # Delete temp file
    os.remove(download_file_path) 
    
    print('Audio resampled successfully: ' + client_download_file_path_full)

resample_and_download(url, audio_to_resample_path)