import pygame
import random
import sys

pygame.init()

# Размер окна
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

clock = pygame.time.Clock()

# Загружаем изображения
import os  # ← добавь в начале файла

base_path = os.path.dirname(__file__)

player_img = pygame.image.load(os.path.join(base_path, "Player.png"))
enemy_img = pygame.image.load(os.path.join(base_path, "Enemy.png"))
coin_img = pygame.image.load(os.path.join(base_path, "Coin.png"))

coin_img = pygame.transform.scale(coin_img, (32, 32))

# Позиция игрока
player_x = WIDTH // 2 - 25
player_y = HEIGHT - 100
player_speed = 6

# Враг
enemy_x = random.randint(50, WIDTH - 50)
enemy_y = -100
enemy_speed = 5

# Монета
coin_x = random.randint(50, WIDTH - 50)
coin_y = -200
coin_speed = 4

# Счет
score = 0
font = pygame.font.SysFont(None, 30)

running = True

while running:
    screen.fill((40, 40, 40))  # фон

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Ограничение движения
    player_x = max(0, min(WIDTH - player_img.get_width(), player_x))

    # Движение врага
    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_y = -100
        enemy_x = random.randint(50, WIDTH - 50)

    # Движение монеты
    coin_y += coin_speed
    if coin_y > HEIGHT:
        coin_y = -200
        coin_x = random.randint(50, WIDTH - 50)

    # Отрисовка объектов
    screen.blit(player_img, (player_x, player_y))
    screen.blit(enemy_img, (enemy_x, enemy_y))
    screen.blit(coin_img, (coin_x, coin_y))

    # Прямоугольники для столкновений
    player_rect = player_img.get_rect(topleft=(player_x, player_y))
    enemy_rect = enemy_img.get_rect(topleft=(enemy_x, enemy_y))
    coin_rect = coin_img.get_rect(topleft=(coin_x, coin_y))

    # Столкновение с врагом
    if player_rect.colliderect(enemy_rect):
        print("GAME OVER")
        pygame.quit()
        sys.exit()

    # Подбор монеты
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_y = -200
        coin_x = random.randint(50, WIDTH - 50)

    # Отображение счета (правый верх)
    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(60)