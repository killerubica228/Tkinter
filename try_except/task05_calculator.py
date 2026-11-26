# Задание 5. Калькулятор выражений
import math
import operator

OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul,
              "/": operator.truediv, "//": operator.floordiv,
              "%": operator.mod, "**": operator.pow}
MAX_DIGITS = 100          # результат больше 10**100 считаем слишком большим


class UnknownOperationError(Exception):
    pass


def parse_number(text):
    text = text.strip().replace(",", ".")
    try:
        return int(text)
    except ValueError:
        pass
    try:
        value = float(text)
    except ValueError:
        raise ValueError(f"«{text}» — неправильный формат числа.") from None
    if not math.isfinite(value):
        raise ValueError(f"«{text}» — недопустимое значение.")
    return value


def calculate(a, op, b):
    if op not in OPERATIONS:
        raise UnknownOperationError(
            f"Неизвестная операция «{op}». Допустимы: {' '.join(OPERATIONS)}")
    if op == "**" and b > 0 and abs(a) > 1:
        # заранее оцениваем размер результата, чтобы программа не «зависла»
        if b * math.log10(abs(a)) > MAX_DIGITS:
            raise OverflowError("слишком большой результат")
    result = OPERATIONS[op](a, b)
    if isinstance(result, complex):
        raise ValueError("результат не является вещественным числом")
    if abs(result) > 10 ** MAX_DIGITS:
        raise OverflowError("слишком большой результат")
    return result


def main():
    print("Калькулятор. Для выхода введите q вместо первого числа.")
    while True:
        first = input("\nПервое число: ")
        if first.strip().lower() == "q":
            break
        try:
            a = parse_number(first)
            op = input("Операция (+ - * / // % **): ").strip()
            b = parse_number(input("Второе число: "))
            result = calculate(a, op, b)
        except ValueError as e:
            print("Ошибка ввода:", e)
        except UnknownOperationError as e:
            print("Ошибка:", e)
        except ZeroDivisionError:
            print("Ошибка: деление на ноль невозможно.")
        except OverflowError:
            print("Ошибка: получился слишком большой результат.")
        else:
            print(f"Результат: {a} {op} {b} = {result}")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nВыход.")
