from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.orders import router as orders_router
from app.api.admin import router as admin_router

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутеры
app.include_router(orders_router, prefix=settings.API_V1_STR)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "Cargo Shipping API",
        "version": settings.VERSION,
        "docs": "/docs",
        "admin": "/admin"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
