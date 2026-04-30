import pygame
import sys
import json
import os
from racer import run_game

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 RACER")

font_big = pygame.font.SysFont(None, 50)
font = pygame.font.SysFont(None, 35)

BASE = os.path.dirname(__file__)
SETTINGS_PATH = os.path.join(BASE, "settings.json")
LEADER_PATH = os.path.join(BASE, "leaderboard.json")

# ---------------- SETTINGS ----------------
def load_settings():
    if not os.path.exists(SETTINGS_PATH):
        default = {
            "sound": True,
            "difficulty": "normal",
            "car_color": "blue"
        }
        with open(SETTINGS_PATH, "w") as f:
            json.dump(default, f, indent=4)
        return default

    with open(SETTINGS_PATH) as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- LEADERBOARD ----------------
def save_score(name, score):
    if not os.path.exists(LEADER_PATH):
        data = []
    else:
        with open(LEADER_PATH) as f:
            data = json.load(f)

    data.append({"name": name, "score": score})
    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADER_PATH, "w") as f:
        json.dump(data, f, indent=4)

def show_leaderboard():
    if not os.path.exists(LEADER_PATH):
        data = []
    else:
        with open(LEADER_PATH) as f:
            data = json.load(f)

    while True:
        screen.fill((255,255,255))

        title = font_big.render("Leaderboard", True, (0,0,0))
        screen.blit(title, (80, 80))

        y = 150
        for i, entry in enumerate(data):
            txt = font.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (0,0,0))
            screen.blit(txt, (60, y))
            y += 30

        back = draw_button("Back", 120, 500, 160, 40)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(e.pos):
                    return

# ---------------- BUTTON ----------------
def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, (0,0,0), rect, 2)

    txt = font.render(text, True, (0,0,0))
    screen.blit(txt, (x + 20, y + 10))
    return rect

# ---------------- NAME INPUT ----------------
def name_input():
    name = ""

    while True:
        screen.fill((255,255,255))

        screen.blit(font_big.render("Enter your name", True, (0,0,0)), (60,150))
        screen.blit(font.render(name, True, (0,0,0)), (180,250))
        screen.blit(pygame.font.SysFont(None,25).render("Press ENTER to start", True, (100,100,100)), (110,300))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    settings = load_settings()

                    score = run_game(screen, settings)

                    save_score(name if name else "Player", score)

                    return

                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode

# ---------------- SETTINGS ----------------
def settings_menu():
    settings = load_settings()

    while True:
        screen.fill((255,255,255))

        screen.blit(font_big.render("Settings", True, (0,0,0)), (120,100))

        sound_btn = draw_button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 80,200,240,50)
        car_btn = draw_button(f"Car: {settings['car_color']}", 80,270,240,50)
        diff_btn = draw_button(f"Difficulty: {settings['difficulty']}", 80,340,240,50)
        back_btn = draw_button("Back", 120,450,160,50)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(e.pos):
                    settings["sound"] = not settings["sound"]

                if car_btn.collidepoint(e.pos):
                    colors = ["blue", "green", "yellow"]
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i+1)%3]

                if diff_btn.collidepoint(e.pos):
                    diffs = ["easy","normal","hard"]
                    i = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(i+1)%3]

                if back_btn.collidepoint(e.pos):
                    save_settings(settings)
                    return

# ---------------- MAIN MENU ----------------
def main_menu():
    while True:
        screen.fill((255,255,255))

        screen.blit(font_big.render("TSIS3 RACER", True, (0,0,0)), (70,100))

        play = draw_button("Play", 120,200,160,40)
        lb = draw_button("Leaderboard", 120,260,160,40)
        sett = draw_button("Settings", 120,320,160,40)
        quitb = draw_button("Quit", 120,380,160,40)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(e.pos):
                    name_input()

                if lb.collidepoint(e.pos):
                    show_leaderboard()

                if sett.collidepoint(e.pos):
                    settings_menu()

                if quitb.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()

# ---------------- START ----------------
main_menu()