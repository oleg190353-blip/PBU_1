import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Мой калькулятор")
    root.geometry("420x320")
    root.minsize(420, 320)

    count = 0

    label = tk.Label(root, text="Нажатий: 0")
    label.pack(expand=True)

    def on_click():
        nonlocal count
        count += 1
        label.config(text=f"Нажатий: {count}")

    button = tk.Button(root, text="Проверить", command=on_click)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()