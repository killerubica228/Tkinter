# Задание 3. Размещение окна по центру экрана
import tkinter as tk

root = tk.Tk()
root.title("Окно по центру")

width, height = 500, 350
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f"{width}x{height}+{x}+{y}")

tk.Label(root, text=f"Экран: {screen_width}×{screen_height}\nПозиция окна: {x}, {y}",
         font=("Arial", 12)).pack(expand=True)

root.mainloop()
