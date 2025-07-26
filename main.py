import logging
import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.controller import currencies_controller, exchange_rates_controller
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

origins = [
    'http://localhost:8080',
    'http://0.0.0.0:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(currencies_controller.router)
app.include_router(exchange_rates_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
