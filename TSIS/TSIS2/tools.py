# tools.py

import pygame
from datetime import datetime
import math

WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)

# ========= FLOOD FILL =========
def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or px >= WIDTH or py < 0 or py >= HEIGHT:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px+1, py))
        stack.append((px-1, py))
        stack.append((px, py+1))
        stack.append((px, py-1))


# ========= SAVE =========
def save_canvas(surface):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"painting_{now}.png"
    pygame.image.save(surface, filename)
    print("Saved:", filename)


# ========= BASIC SHAPES =========
def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)

def draw_rect(surface, color, start, end, size):
    rect = pygame.Rect(start, (end[0]-start[0], end[1]-start[1]))
    pygame.draw.rect(surface, color, rect, size)

def draw_circle(surface, color, start, end, size):
    radius = int(((end[0]-start[0])**2 + (end[1]-start[1])**2) ** 0.5)
    pygame.draw.circle(surface, color, start, radius, size)

# ========= NEW SHAPES =========
def draw_square(surface, color, start, end, size):
    side = max(abs(end[0]-start[0]), abs(end[1]-start[1]))
    rect = pygame.Rect(start[0], start[1], side, side)
    pygame.draw.rect(surface, color, rect, size)

def draw_right_triangle(surface, color, start, end, size):
    p1 = start
    p2 = (end[0], start[1])
    p3 = end
    pygame.draw.polygon(surface, color, [p1, p2, p3], size)

def draw_equilateral_triangle(surface, color, start, end, size):
    side = abs(end[0] - start[0])
    height = int(side * math.sqrt(3) / 2)

    p1 = (start[0], start[1])
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side//2, start[1] - height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], size)

def draw_rhombus(surface, color, start, end, size):
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2

    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2

    points = [
        (cx, cy - dy),
        (cx + dx, cy),
        (cx, cy + dy),
        (cx - dx, cy)
    ]

    pygame.draw.polygon(surface, color, points, size)