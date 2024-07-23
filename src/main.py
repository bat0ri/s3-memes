import uvicorn

from app.api.main import get_app


if __name__ == "__main__":
    app = get_app()

    uvicorn.run(app, host="0.0.0.0", port=8000)
