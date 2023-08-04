from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass

import time

from .utils import git_commit_hash

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@dataclass
class IndexResponse:
    message: str
    git_commit_hash: str = git_commit_hash()
    server_time: str = "2021-01-01 00:00:00"
    version: str = "0.0.1"


@app.get("/")
def index() -> IndexResponse:
    return IndexResponse(
        message="This is awkward, nothing works yet. Except for this message.",
        server_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        git_commit_hash=git_commit_hash()
    )
