from fastapi import FastAPI
import uvicorn

from src.controller import currencies_controller

app = FastAPI()

app.include_router(currencies_controller.router)

if __name__ == "__main__":
    uvicorn.run(app)