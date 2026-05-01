import json
import random
import pygame
from pathlib import Path

from db import get_personal_best, save_result

WIDTH = 600
HEIGHT = 600
CELL = 30
GRID_W = WIDTH // CELL
GRID_H = HEIGHT // CELL

# 🎨 нежные цвета
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 255)

YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 0, 200)

DARK_RED = (120, 0, 0)

WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
BLACK = (0, 0, 0)

PINK = (255, 182, 193)
PEACH = (255, 218, 185)
YELLOW = (255, 250, 205)
BLUE = (176, 224, 230)
LAVENDER = (221, 160, 221)

GREEN = (170, 240, 170)
ORANGE = (255, 200, 150)
PURPLE = (210, 180, 255)
DARK_RED = (120, 0, 0)

SETTINGS_FILE = Path("settings.json")

DEFAULT_SETTINGS = {
    "snake_color": [255, 182, 193],
    "grid": True,
    "sound": True
}


# ---------------- SETTINGS ----------------
def load_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🔥 автоматически добавляем отсутствующие ключи
    for key, value in DEFAULT_SETTINGS.items():
        if key not in data:
            data[key] = value

    return data


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


# ---------------- HELPERS ----------------
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def same(a, b):
    return a.x == b.x and a.y == b.y


def in_list(p, arr):
    return any(p.x == x.x and p.y == x.y for x in arr)


def random_free(snake, obstacles, extra=None):
    if extra is None:
        extra = []

    while True:
        p = Point(random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))

        if in_list(p, snake.body): continue
        if in_list(p, obstacles): continue
        if in_list(p, extra): continue

        return p


# ---------------- SNAKE ----------------
class Snake:
    def __init__(self, color):
        self.body = [Point(10, 10), Point(9, 10), Point(8, 10)]
        self.dx = 1
        self.dy = 0
        self.color = color
        self.score = 0
        self.food_count = 0
        self.level = 1
        self.shield = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def collision(self):
        h = self.body[0]
        return (
            h.x < 0 or h.x >= GRID_W or
            h.y < 0 or h.y >= GRID_H or
            any(same(h, b) for b in self.body[1:])
        )

    def grow(self):
        h = self.body[0]
        self.body.append(Point(h.x, h.y))

    def shorten(self, n):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    def draw(self, screen):
        # 🔥 ВЕСЬ змейка одного цвета
        for seg in self.body:
            pygame.draw.rect(
                screen,
                self.color,
                (seg.x * CELL, seg.y * CELL, CELL, CELL)
            )


# ---------------- FOOD ----------------
class Food:
    def __init__(self, snake, obstacles, extra=None):
        self.pos = random_free(snake, obstacles, extra)
        self.weight = random.choice([1, 2, 3])
        self.spawn = pygame.time.get_ticks()
        self.life = 5000

    def expired(self):
        return pygame.time.get_ticks() - self.spawn > self.life

    def draw(self, screen):
        color = GREEN if self.weight == 1 else ORANGE if self.weight == 2 else PURPLE
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


# ---------------- POISON ----------------
class Poison:
    def __init__(self, snake, obstacles, extra=None):
        self.pos = random_free(snake, obstacles, extra)
        self.spawn = pygame.time.get_ticks()
        self.life = 6000

    def expired(self):
        return pygame.time.get_ticks() - self.spawn > self.life

    def draw(self, screen):
        pygame.draw.rect(screen, DARK_RED,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


# ---------------- POWERUP ----------------
class PowerUp:
    def __init__(self):
        self.active = False
        self.kind = None
        self.pos = None
        self.spawn = 0
        self.life = 8000

    def spawn_power(self, snake, obstacles, extra):
        if self.active:
            return

        self.kind = random.choice(["speed", "slow", "shield"])
        self.pos = random_free(snake, obstacles, extra)
        self.spawn = pygame.time.get_ticks()
        self.active = True

    def expired(self):
        return self.active and pygame.time.get_ticks() - self.spawn > self.life

    def collect(self):
        self.active = False
        return self.kind

    def draw(self, screen):
        if not self.active:
            return

        color = BLUE if self.kind == "speed" else PURPLE if self.kind == "slow" else ORANGE
        pygame.draw.rect(screen, color,
                         (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))


# ---------------- MAIN GAME ----------------
def run_game(screen, username, settings):
    if settings.get("sound", True):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # loop
    else:
        pygame.mixer.music.stop()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Verdana", 18)

    snake = Snake(tuple(settings.get("snake_color",[255, 182, 193])))
    best = get_personal_best(username)

    obstacles = []
    food = Food(snake, obstacles)
    poison = Poison(snake, obstacles, [food.pos])
    power = PowerUp()

    active_power = None
    power_end = 0

    running = True

    while running:
        now = pygame.time.get_ticks()

        speed = 6 + snake.level

        # power logic
        if active_power == "speed":
            speed += 4
            if now > power_end:
                active_power = None

        elif active_power == "slow":
            speed = max(3, speed - 3)
            if now > power_end:
                active_power = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and snake.dx != -1:
            snake.dx, snake.dy = 1, 0
        if keys[pygame.K_LEFT] and snake.dx != 1:
            snake.dx, snake.dy = -1, 0
        if keys[pygame.K_UP] and snake.dy != 1:
            snake.dx, snake.dy = 0, -1
        if keys[pygame.K_DOWN] and snake.dy != -1:
            snake.dx, snake.dy = 0, 1

        snake.move()

        if snake.collision():
            if snake.shield:
                snake.shield = False
            else:
                break

        head = snake.body[0]

        # food
        if same(head, food.pos):
            snake.grow()
            snake.score += food.weight
            food = Food(snake, obstacles, [poison.pos])

        if food.expired():
            food = Food(snake, obstacles, [poison.pos])

        # poison
        if same(head, poison.pos):
            snake.shorten(2)
            if len(snake.body) <= 1:
                break
            poison = Poison(snake, obstacles, [food.pos])

        if poison.expired():
            poison = Poison(snake, obstacles, [food.pos])

        # power
        if not power.active and now % 9000 < 20:
            power.spawn_power(snake, obstacles, [food.pos, poison.pos])

        if power.expired():
            power.active = False

        if power.active and same(head, power.pos):
            kind = power.collect()

            if kind == "speed":
                active_power = "speed"
                power_end = now + 5000
            elif kind == "slow":
                active_power = "slow"
                power_end = now + 5000
            else:
                snake.shield = True

        # draw
        screen.fill(WHITE)

        snake.draw(screen)
        food.draw(screen)
        poison.draw(screen)
        power.draw(screen)

        screen.blit(font.render(f"Score: {snake.score}", True, BLACK), (10, 10))
        screen.blit(font.render(f"Level: {snake.level}", True, BLACK), (10, 30))
        screen.blit(font.render(f"Best: {best}", True, BLACK), (10, 50))

        if settings.get("grid"):
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(screen, (230, 230, 230), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL):
                pygame.draw.line(screen, (230, 230, 230), (0, y), (WIDTH, y))

        pygame.display.flip()
        clock.tick(speed)

    save_result(username, snake.score, snake.level)

    return "game_over", {
        "score": snake.score,
        "level": snake.level,
        "best": max(best, snake.score)
    }