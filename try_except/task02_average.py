# Задание 2. Среднее значение списка
import math


def parse_numbers(line):
    parts = line.split()
    if not parts:
        raise ValueError("Ввод пуст: введите хотя бы одно число.")
    numbers = []
    for part in parts:
        try:
            value = float(part.replace(",", "."))
        except ValueError:
            raise ValueError(f"«{part}» — это не число.") from None
        if not math.isfinite(value):
            raise ValueError(f"«{part}» — недопустимое значение.")
        numbers.append(value)
    return numbers


def average(numbers):
    try:
        result = sum(numbers) / len(numbers)
    except ZeroDivisionError:             # пустой список
        raise ValueError("Невозможно вычислить среднее: список пуст.") from None
    if not math.isfinite(result):         # числа слишком большие, сумма «улетела» в inf
        raise OverflowError("Невозможно вычислить среднее: числа слишком велики.")
    return result


def main():
    try:
        numbers = parse_numbers(input("Введите числа через пробел: "))
        result = average(numbers)
    except ValueError as e:
        print("Ошибка ввода:", e)
    except OverflowError as e:
        print("Ошибка вычисления:", e)
    else:
        print(f"Список: {numbers}")
        print(f"Среднее значение: {result:.4g}")
    finally:
        print("Программа завершена.")


if __name__ == "__main__":
    main()
