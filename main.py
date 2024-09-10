from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from repositories.videos import VideoRepository
from schemas.videos import Video

app = FastAPI()

engine = create_async_engine("sqlite+aiosqlite:///database.db")
async_session = AsyncSession(bind=engine)

video_repository = VideoRepository(db=async_session)

@app.get("/videos/", response_model=list[Video])
async def read_videos():
    videos = await video_repository.get_all_videos()
    return [Video.from_orm(video) for video in videos]

@app.get("/videos/{id}", response_model=Video)
async def read_video(id: int):
    video = await video_repository.get_video_by_id(id)
    if video:
        return Video.from_orm(video)
    raise HTTPException(status_code=404, detail="Video not found")

@app.post("/videos/", response_model=Video)
async def create_video(title: str, description: str):
    video = await video_repository.create_video(title, description)
    return Video.from_orm(video)

@app.put("/videos/{id}", response_model=Video)
async def update_video(id: int, title: str, description: str):
    video = await video_repository.update_video(id, title, description)
    if video:
        return Video.from_orm(video)
    raise HTTPException(status_code=404, detail="Video not found")

@app.delete("/videos/{id}")
async def delete_video(id: int):
    if await video_repository.delete_video(id):
        return {"message": "Video deleted"}
    raise HTTPException(status_code=404, detail="Video not found")