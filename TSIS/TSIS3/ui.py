import pygame
from persistence import load_scores, load_settings, save_settings

def draw_text(screen, text, size, x, y, color=(255,255,255)):
    font = pygame.font.SysFont(None, size)
    screen.blit(font.render(text, True, color), (x,y))


def main_menu(screen):
    while True:
        screen.fill((0,0,0))

        draw_text(screen, "RACER", 60, 130, 100)
        draw_text(screen, "1 - Play", 30, 150, 200)
        draw_text(screen, "2 - Leaderboard", 30, 150, 250)
        draw_text(screen, "3 - Settings", 30, 150, 300)
        draw_text(screen, "4 - Quit", 30, 150, 350)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_1: return "play"
                if e.key == pygame.K_2: return "leaderboard"
                if e.key == pygame.K_3: return "settings"
                if e.key == pygame.K_4: return "quit"


def get_username(screen):
    font = pygame.font.SysFont(None, 40)
    name = ""

    while True:
        screen.fill((0,0,0))
        draw_text(screen, "Enter name:", 40, 120, 150)
        draw_text(screen, name, 40, 120, 220, (0,255,0))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "Player"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return name if name else "Player"
                elif e.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += e.unicode


def leaderboard_screen(screen):
    scores = load_scores()

    while True:
        screen.fill((0,0,0))

        draw_text(screen, "TOP 10", 50, 140, 50)

        y = 120
        for i, s in enumerate(scores):
            text = f"{i+1}. {s['name']} {s['score']} pts"
            draw_text(screen, text, 30, 60, y)
            y += 30

        draw_text(screen, "ESC - Back", 25, 120, 550)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return


def settings_screen(screen):
    settings = load_settings()
    options = ["sound", "car_color", "difficulty", "back"]
    selected = 0

    colors = ["blue", "green", "yellow"]
    difficulties = ["easy", "normal", "hard"]

    while True:
        screen.fill((20,20,20))

        draw_text(screen, "SETTINGS", 50, 110, 50)

        for i, opt in enumerate(options):
            col = (0,255,0) if i == selected else (255,255,255)

            if opt == "sound":
                text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
            elif opt == "car_color":
                text = f"Car: {settings['car_color']}"
            elif opt == "difficulty":
                text = f"Difficulty: {settings['difficulty']}"
            else:
                text = "Back"

            draw_text(screen, text, 30, 100, 150+i*50, col)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:

                if e.key == pygame.K_UP:
                    selected = (selected-1)%4
                if e.key == pygame.K_DOWN:
                    selected = (selected+1)%4

                if e.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    if options[selected] == "sound":
                        settings["sound"] = not settings["sound"]

                    elif options[selected] == "car_color":
                        i = colors.index(settings["car_color"])
                        settings["car_color"] = colors[(i+1)%3]

                    elif options[selected] == "difficulty":
                        i = difficulties.index(settings["difficulty"])
                        settings["difficulty"] = difficulties[(i+1)%3]

                if e.key == pygame.K_RETURN:
                    if options[selected] == "back":
                        save_settings(settings)
                        return


def game_over_screen(screen, score, distance):
    while True:
        screen.fill((0,0,0))

        draw_text(screen, "GAME OVER", 50, 110, 150, (255,0,0))
        draw_text(screen, f"Score: {score}", 30, 130, 230)
        draw_text(screen, "R - Retry", 30, 130, 300)
        draw_text(screen, "ESC - Menu", 30, 110, 350)

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return "retry"
                if e.key == pygame.K_ESCAPE:
                    return "menu"