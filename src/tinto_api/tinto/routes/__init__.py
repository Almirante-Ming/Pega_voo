from .authentication import router as auth_router
from .persons import router as persons_router

__all__ = ['auth_router', 'persons_router']