# Автоматическая проверка заданий 2, 3 и 7: запускает программы с заранее
# подготовленным вводом и сравнивает ответ с ожидаемым.
import subprocess
import sys

DIR = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."


def run(script, inputs):
    result = subprocess.run([sys.executable, f"{DIR}/{script}"], input="\n".join(inputs) + "\n",
                            capture_output=True, text=True, encoding="utf-8")
    return result.stdout


def check(title, script, inputs, expected):
    out = run(script, inputs)
    ok = expected in out
    print(f"[{'OK' if ok else 'ОШИБКА'}] {title}: ввод {inputs} -> ищем «{expected}»")
    if not ok:
        print("    получено:", out)
    return ok


results = []
print("=== Задание 2 ===")
results += [check("10", "task2.py", ["10"], "Положительное число"),
            check("-5", "task2.py", ["-5"], "Отрицательное число"),
            check("0", "task2.py", ["0"], "Число равно нулю"),
            check("буквы", "task2.py", ["abc"], "Ошибка")]

print("\n=== Задание 3 (калькулятор) ===")
results += [check("сложение", "task3.py", ["2", "3", "+"], "5.0"),
            check("вычитание", "task3.py", ["10", "4", "-"], "6.0"),
            check("умножение", "task3.py", ["2.5", "4", "*"], "10.0"),
            check("деление", "task3.py", ["9", "3", "/"], "3.0"),
            check("деление на ноль", "task3.py", ["5", "0", "/"], "на ноль делить нельзя"),
            check("неизвестная операция", "task3.py", ["5", "2", "^"], "неизвестная операция"),
            check("буквы вместо чисел", "task3.py", ["abc"], "нужно вводить числа")]

print("\n=== Задание 7 (авторизация) ===")
results += [check("верный логин и пароль", "task7.py", ["admin", "Python123"], "Доступ разрешён"),
            check("неверный логин", "task7.py", ["root", "Python123"] * 3, "Доступ заблокирован"),
            check("неверный пароль", "task7.py", ["admin", "wrong"] * 3, "Доступ заблокирован"),
            check("пустой ввод", "task7.py", ["", ""] * 3, "Доступ заблокирован"),
            check("вход с третьей попытки", "task7.py",
                  ["admin", "1", "root", "x", "admin", "Python123"], "Доступ разрешён"),
            check("пароль с другим регистром", "task7.py", ["admin", "python123"] * 3,
                  "Доступ заблокирован")]

print(f"\nПройдено проверок: {sum(results)} из {len(results)}")
