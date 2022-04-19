from tempfile import NamedTemporaryFile
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import shutil
import ffmpeg
import os
from pathlib import Path

app = FastAPI()
output_file_path = r"C:\Users\AD\Desktop\You Tell Me-resampled.mp3"

@app.post("/files/")
def file_upload(inFile: UploadFile):
    try:
       suffix = Path(inFile.filename).suffix
       with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(inFile.file, tmp)
            tmp_path = Path(tmp.name)
            #global output_file_path
            #output_file_path = tmp_path + '-resampled.mp3'
            stream = ffmpeg.input(tmp_path)
            audio = stream.audio
            stream = ffmpeg.output(audio, output_file_path, **{'ar': '16000','acodec':'mp3'})
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
          
        #return {tmp_path, suffix}
    #except BaseException as err:
        #return {f"Unexpected {err}, {type(err)=}"}
    
    finally:
        #inFile.file.close()
        tmp_path.unlink()
    return {output_file_path}

@app.get("/files/", response_class=FileResponse)
async def main():
    return output_file_path
#os.remove(output_file_path)
