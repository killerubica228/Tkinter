# Задание 12 (итоговое). Консольная библиотечная система
import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.json")


# ---------- собственные исключения ----------
class LibraryError(Exception):
    """Базовый класс всех ошибок библиотеки."""


class BookNotFoundError(LibraryError):
    pass


class BookAlreadyIssuedError(LibraryError):
    pass


class BookNotIssuedError(LibraryError):
    pass


class DataFileError(LibraryError):
    """Проблема с файлом данных (повреждён или недоступен)."""

    def __init__(self, message, corrupted=False):
        super().__init__(message)
        self.corrupted = corrupted


# ---------- логика библиотеки ----------
class Library:
    def __init__(self):
        self.books = []

    def _next_id(self):
        return max((b["id"] for b in self.books), default=0) + 1

    def add_book(self, title, author, year):
        if not title.strip() or not author.strip():
            raise ValueError("Название и автор не могут быть пустыми.")
        if not 1 <= year <= date.today().year:
            raise ValueError(f"Год должен быть от 1 до {date.today().year}.")
        book = {"id": self._next_id(), "title": title.strip(), "author": author.strip(),
                "year": year, "reader": None, "issued_date": None}
        self.books.append(book)
        return book

    def get(self, book_id):
        for book in self.books:
            if book["id"] == book_id:
                return book
        raise BookNotFoundError(f"Книга с номером {book_id} не найдена.")

    def search(self, query):
        q = query.strip().casefold()
        if not q:
            raise ValueError("Введите текст для поиска.")
        found = [b for b in self.books
                 if q in b["title"].casefold() or q in b["author"].casefold()]
        if not found:
            raise BookNotFoundError(f"По запросу «{query.strip()}» ничего не найдено.")
        return found

    def issue(self, book_id, reader):
        if not reader.strip():
            raise ValueError("Укажите имя читателя.")
        book = self.get(book_id)
        if book["reader"] is not None:
            raise BookAlreadyIssuedError(
                f"Книга «{book['title']}» уже выдана: {book['reader']} "
                f"({book['issued_date']}).")
        book["reader"] = reader.strip()
        book["issued_date"] = date.today().strftime("%d.%m.%Y")
        return book

    def give_back(self, book_id):
        book = self.get(book_id)
        if book["reader"] is None:
            raise BookNotIssuedError(f"Книга «{book['title']}» не была выдана.")
        book["reader"] = None
        book["issued_date"] = None
        return book

    def load_books(self, data):
        """Проверяет структуру прочитанных данных. Неверная структура -> DataFileError."""
        if not isinstance(data, dict) or not isinstance(data.get("books"), list):
            raise DataFileError("Неверная структура файла данных.", corrupted=True)
        books = []
        for item in data["books"]:
            ok = (isinstance(item, dict)
                  and isinstance(item.get("id"), int)
                  and isinstance(item.get("title"), str)
                  and isinstance(item.get("author"), str)
                  and isinstance(item.get("year"), int)
                  and isinstance(item.get("reader"), (str, type(None)))
                  and isinstance(item.get("issued_date"), (str, type(None))))
            if not ok:
                raise DataFileError("В файле данных есть некорректная запись о книге.",
                                    corrupted=True)
            books.append({k: item[k] for k in
                          ("id", "title", "author", "year", "reader", "issued_date")})
        self.books = books

    def add_demo_books(self):
        for t, a, y in [("Война и мир", "Лев Толстой", 1869),
                        ("Мастер и Маргарита", "Михаил Булгаков", 1967),
                        ("Преступление и наказание", "Фёдор Достоевский", 1866),
                        ("1984", "Джордж Оруэлл", 1949),
                        ("Маленький принц", "Антуан де Сент-Экзюпери", 1943)]:
            self.add_book(t, a, y)


