"""
Библиотечная система (Python 3 + Tkinter + SQLite).

Запуск:  python library_app.py
Демо-аккаунты:
    admin     / admin123   (администратор: добавление, правка, удаление книг)
    librarian / lib123     (библиотекарь: поиск, выдача и возврат книг)
Данные хранятся в файле library.db рядом с программой.
"""
import hashlib
import os
import sqlite3
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "library.db")

# ---------- оформление ----------
BG = "#f4ecd8"
HEADER = "#5b3a29"
BTN = "#8b5e3c"
BTN_ACTIVE = "#a67550"
FONT = ("Georgia", 11)

ROLE_NAMES = {"admin": "администратор", "librarian": "библиотекарь"}
GENRES = ["Роман", "Поэзия", "Поэма", "Антиутопия", "Сказка", "Фэнтези",
          "Детектив", "Приключения", "Научная литература", "Другое"]

DEMO_BOOKS = [
    ("Война и мир", "Лев Толстой", 1869, "Роман", 5),
    ("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", 4),
    ("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман", 6),
    ("Евгений Онегин", "Александр Пушкин", 1833, "Поэзия", 3),
    ("Мёртвые души", "Николай Гоголь", 1842, "Поэма", 3),
    ("Отцы и дети", "Иван Тургенев", 1862, "Роман", 2),
    ("Герой нашего времени", "Михаил Лермонтов", 1840, "Роман", 4),
    ("1984", "Джордж Оруэлл", 1949, "Антиутопия", 5),
    ("Маленький принц", "Антуан де Сент-Экзюпери", 1943, "Сказка", 7),
    ("Сто лет одиночества", "Габриэль Гарсиа Маркес", 1967, "Роман", 2),
    ("Гарри Поттер и философский камень", "Джоан Роулинг", 1997, "Фэнтези", 6),
    ("Властелин колец", "Джон Р. Р. Толкин", 1954, "Фэнтези", 3),
    ("Шерлок Холмс", "Артур Конан Дойл", 1892, "Детектив", 4),
    ("Три мушкетёра", "Александр Дюма", 1844, "Приключения", 3),
]


def hash_password(password, salt=None):
    """Возвращает строку 'соль$хеш' (пароли не хранятся в открытом виде)."""
    salt = salt or os.urandom(8).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 50_000).hex()
    return f"{salt}${digest}"


