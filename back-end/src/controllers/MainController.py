import os
import sys
from threading import Thread
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import  JSONResponse, StreamingResponse
import shutil

# Add the 'utils' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
# import modules from the 'utils' directory
import VideoCutter as vd 
import storage_manager as sm

UPLOAD_DIRECTORY = os.path.join("..","..","..","uploads")
VIDEOS_DIRECTORY=os.path.join("..","..","..","videos-cctv")

# Initialize camera
# mycam = vd.MyCam("http://204.106.237.68:88/mjpg/1/video.mjpg")
mycam = vd.MyCam(0)


app = FastAPI()
# Définir les origines autorisées
origins = [
        "http://localhost", 
        "http://localhost:4200", 
        "http://127.0.0.1:4200"
    ]   
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Autoriser uniquement les origines spécifiées
        allow_credentials=True,
        allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
        allow_headers=["*"],  # Autoriser tous les en-têtes
    )
    


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/motion-data")
async def detect(file_name: str=str(...)) :
    VIDEO_PATH=os.path.join(UPLOAD_DIRECTORY,file_name)
    if not os.path.isfile(VIDEO_PATH) :
        raise HTTPException(status_code=404, detail=f"Video not found {VIDEO_PATH}")
    return vd.detect_and_categorize_objects(VIDEO_PATH)

@app.get("/file-exists")
async def file_exists(file_name : str=str(...)):
    return {"exists":os.path.exists(os.path.join(UPLOAD_DIRECTORY,file_name))}
    
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse(content={"filename": file.filename}, status_code=200)

@app.get("/videos")
async def get_videos():
    return {"videos":sm.get_videos_details()}

@app.get("/video/{file_name}")
async def get_video(file_name:str ):
    file_path = os.path.join(VIDEOS_DIRECTORY, file_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File not found: {file_path}\n{file_name}")
    
    file_size = os.stat(file_path).st_size
    
    headers = {
        "content-type": "video/mp4",
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "content-range": f"bytes 0-{file_size - 1}/{file_size}",
    }

    return StreamingResponse(
        content=sm.generate_video_chunks(file_path),
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type="video/mp4",
        
    )

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(mycam.generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/start-recording")
async def detect_motion(file_name: str=str(...)) :
    Thread(target=mycam.detect_and_categorize_objects_3,daemon=True).start()
    
@app.get("/stop-recording")
async def stop_recording():
    mycam.stop_recording()
@app.get("/enable-disable")
async def start():
    mycam.enable_disable()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapiserver:app", host="127.0.0.1", port=8000, reload=True)
    
    
