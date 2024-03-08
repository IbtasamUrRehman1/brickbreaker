import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (3, 62, 156)
BLACK = (0, 0, 0)

# Brick settings
brick_width, brick_height = 100, 20
brick_cols, brick_rows = 8, 5
brick_spacing = 10

# Player settings
player_width, player_height = 100, 20
player_x, player_y = (WIDTH - player_width) // 2, HEIGHT - player_height - 20
player_speed = 5

# Ball settings
ball_radius, ball_speed = 10, 5
ball_direction = random.choice([(-1, -1), (1, -1)])

# Create bricks
bricks = [
    pygame.Rect(col * (brick_width + brick_spacing), row * (brick_height + brick_spacing), brick_width, brick_height)
    for row in range(brick_rows) for col in range(brick_cols)]

total_bricks, bricks_broken = len(bricks), 0

# Create player
player = pygame.Rect(player_x, player_y, player_width, player_height)

# Create ball
ball_x, ball_y = WIDTH // 2, player_y - ball_radius

# Play button
play_button_rect = pygame.Rect((WIDTH - 200) // 2, (HEIGHT - 50) // 2, 200, 50)

# Font
font = pygame.font.Font(None, 36)

# Clock
clock = pygame.time.Clock()

# Game state
game_state = "start"  # Possible states: "start", "playing", "game_over"

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == "start" and play_button_rect.collidepoint(event.pos):
                game_state = "playing"
            elif game_state == "game_over" and play_button_rect.collidepoint(event.pos):
                # Reset game state
                game_state = "playing"
                bricks = [
                    pygame.Rect(col * (brick_width + brick_spacing), row * (brick_height + brick_spacing), brick_width,
                                brick_height)
                    for row in range(brick_rows) for col in range(brick_cols)]
                total_bricks, bricks_broken = len(bricks), 0
                player.x, ball_x, ball_y = (WIDTH - player_width) // 2, WIDTH // 2, player_y - ball_radius
                ball_direction = random.choice([(-1, -1), (1, -1)])

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        player.x = max(0, min(WIDTH - player_width,
                              player.x - keys[pygame.K_LEFT] * player_speed + keys[pygame.K_RIGHT] * player_speed))

        ball_x += ball_speed * ball_direction[0]
        ball_y += ball_speed * ball_direction[1]

        if player.colliderect((ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
            ball_direction = (ball_direction[0], -ball_direction[1])

        for brick in bricks[:]:
            if brick.colliderect((ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)):
                bricks.remove(brick)
                bricks_broken += 1
                ball_direction = (ball_direction[0], -ball_direction[1])

        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_direction = (-ball_direction[0], ball_direction[1])
        if ball_y <= ball_radius:
            ball_direction = (ball_direction[0], -ball_direction[1])

        if ball_y >= HEIGHT:
            game_state = "game_over"

        win.fill(WHITE)
        [pygame.draw.rect(win, BLUE, brick) for brick in bricks]
        pygame.draw.rect(win, RED, player)
        pygame.draw.circle(win, RED, (ball_x, ball_y), ball_radius)
        bricks_broken_text = font.render("Bricks Broken: {}".format(bricks_broken), True, BLACK)
        win.blit(bricks_broken_text, ((WIDTH - bricks_broken_text.get_width()) // 2, play_button_rect.bottom + 10))

    elif game_state == "start":
        pygame.draw.rect(win, BLACK, play_button_rect)
        play_text = font.render("Play", True, WHITE)
        win.blit(play_text, ((WIDTH - play_text.get_width()) // 2, (HEIGHT - play_text.get_height()) // 2))

    elif game_state == "game_over":
        game_over_text = font.render("Game Over", True, BLACK)
        win.blit(game_over_text,
                 ((WIDTH - game_over_text.get_width()) // 2, (HEIGHT - game_over_text.get_height()) // 2))
        pygame.draw.rect(win, BLACK, play_button_rect)
        play_text = font.render("Play Again", True, WHITE)
        win.blit(play_text, ((WIDTH - play_text.get_width()) // 2, (HEIGHT - play_text.get_height()) // 2))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
