from tkinter import *

root = Tk()
root.title("Калькулятор дробей")
root.geometry("300x140+600+150")

frame = Frame(root)
frame.pack(pady=10)

num1 = Entry(frame, width=2)
num1.config(font=("Arial", 15), justify="center")
num1.grid(row=0, column=0)
Label(frame, text= chr(8212)*3 ).grid(row=1, column=0)
den1 = Entry(frame, width=2)
den1.config(font=("Arial", 15), justify="center")
den1.grid(row=2, column=0)

oper = Entry(frame, width=2)
oper.config(font=("Arial", 15), justify="center")
oper.grid(row=1, column=1, padx=5)

num2 = Entry(frame, width=2)
num2.config(font=("Arial", 15), justify="center")
num2.grid(row=0, column=2)
Label(frame, text= chr(8212)*3 ).grid(row=1, column=2)
den2 = Entry(frame, width=2)
den2.config(font=("Arial", 15), justify="center")
den2.grid(row=2, column=2)

btn = Button(frame, text='=')
btn.config(font=("Arial", 15), justify="center", width=3)
btn.grid(row=1, column=3, padx=5)

res_int = Label(frame, text='   ', bg="light gray" )
res_int.config(font=("Arial", 20), justify="center")
res_int.grid(row=1, column=4)

num3 = Label(frame, width=2, bg="light gray")
num3.config(font=("Arial", 15), justify="center")
num3.grid(row=0, column=5)
Label(frame, text= chr(8212)*3 ).grid(row=1, column=5)
den3 = Label(frame, width=2, bg="light gray")
den3.config(font=("Arial", 15), justify="center")
den3.grid(row=2, column=5)


root.mainloop()