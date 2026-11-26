# Задание 8. Обработка матрицы
matrix = [[1, 2, 3, 4],
          [5, 6, 7, 8],
          [9, 10, 11, 12]]


def print_matrix():
    print("\nМатрица:")
    for row in matrix:
        print("  " + " ".join(f"{x:>6}" for x in row))


def read_index(text, size, what):
    """Номер строки/столбца вводится с 1. Возвращает индекс с 0."""
    try:
        number = int(text.strip())
    except ValueError:
        raise ValueError(f"{what} должен быть целым числом, а не «{text.strip()}».") from None
    if not 1 <= number <= size:
        raise IndexError(f"{what} {number} вне матрицы (допустимо от 1 до {size}).")
    return number - 1


def read_value(text):
    text = text.strip().replace(",", ".")
    for convert in (int, float):
        try:
            return convert(text)
        except ValueError:
            pass
    raise TypeError(f"Новое значение «{text}» не является числом.")


def main():
    print("Для выхода введите q вместо номера строки.")
    while True:
        print_matrix()
        row_text = input("Номер строки: ")
        if row_text.strip().lower() == "q":
            break
        try:
            row = read_index(row_text, len(matrix), "Номер строки")
            col = read_index(input("Номер столбца: "), len(matrix[0]), "Номер столбца")
            value = read_value(input("Новое значение: "))
        except ValueError as e:
            print("Ошибка ввода:", e)
        except IndexError as e:
            print("Ошибка границ:", e)
        except TypeError as e:
            print("Ошибка типа:", e)
        else:
            matrix[row][col] = value
            print(f"Элемент [{row + 1}][{col + 1}] изменён на {value}.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nВыход.")
