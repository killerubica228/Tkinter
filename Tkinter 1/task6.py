# Задание 6. Настройка интерфейса через переменные
import tkinter as tk
import random

window_title = "Настройка через переменные"
window_width = 550
window_height = 350
background_color = "#fff4d6"

root = tk.Tk()
root.title(window_title)
root.geometry(f"{window_width}x{window_height}")
root.configure(bg=background_color)

label = tk.Label(root, text=f"Заголовок: {window_title}\n"
                            f"Размер: {window_width}×{window_height}\n"
                            f"Цвет фона: {background_color}",
                 bg=background_color, font=("Arial", 13))
label.pack(pady=40)

colors = ["#fff4d6", "#d6f5e3", "#e0d6ff", "#ffd6d6", "#d6ecff", "#f0f0f0"]

def change_color():
    global background_color
    new = random.choice([c for c in colors if c != background_color])
    background_color = new
    root.configure(bg=new)
    label.config(bg=new, text=f"Заголовок: {window_title}\n"
                              f"Размер: {window_width}×{window_height}\n"
                              f"Цвет фона: {new}")

tk.Button(root, text="Сменить цвет фона", font=("Arial", 12),
          command=change_color).pack(pady=10, ipady=4)

root.mainloop()
