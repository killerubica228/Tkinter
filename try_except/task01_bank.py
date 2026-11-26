# Задание 1. Банковский счёт
import math


class InsufficientFundsError(Exception):
    """Недостаточно средств на счёте."""


def parse_number(text, name):
    """Переводит строку в число. Нечисловой ввод -> ValueError с понятным текстом."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"{name}: «{text}» — это не число.") from None
    if not math.isfinite(value):          # отсекаем nan и inf
        raise ValueError(f"{name}: введите обычное конечное число.")
    return value


def withdraw(balance, amount):
    if amount < 0:
        raise ValueError("Сумма снятия не может быть отрицательной.")
    if amount > balance:
        raise InsufficientFundsError(
            f"Недостаточно средств: на счёте {balance:.2f}, а нужно {amount:.2f}.")
    return balance - amount


def main():
    try:
        balance = parse_number(input("Текущий баланс: "), "Баланс")
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        amount = parse_number(input("Сумма снятия: "), "Сумма")
        new_balance = withdraw(balance, amount)
    except InsufficientFundsError as e:
        print("Ошибка:", e)
    except ValueError as e:
        print("Ошибка ввода:", e)
    else:
        print(f"Снятие выполнено. Остаток на счёте: {new_balance:.2f}")
    finally:
        print("Работа с банкоматом завершена.")


if __name__ == "__main__":
    main()
