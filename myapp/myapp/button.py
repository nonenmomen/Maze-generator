import pygame as pg
from color import *

font = pg.font.Font("C:/Users/HONOR/Documents/myapp/myapp/static/Rubik-Regular.ttf", 22)


class Button:
    def __init__(self, x, y, text=''):
        self.x = x
        self.y = y
        self.img = font.render(text, True, WHITE)

    def draw(self, wn):
        rect = self.img.get_rect()
        rect = (self.x, self.y, rect[2], rect[3])
        pg.draw.rect(wn, BLACK, rect)
        wn.blit(self.img, (self.x, self.y))

    def is_clicked(self, event):
        rect = self.img.get_rect()
        rect = pg.Rect(self.x, self.y, rect[2], rect[3])
        if event.type == pg.MOUSEBUTTONUP and rect.collidepoint(pg.mouse.get_pos()):  # проверка - произвели ли
            # нажатие на кнопку
            return True
        else:
            return False
