from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

ordinals = ["*"]


def setup(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ordinals,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