# ---------- работа с файлом ----------
def load_library(path=DATA_FILE):
    library = Library()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        library.load_books(data)
    except FileNotFoundError:
        library.add_demo_books()
        print("Файл данных не найден: создана новая библиотека с демо-книгами.")
    except PermissionError:
        raise DataFileError(f"Нет доступа к файлу «{path}».") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise DataFileError("Файл данных повреждён (не удаётся прочитать).",
                            corrupted=True) from None
    except OSError as e:
        raise DataFileError(f"Ошибка чтения файла: {e}") from None
    else:
        print(f"Данные загружены. Книг в библиотеке: {len(library.books)}.")
    finally:
        print("Загрузка данных завершена.")
    return library


def save_library(library, path=DATA_FILE):
    """Сохраняет через временный файл, чтобы сбой не испортил старые данные."""
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump({"books": library.books}, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except PermissionError:
        raise DataFileError(f"Нет доступа для записи в «{path}».") from None
    except OSError as e:
        raise DataFileError(f"Не удалось сохранить данные: {e}") from None
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def autosave(library):
    try:
        save_library(library)
    except DataFileError as e:
        print("Предупреждение:", e, "Изменения есть только в памяти.")


# ---------- интерфейс ----------
def read_int(prompt):
    text = input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"«{text}» — это не целое число.") from None


def print_books(books):
    for b in books:
        status = ("в наличии" if b["reader"] is None
                  else f"выдана: {b['reader']} ({b['issued_date']})")
        print(f"  №{b['id']:<3} «{b['title']}» — {b['author']}, {b['year']} | {status}")


def menu_add(library):
    title = input("Название: ")
    author = input("Автор: ")
    book = library.add_book(title, author, read_int("Год издания: "))
    print(f"Книга добавлена под номером {book['id']}.")
    autosave(library)


def menu_search(library):
    print_books(library.search(input("Что искать (название или автор): ")))


def menu_issue(library):
    book_id = read_int("Номер книги: ")
    book = library.issue(book_id, input("Имя читателя: "))
    print(f"Книга «{book['title']}» выдана читателю {book['reader']}.")
    autosave(library)


def menu_return(library):
    book = library.give_back(read_int("Номер возвращаемой книги: "))
    print(f"Книга «{book['title']}» возвращена.")
    autosave(library)


def menu_save(library):
    save_library(library)
    print("Данные сохранены.")


def menu_show(library):
    print_books(library.books) if library.books else print("Библиотека пуста.")


MENU = {"1": menu_add, "2": menu_search, "3": menu_show,
        "4": menu_issue, "5": menu_return, "6": menu_save}


def start():
    """Загружает данные. При повреждении сохраняет копию файла и начинает с чистой."""
    try:
        return load_library()
    except DataFileError as e:
        print("Ошибка:", e)
        if e.corrupted:
            backup = DATA_FILE + ".broken"
            try:
                os.replace(DATA_FILE, backup)
                print(f"Повреждённый файл сохранён как «{os.path.basename(backup)}».")
            except OSError:
                print("Не удалось сохранить копию повреждённого файла.")
        print("Программа начнёт работу с пустой библиотекой.")
        return Library()


def main():
    library = start()
    try:
        while True:
            print("\n1 — Добавить книгу  2 — Найти  3 — Все книги  "
                  "4 — Выдать  5 — Вернуть  6 — Сохранить  0 — Выход")
            choice = input("Выбор: ").strip()
            if choice == "0":
                break
            action = MENU.get(choice)
            if action is None:
                print("Ошибка: выберите пункт меню от 0 до 6.")
                continue
            try:
                action(library)
            except BookNotFoundError as e:
                print("Не найдено:", e)
            except BookAlreadyIssuedError as e:
                print("Повторная выдача:", e)
            except BookNotIssuedError as e:
                print("Ошибка возврата:", e)
            except DataFileError as e:
                print("Ошибка файла:", e)
            except ValueError as e:
                print("Ошибка ввода:", e)
    except (EOFError, KeyboardInterrupt):
        print()
    finally:
        autosave(library)
        print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
