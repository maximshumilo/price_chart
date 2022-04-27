import uvicorn

from api import fastapi_app
from utils.db.models import migrate


if __name__ == '__main__':
    migrate()
    uvicorn.run(app=fastapi_app, host="0.0.0.0", port=5000)
