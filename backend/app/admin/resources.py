from fastapi_admin.resources import Model, Field
from fastapi_admin.widgets import displays, filters, inputs

from app.admin.models import OrderTortoise


class OrderResource(Model):
    """Ресурс для управления заказами"""
    label = "Заказы"
    model = OrderTortoise
    icon = "fas fa-shipping-fast"
    page_size = 20
    page_title = "Управление заказами"

    filters = [
        filters.Search(
            name="client_name",
            label="Имя клиента",
            search_mode="contains",
            placeholder="Поиск по имени"
        ),
        filters.Search(
            name="client_phone",
            label="Телефон",
            search_mode="contains",
            placeholder="Поиск по телефону"
        ),
        filters.Enum(
            enum_class=[
                ("new", "Новый"),
                ("in_progress", "В работе"),
                ("completed", "Завершен"),
                ("cancelled", "Отменен"),
            ],
            name="status",
            label="Статус"
        ),
        filters.Enum(
            enum_class=[
                ("uae_to_rf", "ОАЭ → РФ"),
                ("turkey_to_rf", "Турция → РФ"),
            ],
            name="route",
            label="Маршрут"
        ),
    ]

    fields = [
        Field(
            name="id",
            label="ID",
            display=displays.Display(),
            input_=inputs.DisplayOnly()
        ),
        Field(
            name="client_name",
            label="Имя клиента",
            display=displays.Display(),
            input_=inputs.Text()
        ),
        Field(
            name="client_phone",
            label="Телефон",
            display=displays.Display(),
            input_=inputs.Text()
        ),
        Field(
            name="client_email",
            label="Email",
            display=displays.Display(),
            input_=inputs.Email()
        ),
        Field(
            name="company_name",
            label="Компания",
            display=displays.Display(),
            input_=inputs.Text()
        ),
        Field(
            name="route",
            label="Маршрут",
            display=displays.Display(),
            input_=inputs.Select(
                enum_class=[
                    ("uae_to_rf", "🇦🇪 ОАЭ → РФ"),
                    ("turkey_to_rf", "🇹🇷 Турция → РФ"),
                ]
            )
        ),
        Field(
            name="cargo_type",
            label="Тип груза",
            display=displays.Display(),
            input_=inputs.Text()
        ),
        Field(
            name="cargo_weight",
            label="Вес (кг)",
            display=displays.Display(),
            input_=inputs.Number()
        ),
        Field(
            name="cargo_volume",
            label="Объем (м³)",
            display=displays.Display(),
            input_=inputs.Number()
        ),
        Field(
            name="description",
            label="Описание",
            display=displays.Display(),
            input_=inputs.TextArea()
        ),
        Field(
            name="pickup_address",
            label="Адрес забора",
            display=displays.Display(),
            input_=inputs.TextArea()
        ),
        Field(
            name="delivery_address",
            label="Адрес доставки",
            display=displays.Display(),
            input_=inputs.TextArea()
        ),
        Field(
            name="status",
            label="Статус",
            display=displays.Display(),
            input_=inputs.Select(
                enum_class=[
                    ("new", "Новый"),
                    ("in_progress", "В работе"),
                    ("completed", "Завершен"),
                    ("cancelled", "Отменен"),
                ]
            )
        ),
        Field(
            name="estimated_price",
            label="Ориентировочная цена",
            display=displays.Display(),
            input_=inputs.Number()
        ),
        Field(
            name="notes",
            label="Примечания",
            display=displays.Display(),
            input_=inputs.TextArea()
        ),
        Field(
            name="created_at",
            label="Создано",
            display=displays.DatetimeDisplay(),
            input_=inputs.DisplayOnly()
        ),
        Field(
            name="updated_at",
            label="Обновлено",
            display=displays.DatetimeDisplay(),
            input_=inputs.DisplayOnly()
        ),
    ]
