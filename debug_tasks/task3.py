# Задание 3. Тестирование калькулятора (доработанная версия)
#
# Что добавлено:
#   - деление на ноль не роняет программу, а выводит сообщение;
#   - для неизвестной операции выводится сообщение;
#   - буквы вместо чисел обрабатываются через try/except ValueError.
import math

try:
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))
    if not (math.isfinite(a) and math.isfinite(b)):
        raise ValueError
except ValueError:
    print("Ошибка: нужно вводить числа, а не буквы или другие символы.")
else:
    operation = input("Введите операцию (+, -, *, /): ").strip()
    if operation == "+":
        print(a + b)
    elif operation == "-":
        print(a - b)
    elif operation == "*":
        print(a * b)
    elif operation == "/":
        if b == 0:
            print("Ошибка: на ноль делить нельзя.")
        else:
            print(a / b)
    else:
        print(f"Ошибка: неизвестная операция «{operation}». Допустимы: +, -, *, /")
