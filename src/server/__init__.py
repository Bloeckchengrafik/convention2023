from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass

import time

from .routes import router
from .utils import git_commit_hash
from .datastore import init_database

init_database()

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router)


@dataclass
class IndexResponse:
    message: str
    git_commit_hash: str = git_commit_hash()
    server_time: str = "2021-01-01 00:00:00"
    version: str = "0.0.1"


@app.get("/")
def index() -> IndexResponse:
    return IndexResponse(
        message="It's the final countdown...",
        server_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        git_commit_hash=git_commit_hash()
    )
