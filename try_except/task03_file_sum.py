# Задание 3. Загрузка данных из файла
import math


def sum_file(path):
    """Суммирует числа из файла. Возвращает (сумма, число строк, список ошибок)."""
    total, count, errors = 0.0, 0, []
    with open(path, "r", encoding="utf-8-sig") as f:
        for number, line in enumerate(f, start=1):
            text = line.strip()
            if not text:                      # пустые строки пропускаем
                continue
            try:
                value = float(text.replace(",", "."))
                if not math.isfinite(value):
                    raise ValueError
            except ValueError:
                errors.append(f"Строка {number}: «{text}» — не число.")
                continue
            total += value
            count += 1
    return total, count, errors


def main():
    path = input("Имя файла (например, numbers_ok.txt): ").strip()
    try:
        if not path:
            raise FileNotFoundError
        total, count, errors = sum_file(path)
    except FileNotFoundError:
        print(f"Ошибка: файл «{path}» не найден.")
    except PermissionError:
        print(f"Ошибка: нет доступа к файлу «{path}».")
    except IsADirectoryError:
        print(f"Ошибка: «{path}» — это папка, а не файл.")
    except UnicodeDecodeError:
        print("Ошибка: файл не является текстовым (не удалось прочитать кодировку).")
    except OSError as e:
        print(f"Ошибка при работе с файлом: {e}")
    else:
        for message in errors:
            print("Ошибка данных ->", message)
        print(f"Корректных чисел: {count}, сумма: {total:g}")
        if errors:
            print(f"Пропущено некорректных строк: {len(errors)}")
    finally:
        print("Обработка файла завершена.")


if __name__ == "__main__":
    main()
