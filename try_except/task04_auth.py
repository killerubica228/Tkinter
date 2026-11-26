# Задание 4. Система авторизации
USERS = {"admin": "qwerty123", "anna": "pass2024", "ivan": "secret"}
MAX_ATTEMPTS = 3


class EmptyFieldError(Exception):
    pass


class UnknownLoginError(Exception):
    pass


class WrongPasswordError(Exception):
    pass


def check_login(login, password):
    if not login or not password:
        raise EmptyFieldError("Логин и пароль не должны быть пустыми.")
    try:
        expected = USERS[login]
    except KeyError:
        raise UnknownLoginError(f"Пользователь «{login}» не найден.") from None
    if password != expected:
        raise WrongPasswordError("Неверный пароль.")


def main():
    print(f"Авторизация. У вас {MAX_ATTEMPTS} попытки.")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        login = input("Логин: ").strip()
        password = input("Пароль: ")
        try:
            check_login(login, password)
        except EmptyFieldError as e:
            print("Ошибка:", e)
        except UnknownLoginError as e:
            print("Ошибка:", e)
        except WrongPasswordError as e:
            print("Ошибка:", e)
        else:
            print(f"Добро пожаловать, {login}!")
            break
        left = MAX_ATTEMPTS - attempt
        if left:
            print(f"Осталось попыток: {left}\n")
    else:                                   # цикл закончился без break
        print("Вход заблокирован: превышено число попыток.")


if __name__ == "__main__":
    main()