# =====================================================================
#                              БАЗА ДАННЫХ
# =====================================================================
class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_tables()
        self._seed()

    def _create_tables(self):
        with self.conn:
            self.conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    genre TEXT NOT NULL,
                    total INTEGER NOT NULL CHECK (total >= 0),
                    available INTEGER NOT NULL CHECK (available >= 0)
                );
                CREATE TABLE IF NOT EXISTS loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL REFERENCES books(id),
                    reader TEXT NOT NULL,
                    issue_date TEXT NOT NULL,
                    return_date TEXT
                );
            """)

    def _seed(self):
        """Демонстрационные данные при первом запуске."""
        with self.conn:
            if not self.conn.execute("SELECT 1 FROM users").fetchone():
                self.conn.executemany(
                    "INSERT INTO users (login, password, role, full_name) VALUES (?,?,?,?)",
                    [("admin", hash_password("admin123"), "admin", "Администратор"),
                     ("librarian", hash_password("lib123"), "librarian", "Библиотекарь Анна")])
            if not self.conn.execute("SELECT 1 FROM books").fetchone():
                self.conn.executemany(
                    "INSERT INTO books (title, author, year, genre, total, available) "
                    "VALUES (?,?,?,?,?,?)",
                    [(t, a, y, g, n, n) for t, a, y, g, n in DEMO_BOOKS])

    # --- пользователи ---
    def check_user(self, login, password):
        row = self.conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()
        if row:
            salt = row["password"].split("$")[0]
            if hash_password(password, salt) == row["password"]:
                return row
        return None

    # --- книги ---
    def all_books(self):
        return self.conn.execute("SELECT * FROM books ORDER BY id").fetchall()

    def add_book(self, title, author, year, genre, total):
        with self.conn:
            self.conn.execute(
                "INSERT INTO books (title, author, year, genre, total, available) "
                "VALUES (?,?,?,?,?,?)", (title, author, year, genre, total, total))

    def update_book(self, book_id, title, author, year, genre, total):
        book = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        issued = book["total"] - book["available"]
        if total < issued:
            raise ValueError(f"Нельзя установить количество меньше числа выданных "
                             f"экземпляров ({issued}).")
        with self.conn:
            self.conn.execute(
                "UPDATE books SET title=?, author=?, year=?, genre=?, total=?, available=? "
                "WHERE id=?", (title, author, year, genre, total, total - issued, book_id))

    def delete_book(self, book_id):
        active = self.conn.execute(
            "SELECT COUNT(*) FROM loans WHERE book_id=? AND return_date IS NULL",
            (book_id,)).fetchone()[0]
        if active:
            raise ValueError("Книгу нельзя удалить: есть невозвращённые экземпляры.")
        with self.conn:
            self.conn.execute("DELETE FROM loans WHERE book_id = ?", (book_id,))
            self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))

    # --- выдача и возврат ---
    def issue_book(self, book_id, reader):
        with self.conn:
            book = self.conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            if book["available"] <= 0:
                raise ValueError("Нет доступных экземпляров этой книги.")
            self.conn.execute("UPDATE books SET available = available - 1 WHERE id = ?",
                              (book_id,))
            self.conn.execute(
                "INSERT INTO loans (book_id, reader, issue_date) VALUES (?,?,?)",
                (book_id, reader, date.today().strftime("%d.%m.%Y")))

    def return_book(self, loan_id):
        with self.conn:
            loan = self.conn.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
            if loan["return_date"] is not None:
                raise ValueError("Эта книга уже возвращена.")
            book = self.conn.execute("SELECT * FROM books WHERE id = ?",
                                     (loan["book_id"],)).fetchone()
            if book["available"] >= book["total"]:
                raise ValueError("Нельзя вернуть больше экземпляров, чем есть в библиотеке.")
            self.conn.execute("UPDATE books SET available = available + 1 WHERE id = ?",
                              (book["id"],))
            self.conn.execute("UPDATE loans SET return_date = ? WHERE id = ?",
                              (date.today().strftime("%d.%m.%Y"), loan_id))

    def loans(self, include_returned=False):
        sql = ("SELECT loans.*, books.title FROM loans JOIN books ON books.id = loans.book_id")
        if not include_returned:
            sql += " WHERE loans.return_date IS NULL"
        return self.conn.execute(sql + " ORDER BY loans.id DESC").fetchall()


# =====================================================================
#                          ВСПОМОГАТЕЛЬНОЕ
# =====================================================================
def make_tree(parent, columns):
    """columns: список (id, заголовок, ширина, выравнивание). Возвращает Treeview."""
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill="both", expand=True)
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings",
                        selectmode="browse")
    for cid, text, width, anchor in columns:
        tree.heading(cid, text=text)
        tree.column(cid, width=width, anchor=anchor, stretch=(cid in ("title", "author")))
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return tree


BOOK_COLUMNS = [("id", "№", 50, "center"), ("title", "Название", 260, "w"),
                ("author", "Автор", 190, "w"), ("year", "Год", 70, "center"),
                ("genre", "Жанр", 120, "w"), ("total", "Всего", 70, "center"),
                ("available", "Доступно", 80, "center")]


def fill_books(tree, books):
    tree.delete(*tree.get_children())
    for b in books:
        tree.insert("", "end", iid=str(b["id"]),
                    values=(b["id"], b["title"], b["author"], b["year"],
                            b["genre"], b["total"], b["available"]))


def selected_id(tree):
    sel = tree.selection()
    return int(sel[0]) if sel else None


def label(parent, text, **kw):
    kw.setdefault("bg", BG)
    kw.setdefault("font", FONT)
    return tk.Label(parent, text=text, **kw)


# =====================================================================
#                       ДИАЛОГ ДОБАВЛЕНИЯ / ПРАВКИ КНИГИ
# =====================================================================
class BookDialog(tk.Toplevel):
    def __init__(self, app, book=None, on_saved=None):
        super().__init__(app)
        self.app, self.book, self.on_saved = app, book, on_saved
        self.title("Редактирование книги" if book else "Добавление книги")
        self.configure(bg=BG, padx=20, pady=15)
        self.resizable(False, False)
        self.transient(app)

        self.v_title = tk.StringVar(value=book["title"] if book else "")
        self.v_author = tk.StringVar(value=book["author"] if book else "")
        self.v_year = tk.StringVar(value=book["year"] if book else "")
        self.v_genre = tk.StringVar(value=book["genre"] if book else "")
        self.v_total = tk.StringVar(value=book["total"] if book else "1")

        rows = [("Название книги *", ttk.Entry(self, textvariable=self.v_title, width=36)),
                ("Автор *", ttk.Entry(self, textvariable=self.v_author, width=36)),
                ("Год издания *", ttk.Entry(self, textvariable=self.v_year, width=36)),
                ("Жанр *", ttk.Combobox(self, textvariable=self.v_genre, values=GENRES, width=34)),
                ("Количество экземпляров *", ttk.Entry(self, textvariable=self.v_total, width=36))]
        for i, (text, widget) in enumerate(rows):
            label(self, text).grid(row=i, column=0, sticky="e", padx=5, pady=6)
            widget.grid(row=i, column=1, padx=5, pady=6)
        rows[0][1].focus()

        buttons = tk.Frame(self, bg=BG)
        buttons.grid(row=len(rows), column=0, columnspan=2, pady=(12, 0))
        ttk.Button(buttons, text="Сохранить", style="Brown.TButton",
                   command=self.save).pack(side="left", padx=6)
        ttk.Button(buttons, text="Отмена", style="Brown.TButton",
                   command=self.destroy).pack(side="left", padx=6)
        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.destroy())

        self.update_idletasks()
        x = app.winfo_x() + (app.winfo_width() - self.winfo_width()) // 2
        y = app.winfo_y() + (app.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        self.grab_set()          # модальное окно: второй копии не будет

    def save(self):
        title = self.v_title.get().strip()
        author = self.v_author.get().strip()
        genre = self.v_genre.get().strip()
        if not title:
            return messagebox.showerror("Ошибка", "Введите название книги.", parent=self)
        if not author:
            return messagebox.showerror("Ошибка", "Введите автора.", parent=self)
        if not genre:
            return messagebox.showerror("Ошибка", "Укажите жанр.", parent=self)
        try:
            year = int(self.v_year.get().strip())
            if not 1 <= year <= date.today().year:
                raise ValueError
        except ValueError:
            return messagebox.showerror(
                "Ошибка", f"Год издания — целое число от 1 до {date.today().year}.", parent=self)
        try:
            total = int(self.v_total.get().strip())
            if total < 0:
                raise ValueError
        except ValueError:
            return messagebox.showerror(
                "Ошибка", "Количество экземпляров — целое число не меньше нуля.", parent=self)
        try:
            if self.book:
                self.app.db.update_book(self.book["id"], title, author, year, genre, total)
            else:
                self.app.db.add_book(title, author, year, genre, total)
        except ValueError as e:
            return messagebox.showerror("Ошибка", str(e), parent=self)
        self.destroy()
        if self.on_saved:
            self.on_saved()


# =====================================================================
#                              РАЗДЕЛЫ ГЛАВНОГО ОКНА
# =====================================================================
class BooksView(tk.Frame):
    """Каталог книг. При searchable=True сверху есть панель поиска."""

    def __init__(self, parent, app, searchable):
        super().__init__(parent, bg=BG)
        self.app, self.searchable = app, searchable
        label(self, "Поиск книг" if searchable else "Каталог книг",
              font=("Georgia", 16, "bold")).pack(anchor="w", pady=(0, 8))

        if searchable:
            bar = tk.Frame(self, bg=BG)
            bar.pack(fill="x", pady=(0, 8))
            label(bar, "Искать:").pack(side="left")
            self.query = tk.StringVar()
            entry = ttk.Entry(bar, textvariable=self.query, width=30)
            entry.pack(side="left", padx=6)
            entry.bind("<Return>", lambda e: self.refresh(notify=True))
            self.entry = entry
            self.field = ttk.Combobox(bar, values=["Везде", "Название", "Автор", "Жанр"],
                                      state="readonly", width=10)
            self.field.current(0)
            self.field.pack(side="left", padx=6)
            ttk.Button(bar, text="Найти", style="Brown.TButton",
                       command=lambda: self.refresh(notify=True)).pack(side="left", padx=4)
            ttk.Button(bar, text="Сбросить", style="Brown.TButton",
                       command=self.reset).pack(side="left", padx=4)

        self.tree = make_tree(self, BOOK_COLUMNS)
        self.status = label(self, "", fg="#5b3a29")
        self.status.pack(anchor="w", pady=4)

        if app.user["role"] == "admin":
            bar = tk.Frame(self, bg=BG)
            bar.pack(fill="x")
            ttk.Button(bar, text="Редактировать", style="Brown.TButton",
                       command=self.edit).pack(side="left", padx=(0, 6))
            ttk.Button(bar, text="Удалить", style="Brown.TButton",
                       command=self.delete).pack(side="left")

    def reset(self):
        self.query.set("")
        self.field.current(0)
        self.refresh()

    def matches(self, book):
        q = self.query.get().strip().casefold()
        if not q:
            return True
        fields = {"Название": [book["title"]], "Автор": [book["author"]],
                  "Жанр": [book["genre"]],
                  "Везде": [book["title"], book["author"], book["genre"]]}[self.field.get()]
        return any(q in text.casefold() for text in fields)

    def refresh(self, notify=False):
        books = self.app.db.all_books()
        if self.searchable:
            found = [b for b in books if self.matches(b)]
            if not found and notify:
                messagebox.showinfo("Поиск", "По вашему запросу ничего не найдено.")
            self.status.config(text=f"Найдено записей: {len(found)} из {len(books)}")
            books = found
        else:
            self.status.config(text=f"Всего записей: {len(books)}")
        fill_books(self.tree, books)

    def on_show(self):
        self.refresh()
        if self.searchable:
            self.entry.focus()

    def edit(self):
        book_id = selected_id(self.tree)
        if book_id is None:
            return messagebox.showwarning("Редактирование", "Сначала выберите книгу в таблице.")
        book = next(b for b in self.app.db.all_books() if b["id"] == book_id)
        BookDialog(self.app, book, self.app.main.refresh_current)

    def delete(self):
        book_id = selected_id(self.tree)
        if book_id is None:
            return messagebox.showwarning("Удаление", "Сначала выберите книгу в таблице.")
        title = self.tree.set(str(book_id), "title")
        if messagebox.askyesno("Удаление", f"Удалить книгу «{title}»?"):
            try:
                self.app.db.delete_book(book_id)
            except ValueError as e:
                return messagebox.showerror("Ошибка", str(e))
            self.refresh()


class IssueView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        label(self, "Выдача книги", font=("Georgia", 16, "bold")).pack(anchor="w", pady=(0, 8))
        label(self, "Выберите книгу в таблице и введите имя читателя.").pack(anchor="w")
        self.tree = make_tree(self, BOOK_COLUMNS)

        bar = tk.Frame(self, bg=BG)
        bar.pack(fill="x", pady=8)
        label(bar, "Читатель:").pack(side="left")
        self.reader = tk.StringVar()
        entry = ttk.Entry(bar, textvariable=self.reader, width=30)
        entry.pack(side="left", padx=6)
        entry.bind("<Return>", lambda e: self.issue())
        self.entry = entry
        label(bar, f"Дата выдачи: {date.today().strftime('%d.%m.%Y')}").pack(side="left", padx=10)
        ttk.Button(bar, text="Выдать книгу", style="Brown.TButton",
                   command=self.issue).pack(side="left")

    def on_show(self):
        fill_books(self.tree, self.app.db.all_books())

    def issue(self):
        book_id = selected_id(self.tree)
        reader = self.reader.get().strip()
        if book_id is None:
            return messagebox.showwarning("Выдача", "Выберите книгу в таблице.")
        if not reader:
            return messagebox.showwarning("Выдача", "Введите имя читателя.")
        try:
            self.app.db.issue_book(book_id, reader)
        except ValueError as e:
            return messagebox.showerror("Ошибка", str(e))
        title = self.tree.set(str(book_id), "title")
        messagebox.showinfo("Выдача", f"Книга «{title}» выдана читателю: {reader}.")
        self.reader.set("")
        self.on_show()
        self.tree.selection_set(str(book_id))


class ReturnView(tk.Frame):
    COLUMNS = [("id", "№", 50, "center"), ("title", "Книга", 260, "w"),
               ("reader", "Читатель", 190, "w"), ("issue", "Дата выдачи", 110, "center"),
               ("ret", "Дата возврата", 110, "center")]

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        label(self, "Выданные книги и возврат",
              font=("Georgia", 16, "bold")).pack(anchor="w", pady=(0, 8))
        self.show_all = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Показывать и возвращённые", variable=self.show_all,
                       bg=BG, font=FONT, activebackground=BG,
                       command=self.on_show).pack(anchor="w")
        self.tree = make_tree(self, self.COLUMNS)
        self.status = label(self, "")
        self.status.pack(anchor="w", pady=4)
        ttk.Button(self, text="Вернуть выбранную книгу", style="Brown.TButton",
                   command=self.give_back).pack(anchor="w")

    def on_show(self):
        loans = self.app.db.loans(self.show_all.get())
        self.tree.delete(*self.tree.get_children())
        for ln in loans:
            self.tree.insert("", "end", iid=str(ln["id"]),
                             values=(ln["id"], ln["title"], ln["reader"], ln["issue_date"],
                                     ln["return_date"] or "—"))
        self.status.config(text=f"Записей: {len(loans)}")

    def give_back(self):
        loan_id = selected_id(self.tree)
        if loan_id is None:
            return messagebox.showwarning("Возврат", "Выберите запись о выдаче в таблице.")
        try:
            self.app.db.return_book(loan_id)
        except ValueError as e:
            return messagebox.showerror("Ошибка", str(e))
        messagebox.showinfo("Возврат", "Книга возвращена в библиотеку.")
        self.on_show()


# =====================================================================
#                             ОКНА ПРИЛОЖЕНИЯ
# =====================================================================
class LoginFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)
        self.app = app
        tk.Label(self, text="Библиотечная система", bg=HEADER, fg="white",
                 font=("Georgia", 20, "bold")).pack(fill="x", ipady=14)
        form = tk.Frame(self, bg=BG)
        form.pack(pady=20)
        label(form, "Логин:").grid(row=0, column=0, sticky="e", padx=6, pady=8)
        label(form, "Пароль:").grid(row=1, column=0, sticky="e", padx=6, pady=8)
        self.login = ttk.Entry(form, width=24)
        self.password = ttk.Entry(form, width=24, show="*")
        self.login.grid(row=0, column=1, pady=8)
        self.password.grid(row=1, column=1, pady=8)
        self.login.focus()
        self.password.bind("<Return>", lambda e: self.enter())
        self.login.bind("<Return>", lambda e: self.password.focus())

        buttons = tk.Frame(self, bg=BG)
        buttons.pack()
        ttk.Button(buttons, text="Войти", style="Brown.TButton",
                   command=self.enter).pack(side="left", padx=6)
        ttk.Button(buttons, text="Выход", style="Brown.TButton",
                   command=app.on_close).pack(side="left", padx=6)
        label(self, "Демо: admin / admin123,  librarian / lib123",
              fg="#8a7a6a", font=("Georgia", 9)).pack(pady=18)

    def enter(self):
        user = self.app.db.check_user(self.login.get().strip(), self.password.get())
        if user is None:
            messagebox.showerror("Ошибка входа", "Неверный логин или пароль.")
            self.password.delete(0, tk.END)
            return
        self.app.show_main(user)


class MainFrame(tk.Frame):
    def __init__(self, app):
        super().__init__(app, bg=BG)
        self.app = app
        user = app.user

        header = tk.Frame(self, bg=HEADER)
        header.pack(fill="x")
        tk.Label(header, text="Библиотечная система", bg=HEADER, fg="white",
                 font=("Georgia", 20, "bold")).pack(side="left", padx=20, pady=12)
        tk.Label(header, text=f"{user['full_name']} ({ROLE_NAMES[user['role']]})",
                 bg=HEADER, fg="#e8d9c0", font=FONT).pack(side="right", padx=20)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)
        menu = tk.Frame(body, bg=BG)
        menu.pack(side="left", fill="y", padx=15, pady=15)
        self.content = tk.Frame(body, bg=BG)
        self.content.pack(side="left", fill="both", expand=True, padx=(0, 15), pady=15)

        # каждый раздел создаётся один раз; переключение — просто смена видимого Frame
        self.sections = {
            "list": BooksView(self.content, app, searchable=False),
            "search": BooksView(self.content, app, searchable=True),
            "issue": IssueView(self.content, app),
            "return": ReturnView(self.content, app),
        }
        self.current = None

        items = [("Добавить книгу", self.add_book),
                 ("Список книг", lambda: self.show("list")),
                 ("Поиск", lambda: self.show("search")),
                 ("Выдать книгу", lambda: self.show("issue")),
                 ("Вернуть книгу", lambda: self.show("return")),
                 ("Выйти из аккаунта", app.show_login)]
        for text, cmd in items:
            b = ttk.Button(menu, text=text, style="Brown.TButton", command=cmd, width=20)
            b.pack(pady=5, ipady=4)
            if text == "Добавить книгу" and user["role"] != "admin":
                b.state(["disabled"])        # только администратор
        self.show("list")

    def show(self, name):
        if self.current:
            self.current.pack_forget()
        self.current = self.sections[name]
        self.current.pack(fill="both", expand=True)
        self.current.on_show()

    def refresh_current(self):
        self.current.on_show()

    def add_book(self):
        BookDialog(self.app, None, self.refresh_current)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Библиотечная система")
        self.configure(bg=BG)
        self.db = Database(DB_PATH)
        self.user = None
        self.frame = None
        self.main = None

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Brown.TButton", background=BTN, foreground="white",
                        font=FONT, padding=6, borderwidth=0)
        style.map("Brown.TButton",
                  background=[("disabled", "#c9bba9"), ("active", BTN_ACTIVE)],
                  foreground=[("disabled", "#f0e8dc")])
        style.configure("Treeview", rowheight=26, font=("Georgia", 10))
        style.configure("Treeview.Heading", font=("Georgia", 10, "bold"),
                        background=HEADER, foreground="white")
        style.map("Treeview.Heading", background=[("active", BTN)])
        style.map("Treeview", background=[("selected", BTN)])

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_login()

    def center(self, width, height):
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _swap(self, frame):
        if self.frame:
            self.frame.destroy()
        self.frame = frame
        frame.pack(fill="both", expand=True)

    def show_login(self):
        self.user = None
        self.main = None
        self.minsize(1, 1)
        self.resizable(False, False)
        self.center(420, 360)
        self._swap(LoginFrame(self))

    def show_main(self, user):
        self.user = user
        self.resizable(True, True)
        self.minsize(950, 580)
        self.center(1050, 650)
        self.main = MainFrame(self)
        self._swap(self.main)

    def on_close(self):
        self.db.conn.close()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
