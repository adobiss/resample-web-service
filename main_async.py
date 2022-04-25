from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import shutil
import ffmpeg
#import time
import os
from pathlib import Path
from pydub.utils import mediainfo

# Utils
working_dir = Path().resolve()
app = FastAPI()

# Upload and resample audio file
@app.post("/resample/")
def file_upload(inFile: UploadFile):
    try:
        
       # Save uploaded file as temp file
       with NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(inFile.file, tmp)
            tmp_path = Path(tmp.name)
            original_file = inFile.filename

            temp_filename = os.path.basename(tmp_path) # temp name used just in case to help easily differentiate file saved on server from client download
                       
            # Resample file and save to working dir with temp file name
            stream = ffmpeg.input(tmp_path)
            audio = stream.audio                       
            output_file_path = os.path.join(working_dir, temp_filename + ".mp3") # Downloads to project folder
            stream = ffmpeg.output(audio, output_file_path, **{'ar': '32000','acodec': 'mp3', 'b:a': '320k'})
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            # Extract resampled audio sample rate and format
            audio_info = mediainfo(output_file_path)
            resampled_audio_sample_rate = int(int(audio_info['sample_rate']) / 1000)
            resampled_audio_format = audio_info['format_name']
            
            return {'original_file': original_file, 'resampled_server_file_path': output_file_path,
                    'resampled_audio_sample_rate': resampled_audio_sample_rate, 'resampled_audio_format': resampled_audio_format}                   
    finally:
        # Delete temp file
        tmp_path.unlink()
        print('Temp file deleted {}'.format(inFile.filename))

# Client download
@app.get("/resample/", response_class=FileResponse)
def client_download(file_path: str):
    print('Start processing download from server')
    return file_path # returns stream