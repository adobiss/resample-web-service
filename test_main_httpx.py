import os
import httpx
import argparse

# Utils
url = 'http://127.0.0.1:8000/resample/' # endpoint for both resampling and client download
audio_to_resample_path_internal = r"C:\Users\AD\Desktop\You Tell Me.mp3" # add local file path here if not using command-line arguments (tested for .wav and .mp3)

parser = argparse.ArgumentParser(description='Resample audio')
parser.add_argument('--source-file', dest='audio_to_resample_path',
                    help='The path to the audio file (.wav or .mp3) that needs to be resampled to 32kHz mp3. '
                             'If none, will use the path provided in the Python file.')
args = parser.parse_args()

if args.audio_to_resample_path is None:
    audio_to_resample_path = audio_to_resample_path_internal
else:
    audio_to_resample_path = args.audio_to_resample_path

# Main function
def resample_and_download(url, audio_to_resample_path):
    """
    Execute two path operations: POST - to upload file, resample and save on server and 
    GET - resampled file client download 
    """
    # Upload audio, resample and save to working directory under temp file name (server download)
    file = {'inFile': open(audio_to_resample_path, 'rb')}
    response = httpx.post(url=url, files=file)
                          #, timeout=10)
    file = {'inFile': (open(audio_to_resample_path, 'rb')).close()}
    json_data = response.json()
    original_file = json_data['original_file']
    
    # Check resampled audio sample rate and format
    resampled_audio_sample_rate = json_data['resampled_audio_sample_rate']
    resampled_audio_format = json_data['resampled_audio_format']
    print(response, '\'{}\' successfully uploaded and resampled to {}kHz {}.'.format(original_file, resampled_audio_sample_rate, resampled_audio_format))    
    
    # Resampled file download to working directory (client download)
    # Obtain and construct file paths
    download_file_path = json_data['resampled_server_file_path']
    resampled_file_name = os.path.splitext(original_file)[0]
    
    working_dir = os.getcwd()
    
    client_download_file_path = resampled_file_name + '-resampled.mp3'
    client_download_file_path_full = working_dir + '\\' + client_download_file_path
    
    # To declare function parameters as query parameters
    query_params = {'file_path': download_file_path}
    
    download_response = httpx.get(url=url, params=query_params)
                                  #, timeout=10)
    
    # Overwrite client download if already exists to avoid error (a workaround until validations, erorr handling are implemented)
    if os.path.isfile(client_download_file_path):
        os.remove(client_download_file_path)
    open(client_download_file_path, 'wb').write(download_response.content)
    
    # Delete temp file
    os.remove(download_file_path) 
    
    print(download_response, 'Resampled \'{}\' successfully downloaded: {}.'.format(original_file, client_download_file_path_full))

# Run main function
resample_and_download(url, audio_to_resample_path)