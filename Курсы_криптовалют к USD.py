import datetime
import json
import tkinter as tk
import urllib.request
from tkinter import ttk

API_URL = ("https://api.coingecko.com/api/v3/simple/price"
           "?ids=bitcoin,ethereum,litecoin,dogecoin,solana"
           "&vs_currencies=usd&include_24hr_change=true")

# id монеты в CoinGecko -> (название для отображения, тикер)
COINS = {
    "bitcoin": ("Bitcoin", "BTC"),
    "ethereum": ("Ethereum", "ETH"),
    "litecoin": ("Litecoin", "LTC"),
    "dogecoin": ("Dogecoin", "DOGE"),
    "solana": ("Solana", "SOL"), }


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

        self.tree.tag_configure("up", foreground="green")
        self.tree.tag_configure("down", foreground="red")

        # Кнопка обновления
        tk.Button(root, text="Обновить курсы", command=self.refresh,
                  width=20).pack(pady=5)

        # Подпись со временем последнего обновления
        self.status_label = tk.Label(root, text="", fg="gray")
        self.status_label.pack(pady=5)

        # Загружаем данные сразу при запуске
        self.refresh()

    def refresh(self):
        """Запрашивает JSON с CoinGecko и заполняет таблицу."""
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
            change = info.get("usd_24h_change")

            if price is None:
                continue

            if change is not None:
                sign = "+" if change >= 0 else "-"
                tag = "up" if change >= 0 else "down"
                change_str = "{} {:.2f}%".format(sign, abs(change))
            else:
                tag = ""
                change_str = "—"

            self.tree.insert("", tk.END, values=(
                name + " (" + ticker + ")",
                "{:,.2f}".format(price),
                change_str), tags=(tag,))

        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text="Обновлено: " + now, fg="gray")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
