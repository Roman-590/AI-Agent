from pydantic import BaseModel


class Settings(BaseModel):
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    stt_provider: str = "whisper"
    tts_provider: str = "openai"
    audio_storage_path: str = "./data/audio"
    transcripts_path: str = "./data/transcripts"


settings = Settings()
