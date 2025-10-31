from .authentication import router as auth_router
from .persons import router as persons_router
from .airlines import router as airlines_router
from .flights import router as flights_router
from .purchase_history import router as purchase_history_router
from .tickets import router as tickets_router
from .acc_recovery import router as recovery_route

__all__ = [
    'auth_router', 
    'persons_router', 
    'airlines_router', 
    'flights_router', 
    'purchase_history_router', 
    'tickets_router',
    'recovery_route'
]