# Задание 10. Собственные классы исключений (регистрация)
class InvalidAgeError(Exception):
    pass


class InvalidEmailError(Exception):
    pass


class WeakPasswordError(Exception):
    pass


class InvalidNameError(Exception):      # дополнительный класс для проверки имени
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
        raise InvalidAgeError("Возраст должен быть целым числом.") from None
    if not 14 <= age <= 100:
        raise InvalidAgeError("Возраст должен быть в диапазоне от 14 до 100 лет.")
    return age


def validate_email(email):
    email = email.strip()
    if "@" not in email or "." not in email:
        raise InvalidEmailError("Электронная почта должна содержать символы @ и точку.")
    return email


def validate_password(password):
    if len(password) < 8:
        raise WeakPasswordError("Пароль должен содержать не менее 8 символов.")
    return password


def register():
    data = {}
    while True:
        try:
            # если поле уже принято, повторно его не спрашиваем
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
        except InvalidAgeError as e:
            print("Ошибка возраста:", e)
        except InvalidEmailError as e:
            print("Ошибка почты:", e)
        except WeakPasswordError as e:
            print("Слабый пароль:", e)
        else:
            return data
        finally:
            pass    # здесь можно, например, закрывать ресурсы


if __name__ == "__main__":
    try:
        user = register()
        print(f"\nРегистрация успешна: {user['name']}, {user['age']} лет, {user['email']}")
    except (EOFError, KeyboardInterrupt):
        print("\nРегистрация прервана.")
