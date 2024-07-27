import uvicorn

from app.api.main import get_app
from settings import HOST, PORT

app = get_app()
if __name__ == "__main__":

    uvicorn.run(app, host=HOST, port=PORT)
