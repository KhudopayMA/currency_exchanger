import logging
import logging.config

import uvicorn
from fastapi import FastAPI

from src.controller import currencies_controller, exchange_rates_controller
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

app.include_router(currencies_controller.router)
app.include_router(exchange_rates_controller.router)

if __name__ == "__main__":
    uvicorn.run(app)
