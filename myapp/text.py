import pygame as pg
from color import *

font = pg.font.Font("C:/Users/HONOR/Documents/myapp/myapp/static/Rubik-Regular.ttf", 24)


class Text:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.img = font.render(text, True, WHITE)  # создаём текст

    def draw(self, wn):  # текст
        rect = self.img.get_rect()
        rect = (self.x, self.y, rect[2], rect[3])
        pg.draw.rect(wn, BLACK, rect)
        wn.blit(self.img, (self.x, self.y))
