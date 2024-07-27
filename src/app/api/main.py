from fastapi import FastAPI

from app.api.endpoints.memes import router as memes_router

app = FastAPI()


app.include_router(memes_router)


def get_app() -> FastAPI:
    return app