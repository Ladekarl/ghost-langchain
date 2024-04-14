import os

from dotenv import load_dotenv
from fastapi import FastAPI, Body, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader
from langserve import add_routes
from app.chain import chain

load_dotenv()

FASTAPI_API_KEY = os.environ["FASTAPI_API_KEY"]

api_keys = [FASTAPI_API_KEY]

header_scheme = APIKeyHeader(name="x-key")


def api_key_auth(api_key: str = Depends(header_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, chain, path="/ghost-project", dependencies=[Depends(api_key_auth)])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
