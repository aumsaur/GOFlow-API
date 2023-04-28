import uvicorn
import time
from fastapi import FastAPI, Request

# from apps.api.v1.auth.service import router
from apps.core.config import settings
from apps.api.v1.api import api_router
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response
async def authenticate_token(request: Request, call_next):
    print(request.url.path.encode)
    protected_paths = ["/item/read", "/item/update", "/item/create",
                       "/item/fetch", "/user/edit", "/delete", "/fetch"]

    # Check if the request URL path starts with one of the protected prefixes
    if any(request.url.path.startswith(prefix) for prefix in protected_paths):
        # do not authenticate for these endpoints
        response = await call_next(request)
        response.headers["middleware"] = 'do not authenticate for these endpoints'
        return response

    # token = request.headers.get("Authorization")
    # if not token:
    #     raise HTTPException(
    #         status_code=401, detail="Authorization header missing")

    # try:
    #     decoded_token = verify_access_token(token)
    # except:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    response = await call_next(request)
    response.headers["middleware"] = 'authenticate for these endpoints'
    return response


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app",
                host="localhost",
                port=8000,
                reload=True,
                ssl_keyfile="./key.pem",
                ssl_certfile="./cert.pem"
                )
