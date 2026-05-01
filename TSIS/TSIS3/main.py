import pygame
import json
import os
from racer import run_game

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

FONT = pygame.font.SysFont(None, 40)

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


# ---------- SETTINGS ----------
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default = {
            "sound": True,
            "car_color": "blue"
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default

    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
    except:
        settings = {}

    settings.setdefault("sound", True)
    settings.setdefault("car_color", "blue")

    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


# ---------- LEADERBOARD ----------
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []

    try:
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- NAME INPUT ----------
def name_input():
    name = ""
    settings = load_settings()

    while True:
        screen.fill((30, 30, 30))

        text = FONT.render("Enter Name:", True, (255,255,255))
        name_text = FONT.render(name, True, (0,255,0))

        screen.blit(text, (120, 200))
        screen.blit(name_text, (120, 260))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN and name != "":
                    score = run_game(screen, settings)

                    lb = load_leaderboard()
                    lb.append({"name": name, "score": score})
                    lb = sorted(lb, key=lambda x: x["score"], reverse=True)[:10]
                    save_leaderboard(lb)
                    return

                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += e.unicode


# ---------- SETTINGS MENU ----------
def settings_menu():
    settings = load_settings()

    while True:
        screen.fill((30, 30, 30))

        screen.blit(FONT.render("SETTINGS", True, (255,255,255)), (120, 100))
        screen.blit(FONT.render(f"Car: {settings['car_color']}", True, (255,255,255)), (100, 200))
        screen.blit(FONT.render(f"Sound: {settings['sound']}", True, (255,255,255)), (100, 260))

        screen.blit(FONT.render("C - Change Car", True, (200,200,200)), (80, 350))
        screen.blit(FONT.render("S - Toggle Sound", True, (200,200,200)), (60, 400))
        screen.blit(FONT.render("ESC - Back", True, (200,200,200)), (120, 460))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return

                if e.key == pygame.K_c:
                    if settings["car_color"] == "blue":
                        settings["car_color"] = "green"
                    elif settings["car_color"] == "green":
                        settings["car_color"] = "yellow"
                    else:
                        settings["car_color"] = "blue"

                if e.key == pygame.K_s:
                    settings["sound"] = not settings["sound"]


# ---------- LEADERBOARD SCREEN ----------
def leaderboard_screen():
    data = load_leaderboard()

    while True:
        screen.fill((30,30,30))

        screen.blit(FONT.render("LEADERBOARD", True, (255,255,255)), (80, 100))

        y = 180
        for entry in data:
            text = f"{entry['name']} - {entry['score']}"
            screen.blit(FONT.render(text, True, (255,255,255)), (80, y))
            y += 40

        screen.blit(FONT.render("ESC - Back", True, (200,200,200)), (120, 500))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return


# ---------- MAIN MENU ----------
def main_menu():

    while True:
        screen.fill((30, 30, 30))

        screen.blit(FONT.render("RACER GAME", True, (255,255,255)), (90, 120))
        screen.blit(FONT.render("1 - Play", True, (255,255,255)), (120, 220))
        screen.blit(FONT.render("2 - Settings", True, (255,255,255)), (100, 280))
        screen.blit(FONT.render("3 - Leaderboard", True, (255,255,255)), (80, 340))
        screen.blit(FONT.render("ESC - Exit", True, (255,255,255)), (100, 420))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_1:
                    name_input()

                if e.key == pygame.K_2:
                    settings_menu()

                if e.key == pygame.K_3:
                    leaderboard_screen()

                if e.key == pygame.K_ESCAPE:
                    return


# ---------- START ----------
main_menu()
pygame.quit()