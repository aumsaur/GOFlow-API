from apps.auth import app
import ssl

from fastapi import FastAPI
# Generate a self-signed SSL/TLS certificate
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="./perm/cert.pem", keyfile="./perm/key.pem")

app = FastAPI()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl=context)
