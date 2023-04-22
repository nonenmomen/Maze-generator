import random as rnd
from color import *
import pygame as pg
from collections import deque
# from text import Text


def gen(n, m):  # генератор лабиринта в виде графа
    p = [k1 for k1 in range(n * m)]
    sz = [1 for _ in range(n * m)]
    g = [[] for _ in range(n * m)]

    def leader(v):
        if p[v] == v:
            return v

        lead = leader(p[v])
        p[v] = lead
        return lead

    def unite(u, v):
        u = leader(u)
        v = leader(v)

        if sz[v] < sz[u]:
            u, v = v, u

        p[u] = v
        sz[v] += sz[u]

    c = 0
    while c < n * m - 1:
        vx, vy = rnd.randint(0, n - 1), rnd.randint(0, m - 1)
        a = []

        if vx < n - 1:
            a.append((1, 0))

        if vx > 0:
            a.append((-1, 0))

        if vy < m - 1:
            a.append((0, 1))

        if vy > 0:
            a.append((0, -1))

        ln = len(a)

        r = rnd.randint(0, ln - 1)
        dx = a[r][0]
        dy = a[r][1]

        ux = vx + dx
        uy = vy + dy
        if leader(vx * m + vy) != leader(ux * m + uy):
            unite((vx * m + vy), (ux * m + uy))
            g[vx * m + vy].append(ux * m + uy)
            g[ux * m + uy].append(vx * m + vy)
            c += 1
    return g


class Maze:
    def __init__(self, n, m, w):
        self.w = w
        self.n = n
        self.m = m
        self.g = gen(n, m)
        self.dx = (800 - n * w) // 2
        self.dy = 20
        self.rect = pg.Rect(self.dx, self.dy, self.n * w, self.m * w)

    def update(self, wn):
        self.draw(wn)

    def create_image(self, wn):  # разрисовываем сетку
        for row in range(self.n):
            for col in range(self.m):
                pg.draw.line(wn, BLACK, (self.dx + row * self.w, self.dy + col * self.w),
                             (self.dx + (row + 1) * self.w, self.dy + (col * self.w)), 4)
                pg.draw.line(wn, BLACK, (self.dx + row * self.w, self.dy + col * self.w),
                             (self.dx + (row * self.w), self.dy + (col + 1) * self.w), 4)
                pg.draw.line(wn, BLACK, (self.dx + (row + 1) * self.w, self.dy + col * self.w),
                             (self.dx + (row + 1) * self.w, self.dy + (col + 1) * self.w), 3)
                pg.draw.line(wn, BLACK, (self.dx + row * self.w, self.dy + (col + 1) * self.w),
                             (self.dx + (row + 1) * self.w, self.dy + (col + 1) * self.w), 3)

    def draw(self, wn):  # убираем стенки между смежными клетками
        self.create_image(wn)
        for i in range(self.n):
            for j in range(self.m):
                for x in self.g[i * self.m + j]:
                    x1 = i
                    y1 = j
                    x2 = (x // self.m)
                    y2 = (x % self.m)
                    if x1 > x2:
                        x1, x2 = x2, x1

                    if y1 > y2:
                        y1, y2 = y2, y1

                    if x1 + 1 == x2:
                        pg.draw.line(wn, WHITE, (self.dx + x2 * self.w, self.dy + y1 * self.w + 3),
                                     (self.dx + x2 * self.w, self.dy + (y1 + 1) * self.w - 2), 4)

                    if y1 + 1 == y2:
                        pg.draw.line(wn, WHITE, (self.dx + x1 * self.w + 3, self.dy + y2 * self.w),
                                     (self.dx + (x1 + 1) * self.w - 2, self.dy + y2 * self.w), 4)

    def path(self, start, goal, wn):  # находим, а затем строим путь
        visited = {start: None}
        queue = deque([start])

        path = []
        while queue:
            current_node = queue.popleft()
            if current_node == goal:

                while current_node is not None:
                    path.append(current_node)
                    current_node = visited[current_node]
                path = list(reversed(path))
                break

            for neighbor in self.g[current_node]:
                if neighbor not in visited:
                    visited[neighbor] = current_node
                    queue.append(neighbor)

        for v in path:
            x = v // self.m
            y = v % self.m

            if v == path[len(path) - 1]:
                pg.draw.rect(wn, BLUE, (self.dx + x * self.w + 2, self.dy + y * self.w + 2, self.w - 2, self.w - 2), 2)

            else:
                pg.draw.rect(wn, RED, (self.dx + x * self.w + 2, self.dy + y * self.w + 2, self.w - 2, self.w - 2), 2)

        font = pg.font.Font("C:/Users/HONOR/Documents/myapp/myapp/static/Rubik-Regular.ttf", 20)
        img = font.render(f'Длина пути: {len(path) - 1}', True, WHITE)
        rect = img.get_rect()
        rect = (20, 700, rect[2], rect[3])
        pg.draw.rect(wn, BLACK, rect)
        wn.blit(img, (20, 700))
