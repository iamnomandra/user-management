from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def mount_folder(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")