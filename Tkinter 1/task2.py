# Задание 2. Настройка параметров окна
import tkinter as tk

root = tk.Tk()
root.title("Информационная система")
root.geometry("700x450")
root.configure(bg="lightblue")
root.minsize(400, 300)
root.maxsize(900, 600)

tk.Label(root, text="Измените размер окна: он ограничен 400×300 и 900×600",
         bg="lightblue", font=("Arial", 12)).pack(pady=20)

root.mainloop()
