"""
Скрипт для создания первого администратора

Запуск: python create_admin.py
"""

from getpass import getpass
from passlib.hash import bcrypt


def create_admin():
    print("=== Создание администратора ===\n")

    username = input("Введите имя пользователя: ")
    password = getpass("Введите пароль: ")
    password_confirm = getpass("Подтвердите пароль: ")

    if password != password_confirm:
        print("❌ Пароли не совпадают!")
        return

    # Хешируем пароль
    hashed_password = bcrypt.hash(password)

    print("\n✅ Администратор создан!")
    print(f"Username: {username}")
    print(f"Hashed Password: {hashed_password}")
    print("\n📝 Добавьте эти данные в базу данных вручную")
    print("SQL запрос:")
    print(f"""
INSERT INTO admin (username, password, created_at)
VALUES ('{username}', '{hashed_password}', NOW());
    """)


if __name__ == "__main__":
    create_admin()
