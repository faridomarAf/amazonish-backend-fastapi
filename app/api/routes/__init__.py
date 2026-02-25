from .health import router as health_router
from .db_health import router as db_health_router
from .auth import router as auth_router
from .users import router as users_router
from .catalog import router as catalog_router
from .orders import router as orders_router

__all__ = ["health_router", "db_health_router",
           "auth_router", "users_router", "catalog_router", "orders_router"]
