from maze import *
from color import *
from inputbox import InputBox
from button import Button
from text import Text

pg.init()

clock = pg.time.Clock()

m, n = 1, 1

WIDTH = 800
HEIGHT = 800
w = 20

FPS = 60

wn = pg.display.set_mode((WIDTH, HEIGHT))  # окно игры
pg.display.set_caption('Maze')


M = Maze(n, m, w)
B = Button(600, 700, "Сгенерировать")  # кнопка генерации
SAVE_IM = Button(600, 650, "Сохранить")  # Сохранение фотки лабиринта

For_n = InputBox(300, 700, 100, 30)  # поле для ввода ширины
For_m = InputBox(300, 650, 100, 30)  # поле для ввода длины

firstx, firsty = -100, -100
secondx, secondy = -100, -100

done = False

while not done:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        elif B.is_clicked(event):
            n, m = min(35, int(For_n.last_text)), min(30, int(For_m.last_text))
            M = Maze(n, m, w)
            firstx = -100
            firsty = -100
            secondx = -100
            secondy = -100

        elif SAVE_IM.is_clicked(event):
            rect = M.rect
            sub = wn.subsurface(rect)
            pg.image.save(sub, "/myapp/data/screenshot.jpg")

        elif event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            if M.rect.collidepoint(pos):
                if firstx == -100:
                    (firstx, firsty) = pos
                else:
                    (secondx, secondy) = pos

            else:
                firstx = -100
                firsty = -100
                secondx = -100
                secondy = -100

        For_n.handle_event(event)
        For_m.handle_event(event)

    vx, vy = (firstx - M.dx) // w, (firsty - M.dy) // w
    ux, uy = (secondx - M.dx) // w, (secondy - M.dy) // w

    txt_n = Text(220, 650, f'n: {min(35, int(For_m.last_text))}')
    txt_m = Text(220, 700, f'm: {min(30, int(For_n.last_text))}')

    For_n.update()
    For_m.update()
    wn.fill(WHITE)
    if secondx != -100:
        M.path(ux * m + uy, vx * m + vy, wn)
    pg.draw.rect(wn, BLUE, (M.dx + vx * w + 2, M.dy + vy * w + 2, M.w - 2, M.w - 2), 2)
    For_n.draw(wn)
    For_m.draw(wn)
    B.draw(wn)
    SAVE_IM.draw(wn)
    M.update(wn)
    txt_n.draw(wn)
    txt_m.draw(wn)

    pg.display.flip()
    clock.tick(FPS)
