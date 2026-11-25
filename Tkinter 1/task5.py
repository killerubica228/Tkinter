# Задание 5. Окно авторизации
import tkinter as tk

root = tk.Tk()
root.title("Авторизация")
root.geometry("350x260")
root.resizable(False, False)          # запрет изменения размера

tk.Label(root, text="Вход в систему", font=("Arial", 16, "bold")).pack(pady=15)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="Логин:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=8, sticky="e")
entry_login = tk.Entry(frame, width=22)
entry_login.grid(row=0, column=1, padx=5, pady=8)

tk.Label(frame, text="Пароль:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=8, sticky="e")
entry_password = tk.Entry(frame, width=22, show="*")   # скрытие символов
entry_password.grid(row=1, column=1, padx=5, pady=8)

status = tk.Label(root, text="", fg="red")
status.pack()

def login():
    if entry_login.get() and entry_password.get():
        status.config(text="Данные введены", fg="green")
    else:
        status.config(text="Заполните оба поля", fg="red")

def clear():
    entry_login.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    status.config(text="")
    entry_login.focus()

buttons = tk.Frame(root)
buttons.pack(pady=15)
tk.Button(buttons, text="Войти", width=9, command=login).grid(row=0, column=0, padx=4)
tk.Button(buttons, text="Очистить", width=9, command=clear).grid(row=0, column=1, padx=4)
tk.Button(buttons, text="Закрыть", width=9, command=root.destroy).grid(row=0, column=2, padx=4)

root.mainloop()
