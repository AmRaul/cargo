from fastapi import FastAPI
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from tortoise.contrib.fastapi import register_tortoise

from app.admin.models import Admin
from app.admin.resources import OrderResource


TORTOISE_ORM = {
    "connections": {"default": "sqlite://./admin.db"},
    "apps": {
        "models": {
            "models": ["app.admin.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def configure_admin(app: FastAPI):
    """Настройка панели администратора"""

    await admin_app.configure(
        logo_url="https://preview.tabler.io/static/logo-white.svg",
        template_folders=[],
        favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
        providers=[
            UsernamePasswordProvider(
                login_logo_url="https://preview.tabler.io/static/logo.svg",
                admin_model=Admin,
            )
        ],
        admin_path="/admin",
    )

    # Регистрация ресурсов
    admin_app.add_admin_resource(OrderResource)

    # Регистрация Tortoise ORM
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
    )

    app.mount("/admin", admin_app)

    return app
