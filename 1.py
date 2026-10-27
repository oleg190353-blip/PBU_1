import turtle

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

# Подбираем палитру под изображение: от светло‑голубого к фиолетовому, контуры — розовый/оранжевый
layers = 12
base_size = 160
angle_shift = 18  # угол «скручивания» для эффекта звезды

for i in range(layers):
    # Плавный переход цветов по слоям
    if i < layers // 3:
        fill_col = "lightcyan"
        outline_col = "hotpink"
    elif i < 2 * layers // 3:
        fill_col = "lightblue"
        outline_col = "orange"
    else:
        fill_col = "mediumpurple"
        outline_col = "gold"

    t.color(outline_col, fill_col)
    t.begin_fill()

    # Рисуем «скрученный квадрат»
    side = base_size - i * 10  # уменьшаем размер с каждым слоем
    for _ in range(4):
        t.forward(side)
        t.left(90 + angle_shift)

    t.end_fill()

turtle.done()
