import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('🐍 Snake Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 25)

# Snake and food functions
def draw_snake(snake_blocks):
    for block in snake_blocks:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], CELL_SIZE, CELL_SIZE])

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE])

def show_score(score):
    value = font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])

# Game loop
def game_loop():
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_blocks = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
    food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            msg = font.render("Game Over! Press R to Restart or Q to Quit", True, RED)
            screen.blit(msg, [WIDTH // 6, HEIGHT // 3])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = CELL_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -CELL_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = CELL_SIZE
                    x_change = 0

        x += x_change
        y += y_change

        # Collision with walls
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)
        draw_food((food_x, food_y))

        snake_head = [x, y]
        snake_blocks.append(snake_head)

        if len(snake_blocks) > snake_length:
            del snake_blocks[0]

        # Collision with self
        for block in snake_blocks[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_blocks)
        show_score(snake_length - 1)

        pygame.display.update()

        # Collision with food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            food_y = round(random.randrange(0, HEIGHT - CELL_SIZE) / CELL_SIZE) * CELL_SIZE
            snake_length += 1

        clock.tick(10)  # Speed of the game

    pygame.quit()
    quit()

# Start the game
game_loop()