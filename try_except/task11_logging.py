# Задание 11. Журналирование ошибок (регистрация из задания 10 + errors.log)
import logging
import os

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "errors.log")

# --- настройка журнала: дата, время, тип ошибки, описание ---
logger = logging.getLogger("registration")
logger.setLevel(logging.ERROR)
try:
    handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(handler)
except OSError as e:
    print(f"Внимание: журнал errors.log недоступен ({e}). Ошибки не будут записываться.")


def log_error(error):
    """Записывает тип и описание ошибки в errors.log."""
    logger.error("%s | %s", type(error).__name__, error)


class InvalidNameError(Exception):
    pass


class InvalidAgeError(Exception):
    pass


class InvalidEmailError(Exception):
    pass


class WeakPasswordError(Exception):
    pass


def validate_name(name):
    name = name.strip()
    if len(name) < 3:
        raise InvalidNameError("Имя должно содержать не менее 3 символов.")
    return name


def validate_age(text):
    try:
        age = int(text.strip())
    except ValueError:
        raise InvalidAgeError(f"Возраст «{text.strip()}» не является целым числом.") from None
    if not 14 <= age <= 100:
        raise InvalidAgeError(f"Возраст {age} вне диапазона от 14 до 100 лет.")
    return age


def validate_email(email):
    email = email.strip()
    if "@" not in email or "." not in email:
        raise InvalidEmailError(f"Адрес «{email}» должен содержать символы @ и точку.")
    return email


def validate_password(password):
    if len(password) < 8:
        raise WeakPasswordError("Пароль короче 8 символов.")
    return password


def register():
    data = {}
    while True:
        try:
            if "name" not in data:
                data["name"] = validate_name(input("Имя: "))
            if "age" not in data:
                data["age"] = validate_age(input("Возраст: "))
            if "email" not in data:
                data["email"] = validate_email(input("Электронная почта: "))
            if "password" not in data:
                data["password"] = validate_password(input("Пароль: "))
        except InvalidNameError as e:
            print("Ошибка имени:", e)
            log_error(e)
        except InvalidAgeError as e:
            print("Ошибка возраста:", e)
            log_error(e)
        except InvalidEmailError as e:
            print("Ошибка почты:", e)
            log_error(e)
        except WeakPasswordError as e:
            print("Слабый пароль:", e)
            log_error(e)
        else:
            return data


if __name__ == "__main__":
    try:
        user = register()
        print(f"\nРегистрация успешна: {user['name']}, {user['age']} лет, {user['email']}")
    except (EOFError, KeyboardInterrupt):
        print("\nРегистрация прервана.")
    print(f"Журнал ошибок: {LOG_PATH}")
