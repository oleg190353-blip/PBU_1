import json
import tkinter as tk
import urllib.request
from tkinter import ttk, messagebox

API_URL = "https://open.er-api.com/v6/latest/"

# Словарь: код валюты -> русское название
CURRENCY_NAMES = {
    "RUB": "Российский рубль",
    "USD": "Американский доллар",
    "EUR": "Евро",
    "GBP": "Британский фунт",
    "JPY": "Японская иена",
    "TRY": "Турецкая лира",
    "AED": "Дирхам ОАЭ",
    "CNY": "Китайский юань",
    "KZT": "Казахстанский тенге",
    "BYN": "Белорусский рубль"}


class ExchangeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы обмена валют")

        frame = tk.Frame(root, padx=20, pady=10)
        frame.pack()

        # --- Базовая валюта ---
        tk.Label(frame, text="Базовая валюта").pack(pady=5)
        self.base_combo = ttk.Combobox(frame, values=list(CURRENCY_NAMES), state="readonly", width=15)
        self.base_combo.set("EUR")
        self.base_combo.pack()
        self.base_label = tk.Label(frame, text=CURRENCY_NAMES[self.base_combo.get()])
        self.base_label.pack(pady=5)

        # --- Вторая базовая валюта ---
        tk.Label(frame, text="Вторая базовая валюта").pack(pady=5)
        self.base2_combo = ttk.Combobox(frame, values=list(CURRENCY_NAMES), state="readonly", width=15)
        self.base2_combo.set("USD")
        self.base2_combo.pack()
        self.base2_label = tk.Label(frame, text=CURRENCY_NAMES[self.base2_combo.get()])
        self.base2_label.pack(pady=5)

        # --- Целевая валюта ---
        tk.Label(frame, text="Целевая валюта").pack(pady=5)
        self.target_combo = ttk.Combobox(frame, values=list(CURRENCY_NAMES), state="readonly", width=15)
        self.target_combo.set("RUB")
        self.target_combo.pack()
        self.target_label = tk.Label(frame, text=CURRENCY_NAMES[self.target_combo.get()])
        self.target_label.pack(pady=5)

        # Кнопка получения курса
        tk.Button(frame, text="Получить курс обмена", command=self.exchange).pack(pady=10)

        # Поле для вывода результата
        self.result_text = tk.Text(frame, height=3, width=40)
        self.result_text.pack(pady=5)

        # Обновляем подписи при смене валюты
        self.base_combo.bind("<<ComboboxSelected>>", self.update_labels)
        self.base2_combo.bind("<<ComboboxSelected>>", self.update_labels)
        self.target_combo.bind("<<ComboboxSelected>>", self.update_labels)

    def update_labels(self, event=None):
        self.base_label.config(text=CURRENCY_NAMES.get(self.base_combo.get(), ""))
        self.base2_label.config(text=CURRENCY_NAMES.get(self.base2_combo.get(), ""))
        self.target_label.config(text=CURRENCY_NAMES.get(self.target_combo.get(), ""))

    def get_rate(self, base, target):
        """Запрашивает JSON с курсами и возвращает курс base -> target."""
        url = API_URL + base
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
            rates = data.get("rates", {})
            rate = rates.get(target)
            if rate is None:
                return None
            return rate
        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось получить данные: " + str(e))
            return None

    def exchange(self):
        """Запрашивает и отображает курс для одной базовой валюты."""
        base = self.base_combo.get()
        target = self.target_combo.get()

        rate = self.get_rate(base, target)
        if rate is None:
            return

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0",
                                "Курс " + base + " -> " + target + ": " + str(round(rate, 4)))


if __name__ == "__main__":
    root = tk.Tk()
    app = ExchangeApp(root)
    root.mainloop()
