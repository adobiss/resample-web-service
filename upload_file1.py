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
@app.post("/files/")
async def file_upload(inFile: UploadFile):
    try:
       #suffix = Path(inFile.filename).suffix
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
            stream = ffmpeg.output(audio, output_file_path, **{'ar': '16000','acodec':'mp3'})
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            
            return {'file name': base_filename, 'file path': output_file_path, 'tmp path': tmp_path}
    #except BaseException as err:
        #return {f"Unexpected {err}, {type(err)=}"}
    
    finally:
        inFile.filename
        tmp_path.unlink()
#return {output_file_path}

@app.get("/files/", response_class=FileResponse)
async def main(file_path: str):
    return file_path
#os.remove(output_file_path)
