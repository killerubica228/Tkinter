# Задание 4. Главное окно учебного приложения «Электронный дневник»
import tkinter as tk

BG = "#eaf2fb"

root = tk.Tk()
root.title("Электронный дневник")
root.geometry("500x380")
root.configure(bg=BG)

tk.Label(root, text="Электронный дневник", bg=BG, fg="#1f3a5f",
         font=("Arial", 22, "bold")).pack(pady=(30, 10))
tk.Label(root, text="Добро пожаловать!", bg=BG,
         font=("Arial", 14)).pack(pady=5)
tk.Label(root, text="Пользователь: Иванов Иван Иванович", bg=BG,
         font=("Arial", 12, "italic")).pack(pady=5)

tk.Button(root, text="Начать работу", width=20, font=("Arial", 12),
          bg="#4a90d9", fg="white").pack(pady=(25, 10), ipady=4)
tk.Button(root, text="Выход", width=20, font=("Arial", 12),
          command=root.destroy).pack(pady=10, ipady=4)

root.mainloop()
