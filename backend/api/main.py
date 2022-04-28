import uvicorn

from api import create_app
from utils.db.models import migrate


if __name__ == '__main__':
    app = create_app()
    migrate()
    uvicorn.run(app=app, host="0.0.0.0", port=5000)
