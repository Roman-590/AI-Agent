from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.voice import router as voice_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Voice AI Interviewer Service")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"] ,
        allow_headers=["*"],
    )

    app.include_router(voice_router, prefix="/api/voice", tags=["voice"])
    return app


app = create_app()
