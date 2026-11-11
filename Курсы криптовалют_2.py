import datetime
import json
import tkinter as tk
import urllib.request
from tkinter import ttk

API_BASE = "https://api.coingecko.com/api/v3/simple/price"

# id монеты в CoinGecko -> (название для отображения, тикер)
COINS = {
    "bitcoin": ("Bitcoin", "BTC"),
    "ethereum": ("Ethereum", "ETH"),
    "litecoin": ("Litecoin", "LTC"),
    "dogecoin": ("Dogecoin", "DOGE"),
    "solana": ("Solana", "SOL"),
}

# Список фиатных валют: код -> русское название
CURRENCY_NAMES = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум",
}


def fmt(value):
    """Крупные цены — 2 знака после запятой, мелкие — до 6."""
    if value is None:
        return "—"
    if value >= 1:
        return "{:,.2f}".format(value)
    return "{:.6f}".format(value)


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют")

        # --- Выбор целевой валюты ---
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text="Целевая валюта:").pack(side=tk.LEFT, padx=5)

        self.currency_combo = ttk.Combobox(top_frame, values=list(CURRENCY_NAMES),
                                           state="readonly", width=15)
        self.currency_combo.set("USD")
        self.currency_combo.pack(side=tk.LEFT, padx=5)

        # Подпись с полным названием выбранной валюты
        self.currency_label = tk.Label(top_frame, text=CURRENCY_NAMES["USD"], fg="gray")
        self.currency_label.pack(side=tk.LEFT, padx=10)

        # Смена валюты в списке мгновенно перестраивает таблицу
        self.currency_combo.bind("<<ComboboxSelected>>", self.on_currency_change)

        # --- Таблица: монета, цена, изменение в "%" ---
        columns = ("coin", "price", "change")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=6)
        self.tree.heading("coin", text="Монета")
        self.tree.heading("price", text="Цена (USD)")
        self.tree.heading("change", text="%")
        self.tree.column("coin", width=200, anchor=tk.W)
        self.tree.column("price", width=150, anchor=tk.E)
        self.tree.column("change", width=100, anchor=tk.E)
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree.tag_configure("up", foreground="green")
        self.tree.tag_configure("down", foreground="red")

        # --- Кнопка обновления и строка состояния ---
        tk.Button(root, text="Обновить курсы", command=self.refresh,
                  width=20).pack(pady=5)

        self.status_label = tk.Label(root, text="", fg="gray")
        self.status_label.pack(pady=5)

        # Загружаем данные сразу при запуске
        self.refresh()

    def on_currency_change(self, event=None):
        """При смене валюты обновляет подпись и перестраивает таблицу."""
        currency = self.currency_combo.get()
        self.currency_label.config(text=CURRENCY_NAMES.get(currency, ""))
        self.refresh()

    def refresh(self):
        """Запрашивает цены всех монет в выбранной валюте и заполняет таблицу."""
        currency = self.currency_combo.get()
        ids = ",".join(COINS.keys())
        url = (API_BASE + "?ids=" + ids +
               "&vs_currencies=" + currency.lower() +
               "&include_24hr_change=true")

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        # Заголовок столбца цены зависит от выбранной валюты
        self.tree.heading("price", text=f"Цена ({currency})")

        self.tree.delete(*self.tree.get_children())

        for coin_id, (name, ticker) in COINS.items():
            info = data.get(coin_id, {})
            price = info.get(currency.lower())

            if price is None:
                continue

            # Изменение за 24 часа: API возвращает отдельное поле
            change = info.get(f"{currency.lower()}_24h_change")
            if change is not None:
                sign = "+" if change >= 0 else "-"
                tag = "up" if change >= 0 else "down"
                change_str = f"{sign} {abs(change):.2f}%"
            else:
                tag = ""
                change_str = "—"

            self.tree.insert("", tk.END, values=(
                f"{name} ({ticker})",
                fmt(price),
                change_str), tags=(tag,))

        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"Обновлено: {now} ({currency})", fg="gray")


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
