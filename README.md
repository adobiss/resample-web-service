Converts wave/ mp3 files to 32kHz mp3

# README #

### New in this version

- Simultaneous client requests are now supported
- Service will not convert files that are already in the required format
- Resampled files stored on server are deleted as a background task after client download
- Minor workflow improvements

Concurrency - currently implemented by declaring path operation functions with 'def'. In such case FastAPI runs each function in an external threadpool that is then awaited, instead of being called directly ([see FastAPI documentation] (https://fastapi.tiangolo.com/async/#very-technical-details)). Functionality tested by submitting two POST requests (file upload) with 5 second sleep timer activated to 'http://127.0.0.1:8000/resample/' via Postman and referencing server's 'print' messages.

### General info

**Python version: 3.8.1**

 - main.py (RESTful Web Service): Contains two path operations utilising the same endpoint (/resample/). POST - to upload local audio file (tested for .wav and .mp3), resample it and save temporary on 'server' (same dir as main.py). GET - returns resampled audio file from server as stream for client download. All files stored on server are deleted as part of the path operation functions.

 - test_main.py: Run POST and GET methods consecutively under a single function to upload local file for resampling and execute client download (to the same dir as test_main.py). Local file path is required.


### Setup Environment & Install Dependencies

1. extract project folder archive
2. cd project root folder
2. install virtual environment (below virtual environment instructions are untested and provided for reference):
	- 'pip install virtualenv'
	- 'virtualenv env'
3. activate virtual environment (below virtual environment instruction are untested and provided for reference):
	- '.\env\Scripts\activate'
4. pip install -r .\requirements.txta


### Run Test Script

1. cd project root folder
2. type 'uvicorn main:app' in command line to launch server manually (add '--reload' if required to make changes to main.py)
3a. run 'test_main.py --source-file YOUR_FILE_PATH' from shell. '--source-file YOUR_FILE_PATH' is optional. If missing, Python will use the file path specified in main.py
3b. add local file path to test_main.py
4b. run test_main.py


### Current functionality

The Web Service is built with DevOps framework in mind. As majority of the time was spent researching API frameworks, concurrency and parallelism as well as studying FastAPI documentation the goal was to build a basic Web Service that possesses full range of functionality and improve incrementally.

### Missing functionality

Proper test scripts, HTTP exception handling.

### Future improvements

Concurrency using 'async def' path operation functions. Deploy properly using Docker, accept multiple files from single client, run uvicorn server from Python file, workflow improvements.
