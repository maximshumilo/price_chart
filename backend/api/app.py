from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.endpoints import trade_tool_router


def create_app() -> FastAPI:
    fastapi_app = FastAPI()
    fastapi_app.include_router(trade_tool_router)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_headers=["*"],
    )
    return fastapi_app
