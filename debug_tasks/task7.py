# Задание 7. Авторизация пользователя
CORRECT_LOGIN = "admin"
CORRECT_PASSWORD = "Python123"
MAX_ATTEMPTS = 3

for attempt in range(1, MAX_ATTEMPTS + 1):
    login = input("Логин: ").strip()
    password = input("Пароль: ")

    if login == "" or password == "":
        print("Ошибка: логин и пароль не могут быть пустыми.")
    elif login == CORRECT_LOGIN and password == CORRECT_PASSWORD:
        print("Доступ разрешён")
        break
    else:
        print("Ошибка: неверный логин или пароль.")

    left = MAX_ATTEMPTS - attempt
    if left > 0:
        print(f"Осталось попыток: {left}\n")
else:
    # сработает, только если цикл прошёл все попытки без break
    print("Доступ заблокирован")
