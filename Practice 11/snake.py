import pygame
import random
import sys

pygame.init()

# Setup screen and variables
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

font = pygame.font.SysFont("Verdana", 20)

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"

    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "RIGHT":
            head_x += BLOCK_SIZE
        elif self.direction == "LEFT":
            head_x -= BLOCK_SIZE
        elif self.direction == "UP":
            head_y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            head_y += BLOCK_SIZE
            
        self.body.insert(0, (head_x, head_y))
        self.body.pop() # Remove tail

    def grow(self):
        # Add a dummy block, it will be placed correctly on the next move
        self.body.append(self.body[-1])

    def draw(self):
        for block in self.body:
            pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    def check_collision(self):
        head = self.body[0]
        # Wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            return True
        # Self collision
        if head in self.body[1:]:
            return True
        return False

class Food:
    def __init__(self):
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000 # Food disappears after 5 seconds

    def update_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.randomize()

    def draw(self):
        if self.weight == 3:
            color = GOLD
        elif self.weight == 2:
            color = WHITE
        else:
            color = RED
        pygame.draw.rect(screen, color, (self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

snake = Snake()
food = Food()
score = 0

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != "DOWN":
                snake.direction = "UP"
            elif event.key == pygame.K_DOWN and snake.direction != "UP":
                snake.direction = "DOWN"
            elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                snake.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                snake.direction = "RIGHT"

    snake.move()
    
    # Check if snake eats food
    if snake.body[0] == (food.x, food.y):
        score += food.weight
        snake.grow()
        food.randomize()

    if snake.check_collision():
        pygame.quit()
        sys.exit()

    food.update_timer()

    # Drawing
    screen.fill(BLACK)
    snake.draw()
    food.draw()
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(10) # Snake speed