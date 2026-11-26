# Задание 7. Регистрация пользователя (проверки через raise)
def validate_name(name):
    if len(name.strip()) < 3:
        raise ValueError("Имя должно содержать не менее 3 символов.")
    return name.strip()


def validate_age(text):
    try:
        age = int(text.strip())
    except ValueError:
        raise ValueError("Возраст должен быть целым числом.") from None
    if not 14 <= age <= 100:
        raise ValueError("Возраст должен быть в диапазоне от 14 до 100 лет.")
    return age


def validate_email(email):
    email = email.strip()
    if "@" not in email:
        raise ValueError("Электронная почта должна содержать символ @.")
    if "." not in email:
        raise ValueError("Электронная почта должна содержать точку.")
    return email


def validate_password(password):
    if len(password) < 8:
        raise ValueError("Пароль должен содержать не менее 8 символов.")
    return password


def ask(prompt, validator):
    """Спрашивает значение, пока оно не пройдёт проверку."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as e:
            print("Ошибка:", e)


def main():
    name = ask("Имя: ", validate_name)
    age = ask("Возраст: ", validate_age)
    email = ask("Электронная почта: ", validate_email)
    ask("Пароль: ", validate_password)
    print(f"\nРегистрация прошла успешно! {name}, {age} лет, {email}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nРегистрация прервана.")
