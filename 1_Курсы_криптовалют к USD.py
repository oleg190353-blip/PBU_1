import tkinter as tk
from tkinter import ttk

# id монеты в CoinGecko -> (название для отображения, тикер)
COINS = {
    "bitcoin": ("Bitcoin", "BTC"),
    "ethereum": ("Ethereum", "ETH"),
    "litecoin": ("Litecoin", "LTC"),
    "dogecoin": ("Dogecoin", "DOGE"),
    "solana": ("Solana", "SOL"),
}


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют")

        # Таблица курсов (пока пустая — данные появятся в следующем коммите)
        columns = ("coin", "price", "change")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
        self.tree.heading("coin", text="Монета")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="24 ч")
        self.tree.column("coin", width=200)
        self.tree.column("price", width=150, anchor=tk.E)
        self.tree.column("change", width=100, anchor=tk.E)
        self.tree.pack(padx=10, pady=10)

        # Цвета для индикатора изменения за 24 часа (задел на коммит 3)
        self.tree.tag_configure("up", foreground="green")
        self.tree.tag_configure("down", foreground="red")

        # Подпись со временем последнего обновления
        self.status_label = tk.Label(root, text="", fg="gray")
        self.status_label.pack(pady=5)

    def refresh(self):
        """Запрос данных и заполнение таблицы — будет реализовано в следующем коммите."""
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
