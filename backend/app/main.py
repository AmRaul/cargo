from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.core.config import settings
from app.core.database import engine

# Import API routers
from app.api.orders import router as orders_router
from app.api.suppliers import router as suppliers_router
from app.api.clients import router as clients_router
from app.api.rates import router as rates_router
from app.api.shipments import router as shipments_router
from app.api.expenses import router as expenses_router
from app.api.reports import router as reports_router

# Import SQLAdmin views
from app.admin.views import (
    SupplierAdmin,
    ClientAdmin,
    RateAdmin,
    ShipmentAdmin,
    ExpenseAdmin
)

# Note: Tables are now created via Alembic migrations
# Run: alembic upgrade head

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Trust proxy headers (must be first to work correctly behind nginx)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session middleware for SQLAdmin authentication
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)


# SQLAdmin Authentication Backend
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == "admin" and password == settings.ADMIN_PASSWORD:
            request.session.update({"token": "admin-authenticated"})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        return token == "admin-authenticated"


# Initialize SQLAdmin
authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
admin = Admin(
    app,
    engine,
    title="Панель управления грузоперевозками",
    authentication_backend=authentication_backend
)

# Register models with SQLAdmin
admin.add_view(SupplierAdmin)
admin.add_view(ClientAdmin)
admin.add_view(RateAdmin)
admin.add_view(ShipmentAdmin)
admin.add_view(ExpenseAdmin)


# API Routers
app.include_router(orders_router, prefix=settings.API_V1_STR)  # Keep old orders for compatibility
app.include_router(suppliers_router, prefix=settings.API_V1_STR)
app.include_router(clients_router, prefix=settings.API_V1_STR)
app.include_router(rates_router, prefix=settings.API_V1_STR)
app.include_router(shipments_router, prefix=settings.API_V1_STR)
app.include_router(expenses_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {
        "message": "Cargo Logistics Accounting API",
        "version": settings.VERSION,
        "docs": "/docs",
        "admin": "/admin"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
