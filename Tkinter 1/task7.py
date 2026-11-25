# Задание 7. Мини-проект «Библиотечная система»
import tkinter as tk
from tkinter import messagebox

BG = "#f4ecd8"        # фон окна
HEADER = "#5b3a29"    # цвет шапки
BTN = "#8b5e3c"       # цвет кнопок
BTN_ACTIVE = "#a67550"

root = tk.Tk()
root.title("Библиотечная система")

width, height = 800, 500
x = (root.winfo_screenwidth() - width) // 2
y = (root.winfo_screenheight() - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")
root.configure(bg=BG)

# Шапка с названием
header = tk.Frame(root, bg=HEADER)
header.pack(fill="x")
tk.Label(header, text="Библиотечная система", bg=HEADER, fg="white",
         font=("Georgia", 26, "bold")).pack(pady=20)

# Обработчики кнопок
def show_list():
    messagebox.showinfo("Список книг", "Здесь будет отображён список всех книг библиотеки.")

def add_book():
    messagebox.showinfo("Добавить книгу", "Здесь можно будет добавить новую книгу в каталог.")

def find_book():
    messagebox.showinfo("Найти книгу", "Здесь можно будет найти книгу по названию или автору.")

def info():
    messagebox.showinfo("Информация", "Библиотечная система, версия 1.0\nУчебный проект на Tkinter.")

def exit_app():
    if messagebox.askyesno("Выход", "Вы действительно хотите выйти?"):
        root.destroy()

# Кнопки
menu = tk.Frame(root, bg=BG)
menu.pack(expand=True)

for text, cmd in [("Список книг", show_list), ("Добавить книгу", add_book),
                  ("Найти книгу", find_book), ("Информация", info),
                  ("Выход", exit_app)]:
    tk.Button(menu, text=text, command=cmd, width=25, bg=BTN, fg="white",
              activebackground=BTN_ACTIVE, activeforeground="white",
              font=("Georgia", 13), relief="flat").pack(pady=7, ipady=5)

root.protocol("WM_DELETE_WINDOW", exit_app)   # подтверждение и при закрытии крестиком

root.mainloop()
