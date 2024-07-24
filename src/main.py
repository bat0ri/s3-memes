import uvicorn

from app.api.main import get_app
from settings import HOST, PORT


if __name__ == "__main__":
    app = get_app()

    uvicorn.run(app, host=HOST, port=PORT)
