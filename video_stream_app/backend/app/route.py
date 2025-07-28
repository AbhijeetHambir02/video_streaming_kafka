from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse, StreamingResponse
import os, datetime, uuid
from sqlalchemy.orm import Session

from app.config import FILE_UPLOAD
from app import models
from app import schemas
from app.utils import(
    get_db, 
    send_encrypted_video, 
    get_video_stream, 
    encrypt_file, 
    generate_key
)

file_upload_router = APIRouter(prefix="/video-streamer/v1", tags=["File Upload"])


@file_upload_router.post("/upload")
async def file_upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        os.makedirs(FILE_UPLOAD, exist_ok=True)
        file_path = os.path.join(FILE_UPLOAD, file.filename)
        topic = f"video-{uuid.uuid4().hex[:8]}"
        # save to local dir
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)


        # save to db
        uploaded_file = models.StoreFile(
            topic=topic,
            file_name=file.filename,
            file_path=file_path,
            uploaded_at=datetime.datetime.now(),
        )
        db.add(uploaded_file)
        db.commit()
        db.refresh(uploaded_file)

        file_info = db.query(models.StoreFile).filter(models.StoreFile.topic == topic).first()
        data = schemas.StoreFile.model_validate(file_info).model_dump(mode='json')
        
        await send_encrypted_video(topic=topic,file_path=data.get('file_path'))
        
        # encrypt file and save
        key = generate_key()
        encrypt_file(input_path=file_path, output_path=file_path, key=key)

        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@file_upload_router.get("/stream/{id}")
async def stream_video(id: int, db: Session = Depends(get_db)):
    video = db.query(models.StoreFile).filter(models.StoreFile.id == id).first()
    if not video:
        return JSONResponse(content={"error": "Video not found"}, status_code=404)

    return StreamingResponse(get_video_stream(topic=video.topic), media_type="video/mp4")




