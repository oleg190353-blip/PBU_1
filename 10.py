from tkinter import *
from tkinter import messagebox


def is_time(s):
    # Сначала проверяем длину: должно быть ровно 5 символов
    if len(s) != 5:
        return False

    # Проверяем позиции: [0] и [1] — цифры, [2] — двоеточие, [3] и [4] — цифры
    if not (s[0].isdigit() and s[1].isdigit()):
        return False
    if s[2] != ':':
        return False
    if not (s[3].isdigit() and s[4].isdigit()):
        return False

    # Преобразуем в числа и проверяем диапазоны
    hours = int(s[0:2])
    minutes = int(s[3:5])

    if hours < 0 or hours > 23:
        return False
    if minutes < 0 or minutes > 59:
        return False

    return True


def to_minutes(s):
    """Возвращает количество минут от полуночи для заданного времени в формате ЧЧ:ММ"""
    hours = int(s[0:2])
    minutes = int(s[3:5])
    return hours * 60 + minutes


def set_alarm():
    now_text = now_entry.get()
    alarm_text = alarm_entry.get()

    # Проверяем оба поля на корректность времени
    if not is_time(now_text) or not is_time(alarm_text):
        messagebox.showerror("Ошибка", "Время нужно в формате ЧЧ:ММ")
        result.config(text="Напоминание не поставлено")
        return

    now_mins = to_minutes(now_text)
    alarm_mins = to_minutes(alarm_text)

    # Рассчитываем разницу
    diff = alarm_mins - now_mins

    # Если будильник на завтра (время уже прошло сегодня)
    if diff < 0:
        diff += 24 * 60  # добавляем сутки в минутах

    hours = diff // 60
    mins = diff % 60

    result.config(text=f"Сработает через {hours} ч {mins} мин")


window = Tk()
window.title("Напоминалка")
window.geometry("380x240")

Label(text="Сейчас:").pack()
now_entry = Entry()
now_entry.pack()

Label(text="Напомнить в:").pack()
alarm_entry = Entry()
alarm_entry.pack()

Button(text="Поставить", command=set_alarm).pack(pady=10)

result = Label(text="Напоминание не поставлено")
result.pack()

window.mainloop()
