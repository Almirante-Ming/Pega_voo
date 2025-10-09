from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import usuarios_router, voos_router, reservas_router, auth_router
from app.models import Base
from app.config.database import engine
from app.config.settings import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Task Fly API',
    description='API for flight reservation system',
    version='1.0.0',
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(voos_router)
app.include_router(reservas_router)

@app.get('/', tags=['Health Check'])
def read_root():
    return {
        'message': 'Task Fly API is working!',
        'version': '1.0.0',
        'status': 'healthy',
        'environment': settings.environment,
        'debug': settings.debug
    }