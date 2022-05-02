import uvicorn

from api import create_app
from utils.db.models import migrate


if __name__ == '__main__':
    migrate()
    app = create_app()
    uvicorn.run(app=app, host="0.0.0.0", port=5000)
