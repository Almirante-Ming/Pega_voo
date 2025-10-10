from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tinto.routes import auth_router, persons_router
tinto = FastAPI(title="Tinto Booking API")

tinto.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tinto.include_router(auth_router)
tinto.include_router(persons_router)

@tinto.get('/', tags=['Health check'])
def health_response():
    return {'sucess': True, 'message':'working'}