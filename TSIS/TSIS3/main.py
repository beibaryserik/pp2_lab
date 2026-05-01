import pygame
import sys
import os
from racer import run_game
import json

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 RACER")

FONT = pygame.font.SysFont(None, 40)


# ---------- SETTINGS ----------
def load_settings():
    try:
        with open("settings.json") as f:
            return json.load(f)
    except:
        settings = {
            "sound": True,
            "car_color": "blue",
            "difficulty": "normal"
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)
        return settings


def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)


# ---------- LEADERBOARD ----------
def load_leaderboard():
    try:
        with open("leaderboard.json") as f:
            return json.load(f)
    except:
        return []


def save_leaderboard(data):
    with open("leaderboard.json", "w") as f:
        json.dump(data, f)


# ---------- BUTTON ----------
def draw_button(text, x, y):
    rect = pygame.Rect(x, y, 200, 50)
    pygame.draw.rect(screen, (255,255,255), rect, 2)

    label = FONT.render(text, True, (0,0,0))
    screen.blit(label, (x + 50, y + 10))

    return rect


# ---------- NAME INPUT ----------
def name_input():
    name = ""
    settings = load_settings()

    while True:
        screen.fill((240,240,240))

        title = FONT.render("Enter your name", True, (0,0,0))
        screen.blit(title, (80,200))

        text = FONT.render(name, True, (0,0,255))
        screen.blit(text, (150,260))

        hint = pygame.font.SysFont(None, 25).render("Press ENTER to start", True, (100,100,100))
        screen.blit(hint, (110,320))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
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


# ---------- LEADERBOARD ----------
def leaderboard_screen():
    data = load_leaderboard()

    while True:
        screen.fill((240,240,240))

        title = FONT.render("Leaderboard", True, (0,0,0))
        screen.blit(title, (120,50))

        y = 120
        for i, entry in enumerate(data):
            text = f"{i+1}. {entry['name']} - {entry['score']}"
            screen.blit(FONT.render(text, True, (0,0,0)), (80, y))
            y += 40

        back = draw_button("Back", 100, 500)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(e.pos):
                    return


# ---------- SETTINGS ----------
def settings_menu():
    settings = load_settings()

    while True:
        screen.fill((240,240,240))

        title = FONT.render("Settings", True, (0,0,0))
        screen.blit(title, (130,80))

        sound_btn = draw_button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 100, 180)
        color_btn = draw_button(f"Car: {settings['car_color']}", 100, 250)
        diff_btn = draw_button(f"Difficulty: {settings['difficulty']}", 100, 320)
        back_btn = draw_button("Back", 100, 420)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if sound_btn.collidepoint(e.pos):
                    settings["sound"] = not settings["sound"]

                elif color_btn.collidepoint(e.pos):
                    colors = ["blue", "green", "yellow"]
                    i = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(i + 1) % 3]

                elif diff_btn.collidepoint(e.pos):
                    diffs = ["easy", "normal", "hard"]
                    i = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(i + 1) % 3]

                elif back_btn.collidepoint(e.pos):
                    save_settings(settings)
                    return


# ---------- MAIN MENU ----------
def main_menu():
    while True:
        screen.fill((240,240,240))

        title = FONT.render("TSIS3 RACER", True, (0,0,0))
        screen.blit(title, (90,100))

        play = draw_button("Play", 100, 200)
        lb = draw_button("Leaderboard", 100, 270)
        settings_btn = draw_button("Settings", 100, 340)
        quit_btn = draw_button("Quit", 100, 410)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(e.pos):
                    name_input()

                elif lb.collidepoint(e.pos):
                    leaderboard_screen()

                elif settings_btn.collidepoint(e.pos):
                    settings_menu()

                elif quit_btn.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()


# ---------- START ----------
main_menu()