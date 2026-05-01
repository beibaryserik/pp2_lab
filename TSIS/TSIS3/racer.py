import pygame
import random
import os

def load_trimmed(path):
    img = pygame.image.load(path).convert_alpha()
    rect = img.get_bounding_rect()
    return img.subsurface(rect)

# ---------- GAME OVER ----------
def game_over_screen(screen, score):
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 35)

    while True:
        screen.fill((30, 30, 30))

        screen.blit(font_big.render("GAME OVER", True, (255,0,0)), (70,150))
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (140,250))

        retry = pygame.Rect(120,320,160,50)
        menu = pygame.Rect(120,390,160,50)

        pygame.draw.rect(screen, (255,255,255), retry, 2)
        pygame.draw.rect(screen, (255,255,255), menu, 2)

        screen.blit(font.render("Retry", True, (255,255,255)), (150,335))
        screen.blit(font.render("Menu", True, (255,255,255)), (150,405))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(e.pos):
                    return "retry"
                if menu.collidepoint(e.pos):
                    return "menu"


# ---------- MAIN GAME ----------
def run_game(screen, settings):

    WIDTH, HEIGHT = 400, 600
    clock = pygame.time.Clock()

    BASE = os.path.dirname(__file__)
    ASSETS = os.path.join(BASE, "assets")

    # ---------- ДОРОГА ----------
    road = pygame.image.load(os.path.join(ASSETS, "road.png"))
    road = pygame.transform.scale(road, (WIDTH, HEIGHT))

    y1 = 0
    y2 = -HEIGHT

    # ---------- ИГРОК ----------
    color = settings["car_color"]

    if color == "green":
        player = load_trimmed(os.path.join(ASSETS, "greenplayer.png"))
        player = pygame.transform.scale(player, (50, 80))

    elif color == "yellow":
        player = load_trimmed(os.path.join(ASSETS, "yellplayer.png"))
        player = pygame.transform.scale(player, (50, 80))

    else:
        player = load_trimmed(os.path.join(ASSETS, "bluePlayer.png"))
        player = pygame.transform.scale(player, (50, 80))

    # ---------- ВРАГ ----------
    enemy = pygame.image.load(os.path.join(ASSETS, "Enemy.png")).convert_alpha()
    enemy = pygame.transform.scale(enemy, (50, 80))

    # ---------- ОБЪЕКТЫ ----------
    coin = pygame.image.load(os.path.join(ASSETS, "coin1.png")).convert_alpha()
    coin = pygame.transform.scale(coin, (32,32))

    nitro_img = pygame.image.load(os.path.join(ASSETS, "nitro.png")).convert_alpha()
    nitro_img = pygame.transform.scale(nitro_img, (32,32))

    shield_img = pygame.image.load(os.path.join(ASSETS, "shield.png")).convert_alpha()
    shield_img = pygame.transform.scale(shield_img, (32,32))

    # ---------- ЗВУК ----------
    if settings["sound"]:
        pygame.mixer.music.load(os.path.join(ASSETS, "background (1).wav"))
        pygame.mixer.music.play(-1)

    crash = pygame.mixer.Sound(os.path.join(ASSETS, "crash (1).wav"))

    # ---------- ПЕРЕМЕННЫЕ ----------
    px = WIDTH // 2
    py = HEIGHT - 100

    enemies = []
    coins = []
    nitros = []
    shields = []

    score = 0

    nitro_active = False
    nitro_time = 0
    shield = False

    spawn_timer = 0

    # ---------- GAME LOOP ----------
    while True:

        # 🎯 СКОРОСТЬ С УРОВНЯМИ
        base_speed = 5
        multiplier = 1 + (score // 10) * 0.5
        base_speed *= multiplier

        if nitro_active:
            speed = base_speed * 1.3
            if pygame.time.get_ticks() - nitro_time > 4000:
                nitro_active = False
        else:
            speed = base_speed

        # ---------- ДВИЖЕНИЕ ДОРОГИ ----------
        y1 += speed
        y2 += speed

        if y1 >= HEIGHT:
            y1 = -HEIGHT
        if y2 >= HEIGHT:
            y2 = -HEIGHT

        screen.blit(road, (0, y1))
        screen.blit(road, (0, y2))

        # ---------- EVENTS ----------
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return score

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            px -= 6
        if keys[pygame.K_RIGHT]:
            px += 6

        px = max(0, min(WIDTH - 50, px))

        # ---------- SPAWN ----------
        spawn_timer += 1
        if spawn_timer > max(15, 50 - score):

            enemies.append([random.randint(0, WIDTH-50), -80])
            coins.append([random.randint(0, WIDTH-32), -32])

            if random.random() < 0.15:
                nitros.append([random.randint(0, WIDTH-32), -32])

            if random.random() < 0.1:
                shields.append([random.randint(0, WIDTH-32), -32])

            spawn_timer = 0

        player_rect = pygame.Rect(px, py, 50, 80)

        # ---------- ВРАГИ ----------
        for e in enemies[:]:
            e[1] += speed
            screen.blit(enemy, e)

            if player_rect.colliderect(pygame.Rect(e[0], e[1], 50, 80)):
                if shield:
                    shield = False
                    enemies.remove(e)
                else:
                    crash.play()
                    pygame.mixer.music.stop()
                    pygame.time.delay(300)

                    choice = game_over_screen(screen, score)

                    if choice == "retry":
                        return run_game(screen, settings)
                    else:
                        return score

        # ---------- МОНЕТЫ ----------
        for c in coins[:]:
            c[1] += speed
            screen.blit(coin, c)

            if player_rect.colliderect(pygame.Rect(c[0], c[1], 32, 32)):
                score += 1
                coins.remove(c)

        # ---------- НИТРО ----------
        for n in nitros[:]:
            n[1] += speed
            screen.blit(nitro_img, n)

            if player_rect.colliderect(pygame.Rect(n[0], n[1], 32, 32)):
                nitro_active = True
                nitro_time = pygame.time.get_ticks()
                nitros.remove(n)

        # ---------- ЩИТ ----------
        for s in shields[:]:
            s[1] += speed
            screen.blit(shield_img, s)

            if player_rect.colliderect(pygame.Rect(s[0], s[1], 32, 32)):
                shield = True
                shields.remove(s)

        # ---------- ИГРОК ----------
        screen.blit(player, (px, py))

        # ---------- UI ----------
        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))

        if shield:
            screen.blit(font.render("Shield", True, (0,255,255)), (10,40))

        if nitro_active:
            screen.blit(font.render("Nitro", True, (255,255,0)), (10,70))

        pygame.display.update()
        clock.tick(60)