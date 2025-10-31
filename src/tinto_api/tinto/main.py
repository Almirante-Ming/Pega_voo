from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tinto.utils import LoggingMiddleware, LOGGING_CONFIG
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)

from tinto.routes import (
    auth_router, 
    persons_router, 
    airlines_router, 
    flights_router, 
    purchase_history_router, 
    tickets_router,
    recovery_route
)

tinto = FastAPI(title="Tinto Booking API")

tinto.add_middleware(LoggingMiddleware)
tinto.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


tinto.include_router(auth_router)
tinto.include_router(recovery_route)
tinto.include_router(persons_router)
tinto.include_router(airlines_router)
tinto.include_router(flights_router)
tinto.include_router(purchase_history_router)
tinto.include_router(tickets_router)

@tinto.get('/', tags=['Health check'])
def health_response():
    return {'sucess': True, 'message':'working'}