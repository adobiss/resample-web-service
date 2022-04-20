from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import shutil
import ffmpeg
import os
from pathlib import Path

# Utils
working_dir = Path().resolve()
app = FastAPI()

# Upload and resample audio file
@app.post("/resample/")
async def file_upload(inFile: UploadFile):
    try:
       with NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(inFile.file, tmp)
            tmp_path = Path(tmp.name)
                        
            # Create filename for resampled file
            base_filename = os.path.splitext(inFile.filename)[0]
            temp_filename = os.path.basename(tmp_path)
            
            # Resample file
            stream = ffmpeg.input(tmp_path)
            audio = stream.audio                       
            output_file_path = os.path.join(working_dir, temp_filename + ".mp3") # Downloads to project folder
            stream = ffmpeg.output(audio, output_file_path, **{'ar': '32000','acodec':'mp3'})
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            return {'file_name': base_filename, 'file_path': output_file_path, 'working_dir': working_dir}
    finally:
        tmp_path.unlink()

@app.get("/resample/", response_class=FileResponse)
async def client_download(file_path: str):
    return file_path
