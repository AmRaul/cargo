from tortoise import Model, fields
from fastapi_admin.models import AbstractAdmin


class Admin(AbstractAdmin):
    """Модель администратора"""
    last_login = fields.DatetimeField(description="Last Login", default=None, null=True)
    email = fields.CharField(max_length=200, default="")
    avatar = fields.CharField(max_length=200, default="")
    intro = fields.TextField(default="")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admin"


class OrderTortoise(Model):
    """Модель заказа для Tortoise ORM"""
    id = fields.IntField(pk=True)

    # Клиентская информация
    client_name = fields.CharField(max_length=255, description="Имя клиента")
    client_phone = fields.CharField(max_length=50, description="Телефон")
    client_email = fields.CharField(max_length=255, null=True, description="Email")
    company_name = fields.CharField(max_length=255, null=True, description="Компания")

    # Детали груза
    route = fields.CharField(max_length=50, description="Маршрут")
    cargo_type = fields.CharField(max_length=255, description="Тип груза")
    cargo_weight = fields.FloatField(null=True, description="Вес (кг)")
    cargo_volume = fields.FloatField(null=True, description="Объем (м³)")
    description = fields.TextField(null=True, description="Описание")

    # Адреса
    pickup_address = fields.TextField(null=True, description="Адрес забора")
    delivery_address = fields.TextField(null=True, description="Адрес доставки")

    # Статус
    status = fields.CharField(max_length=50, default="new", description="Статус")
    estimated_price = fields.FloatField(null=True, description="Ориентировочная цена")
    notes = fields.TextField(null=True, description="Примечания")

    # Временные метки
    created_at = fields.DatetimeField(auto_now_add=True, description="Создано")
    updated_at = fields.DatetimeField(auto_now=True, description="Обновлено")

    class Meta:
        table = "orders_admin"

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name}"
