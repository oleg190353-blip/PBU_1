import datetime
import json
import tkinter as tk
import urllib.request
from tkinter import ttk

API_URL = ("https://api.coingecko.com/api/v3/simple/price"
           "?ids=bitcoin,ethereum,litecoin,dogecoin,solana"
           "&vs_currencies=usd")

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

        # Таблица курсов
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

        # Загружаем данные сразу при запуске
        self.refresh()

    def refresh(self):
        """Запрашивает JSON с CoinGecko и заполняет таблицу ценами."""
        try:
            with urllib.request.urlopen(API_URL, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as e:
            self.status_label.config(text="Ошибка загрузки: " + str(e), fg="red")
            return

        self.tree.delete(*self.tree.get_children())

        for coin_id, (name, ticker) in COINS.items():
            info = data.get(coin_id, {})
            price = info.get("usd")

            if price is None:
                continue

            self.tree.insert("", tk.END, values=(
                name + " (" + ticker + ")",
                "{:,.2f}".format(price),
                "—"))

        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text="Обновлено: " + now, fg="gray")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
