from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.route import file_upload_router
from app.utils import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    Base.metadata.create_all(bind=engine)
    print("All tables created!")
    yield
    # shutdown
    engine.dispose()
    print("Database connection close!")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# redirect to docs
@app.get('/')
async def redirect_docs():
    return RedirectResponse(url="/docs")

app.include_router(file_upload_router)