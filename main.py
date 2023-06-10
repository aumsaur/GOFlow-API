import uvicorn
from fastapi import FastAPI
from apps.core.config import settings
from apps.api.v1.api import api_router, authenticate_token
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(api_router)

app.middleware("http")(authenticate_token)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    return {"message": "Hello from server"}

if __name__ == '__main__':
    uvicorn.run("main:app",
                host="localhost",
                port=8000,
                reload=True,
                ssl_keyfile="./key.pem",
                ssl_certfile="./cert.pem"
                )
