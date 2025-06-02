from fastapi import FastAPI
import uvicorn

from src.controller import currencies_controller, exchange_rates_controller
app = FastAPI()

app.include_router(currencies_controller.router)
app.include_router(exchange_rates_controller.router)

if __name__ == "__main__":
    uvicorn.run(app)
