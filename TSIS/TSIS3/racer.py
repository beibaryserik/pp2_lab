import pygame
import random
import os

# ---------------- GAME OVER ----------------
def game_over_screen(screen, score):
    font_big = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 35)

    while True:
        screen.fill((30, 30, 30))

        title = font_big.render("GAME OVER", True, (255, 0, 0))
        screen.blit(title, (70, 150))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (140, 250))

        retry_rect = pygame.Rect(120, 320, 160, 50)
        menu_rect = pygame.Rect(120, 390, 160, 50)

        pygame.draw.rect(screen, (255,255,255), retry_rect, 2)
        pygame.draw.rect(screen, (255,255,255), menu_rect, 2)

        screen.blit(font.render("Retry", True, (255,255,255)), (150, 335))
        screen.blit(font.render("Menu", True, (255,255,255)), (150, 405))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return "menu"
            if e.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(e.pos):
                    return "retry"
                if menu_rect.collidepoint(e.pos):
                    return "menu"


# ---------------- ИГРА ----------------
def run_game(screen, settings):

    WIDTH, HEIGHT = 400, 600
    clock = pygame.time.Clock()

    BASE = os.path.dirname(__file__)
    ASSETS = os.path.join(BASE, "assets")

    # ----------- ВЫБОР МАШИНЫ -----------
    color = settings["car_color"]

    if color == "green":
        player = pygame.image.load(os.path.join(ASSETS, "greenplayer.png"))
    elif color == "yellow":
        player = pygame.image.load(os.path.join(ASSETS, "yellplayer.png"))
    else:
        player = pygame.image.load(os.path.join(ASSETS, "bluePlayer.png"))

    # ----------- ЗАГРУЗКА -----------
    enemy = pygame.image.load(os.path.join(ASSETS, "Enemy.png"))
    coin = pygame.image.load(os.path.join(ASSETS, "coin1.png"))  # 🔥 НОВАЯ МОНЕТА
    nitro_img = pygame.image.load(os.path.join(ASSETS, "nitro.png"))
    shield_img = pygame.image.load(os.path.join(ASSETS, "shield.png"))

    # размеры
    player = pygame.transform.scale(player, (50, 80))
    enemy = pygame.transform.scale(enemy, (50, 80))
    coin = pygame.transform.scale(coin, (32, 32))  # 🔥 32x32
    nitro_img = pygame.transform.scale(nitro_img, (32, 32))
    shield_img = pygame.transform.scale(shield_img, (32, 32))

    player = pygame.transform.rotate(player, 180)

    # ----------- СЛОЖНОСТЬ -----------
    difficulty = settings["difficulty"]

    if difficulty == "easy":
        base_speed = 3
        spawn_delay = 70
    elif difficulty == "hard":
        base_speed = 7
        spawn_delay = 30
    else:
        base_speed = 5
        spawn_delay = 50

    # ----------- ЗВУК -----------
    if settings["sound"]:
        pygame.mixer.music.load(os.path.join(ASSETS, "background (1).wav"))
        pygame.mixer.music.play(-1)

    crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash (1).wav"))

    # ----------- ПЕРЕМЕННЫЕ -----------
    px, py = WIDTH // 2, HEIGHT - 100

    enemies = []
    coins = []
    nitros = []
    shields = []

    score = 0

    nitro_active = False
    nitro_timer = 0
    shield = False

    spawn_timer = 0

    # ----------- ЦИКЛ -----------
    while True:
        screen.fill((40, 40, 40))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if settings["sound"]:
                    pygame.mixer.music.stop()
                return score

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            px -= 6
        if keys[pygame.K_RIGHT]:
            px += 6

        px = max(0, min(WIDTH - 50, px))

        # сложность растёт от очков
        enemy_speed = base_speed + score * 0.2

        # нитро
        if nitro_active:
            speed = enemy_speed * 1.3
            if pygame.time.get_ticks() - nitro_timer > 4000:
                nitro_active = False
        else:
            speed = enemy_speed

        # спавн
        spawn_timer += 1
        if spawn_timer > max(15, spawn_delay - score):

            enemies.append([random.randint(0, WIDTH - 50), -80])
            coins.append([random.randint(0, WIDTH - 32), -32])

            if random.random() < 0.15:
                nitros.append([random.randint(0, WIDTH - 32), -32])

            if random.random() < 0.1:
                shields.append([random.randint(0, WIDTH - 32), -32])

            spawn_timer = 0

        player_rect = pygame.Rect(px, py, 50, 80)

        # ----------- ВРАГИ -----------
        for e in enemies[:]:
            e[1] += speed
            screen.blit(enemy, e)

            if player_rect.colliderect(pygame.Rect(e[0], e[1], 50, 80)):
                if shield:
                    shield = False
                    enemies.remove(e)
                else:
                    if settings["sound"]:
                        crash_sound.play()
                        pygame.mixer.music.stop()

                    pygame.time.delay(300)

                    choice = game_over_screen(screen, score)

                    if choice == "retry":
                        return run_game(screen, settings)
                    else:
                        return score

        # ----------- МОНЕТЫ -----------
        for c in coins[:]:
            c[1] += 4
            screen.blit(coin, c)

            if player_rect.colliderect(pygame.Rect(c[0], c[1], 32, 32)):
                score += 1
                coins.remove(c)

        # ----------- НИТРО -----------
        for n in nitros[:]:
            n[1] += 4
            screen.blit(nitro_img, n)

            if player_rect.colliderect(pygame.Rect(n[0], n[1], 32, 32)):
                nitro_active = True
                nitro_timer = pygame.time.get_ticks()
                nitros.remove(n)

        # ----------- ЩИТ -----------
        for s in shields[:]:
            s[1] += 4
            screen.blit(shield_img, s)

            if player_rect.colliderect(pygame.Rect(s[0], s[1], 32, 32)):
                shield = True
                shields.remove(s)

        # игрок
        screen.blit(player, (px, py))

        # UI
        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))

        if shield:
            screen.blit(font.render("Shield", True, (0,255,255)), (10,40))

        if nitro_active:
            screen.blit(font.render("Nitro", True, (255,255,0)), (10,70))

        pygame.display.update()
        clock.tick(60)