from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from .config import KUBERNETES_KEY, KUBERNETES_URL, PUBLIC_KEY_PATH
from .models import Kubernetes
from jwt import decode

kube: Kubernetes

@asynccontextmanager
async def init(app: FastAPI):
    global kube
    kube = Kubernetes(key=KUBERNETES_KEY, url=KUBERNETES_URL)
    yield

app = FastAPI(lifespan=init)


class Data(BaseModel):
    # user_id: int
    cmd: str

@app.post("/exec")
def execute_command(x_token: Annotated[str, Header()], data: Data):
    token = None
    try:
        token = decode(x_token, key=open(PUBLIC_KEY_PATH).read(), algorithms=['RS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if kube.execute_command(user_id=token["sub"], command=data.cmd):
        return {"result": "ok"}
    else:
        raise HTTPException(status_code=500, detail="Error")

@app.post("/create")
def create_accessbox(x_token: Annotated[str, Header()]):
    token = None
    try:
        token = decode(x_token, key=open(PUBLIC_KEY_PATH).read(), algorithms=['RS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    kube.create_accessbox(user_id=token["sub"])
    return {"status": "ok"}

@app.get("/logs")
def get_logs(x_token: Annotated[str, Header()]):
    token = None
    try:
        token = decode(x_token, key=open(PUBLIC_KEY_PATH).read(), algorithms=['RS256'])
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized")
    data = kube.get_logs(user_id=token["sub"])
    if data:
        return {"logs": data}
    else:
        raise HTTPException(status_code=500, detail="Error")


@app.get("/health")
def health():
    return {"status": "ok"}
