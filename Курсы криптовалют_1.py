import tkinter as tk
from tkinter import ttk

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

        # При смене валюты будет перестраиваться таблица
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

        # Настройка тегов цветов для индикатора изменения
        self.tree.tag_configure("up", foreground="green")
        self.tree.tag_configure("down", foreground="red")

        # --- Кнопка обновления и строка состояния ---
        tk.Button(root, text="Обновить курсы", command=self.refresh,
                  width=20).pack(pady=5)

        self.status_label = tk.Label(root, text="", fg="gray")
        self.status_label.pack(pady=5)

    def on_currency_change(self, event=None):
        """Обновляет подпись с названием валюты."""
        self.currency_label.config(text=CURRENCY_NAMES.get(self.currency_combo.get(), ""))
        # Данные появятся во 2-м коммите
        self.refresh()

    def refresh(self):
        """Заглушка: в 1-м коммите таблица остаётся пустой."""
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()
