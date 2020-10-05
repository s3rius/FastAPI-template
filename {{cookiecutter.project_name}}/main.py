import uvicorn

from src.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.server:app", host="0.0.0.0", port=8000, log_level=settings.log_level
    )
