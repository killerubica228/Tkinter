# Задание 6. Управление товарами
products = {
    "яблоко": {"price": 50.0, "qty": 100},
    "хлеб": {"price": 40.0, "qty": 30},
    "молоко": {"price": 85.5, "qty": 20},
}


class ProductNotFoundError(Exception):
    pass


class NotEnoughStockError(Exception):
    pass


def get_product(name):
    key = name.strip().lower()
    try:
        return key, products[key]
    except KeyError:
        raise ProductNotFoundError(f"Товар «{name.strip()}» не найден.") from None


def read_price(text):
    try:
        price = float(text.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"Цена «{text}» — не число.") from None
    if not price > 0 or price == float("inf"):
        raise ValueError("Цена должна быть положительным числом.")
    return price


def read_int(text, min_value, what="Количество"):
    try:
        value = int(text.strip())
    except ValueError:
        raise ValueError(f"{what} должно быть целым числом.") from None
    if value < min_value:
        raise ValueError(f"{what} не может быть меньше {min_value}.")
    return value


def show_products():
    name = input("Название товара (Enter — показать все): ")
    if not name.strip():
        for key, p in products.items():
            print(f"  {key}: цена {p['price']:.2f}, на складе {p['qty']}")
    else:
        key, p = get_product(name)
        print(f"  {key}: цена {p['price']:.2f}, на складе {p['qty']}")


def add_product():
    name = input("Название нового товара: ").strip().lower()
    if not name:
        raise ValueError("Название не может быть пустым.")
    if name in products:
        raise ValueError(f"Товар «{name}» уже есть, измените его количество.")
    price = read_price(input("Цена: "))
    qty = read_int(input("Количество: "), 0)
    products[name] = {"price": price, "qty": qty}
    print(f"Товар «{name}» добавлен.")


def change_quantity():
    key, p = get_product(input("Название товара: "))
    p["qty"] = read_int(input(f"Новое количество (сейчас {p['qty']}): "), 0)
    print(f"Количество товара «{key}» теперь {p['qty']}.")


def sell_product():
    key, p = get_product(input("Название товара: "))
    qty = read_int(input("Сколько продать: "), 1)
    if qty > p["qty"]:
        raise NotEnoughStockError(
            f"Недостаточно товара «{key}»: на складе {p['qty']}, запрошено {qty}.")
    p["qty"] -= qty
    print(f"Продано {qty} шт. на сумму {qty * p['price']:.2f}. Остаток: {p['qty']}.")


ACTIONS = {"1": show_products, "2": add_product, "3": change_quantity, "4": sell_product}


def main():
    while True:
        print("\n1 — Просмотр  2 — Добавить  3 — Изменить количество  4 — Продать  0 — Выход")
        choice = input("Выбор: ").strip()
        if choice == "0":
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Ошибка: выберите пункт меню от 0 до 4.")
            continue
        try:
            action()
        except ProductNotFoundError as e:
            print("Ошибка:", e)
        except NotEnoughStockError as e:
            print("Ошибка:", e)
        except ValueError as e:
            print("Ошибка ввода:", e)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        pass
    print("Работа завершена.")
