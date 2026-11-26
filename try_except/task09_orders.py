# Задание 9. Мини-система заказов
CATALOG = {
    "Ноутбук": {"price": 55000, "stock": 5},
    "Мышь": {"price": 1500, "stock": 30},
    "Клавиатура": {"price": 3500, "stock": 20},
    "Монитор": {"price": 18000, "stock": 8},
    "Наушники": {"price": 4500, "stock": 15},
}
MAX_ORDER_SUM = 100_000


class ProductNotFoundError(Exception):
    pass


class InvalidQuantityError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class OrderLimitExceededError(Exception):
    pass


def show_catalog():
    print("\nТовары:")
    for i, (name, p) in enumerate(CATALOG.items(), start=1):
        print(f"  {i}. {name} — {p['price']} руб., на складе: {p['stock']}")


def choose_product(text):
    """Товар выбирается по номеру из списка или по названию."""
    text = text.strip()
    names = list(CATALOG)
    if text.isdigit():
        index = int(text)
        if 1 <= index <= len(names):
            return names[index - 1]
    else:
        for name in names:
            if name.casefold() == text.casefold():
                return name
    raise ProductNotFoundError(f"Товара «{text}» нет в списке.")


def read_quantity(text):
    try:
        qty = int(text.strip())
    except ValueError:
        raise InvalidQuantityError(f"Количество «{text.strip()}» — не целое число.") from None
    if qty <= 0:
        raise InvalidQuantityError("Количество должно быть больше нуля.")
    return qty


def make_order(name, qty):
    product = CATALOG[name]
    if qty > product["stock"]:
        raise OutOfStockError(
            f"На складе только {product['stock']} шт. товара «{name}», а нужно {qty}.")
    cost = qty * product["price"]
    if cost > MAX_ORDER_SUM:
        raise OrderLimitExceededError(
            f"Сумма заказа {cost} руб. превышает максимум {MAX_ORDER_SUM} руб.")
    product["stock"] -= qty
    return cost


def main():
    print("Для выхода введите q вместо товара.")
    while True:
        show_catalog()
        choice = input("\nТовар (номер или название): ")
        if choice.strip().lower() == "q":
            break
        try:
            name = choose_product(choice)
            qty = read_quantity(input("Количество: "))
            cost = make_order(name, qty)
        except ProductNotFoundError as e:
            print("Ошибка:", e)
        except InvalidQuantityError as e:
            print("Ошибка:", e)
        except OutOfStockError as e:
            print("Ошибка:", e)
        except OrderLimitExceededError as e:
            print("Ошибка:", e)
        else:
            print(f"Заказ оформлен: {name} × {qty} = {cost} руб.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nВыход.")
