
import pygame
import random
import sys
import os

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
FPS = 12

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
DARK_GREEN = (0, 100, 0)
RED = (200, 0, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)
GRAY = (40, 40, 40)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Advanced Edition")

# Set icon
try:
    icon = pygame.image.load(os.path.join("assets", "icon.png"))
    pygame.display.set_icon(icon)
except:
    print("icon.png not found.")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 28, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)

# Load assets
def load_image(name, fallback_color):
    try:
        img = pygame.image.load(os.path.join("assets", name))
        return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
    except:
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
        surface.fill(fallback_color)
        return surface

apple_img = load_image("apple.png", RED)
golden_img = load_image("golden_apple.png", GOLD)
trap_img = load_image("trap.png", GRAY)

# Sounds
try:
    eat_sound = pygame.mixer.Sound(os.path.join("assets", "eat.wav"))
    gameover_sound = pygame.mixer.Sound(os.path.join("assets", "gameover.wav"))
except:
    eat_sound = gameover_sound = None

def play_sound(s):
    if s:
        s.play()

# Score tracking
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Drawing
def draw_text_center(text, font, color, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH//2, y))
    screen.blit(surface, rect)

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, DARK_GREEN, (*segment, CELL_SIZE, CELL_SIZE))

def generate_item(snake, items):
    while True:
        x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x, y) not in snake and (x, y) not in items:
            return (x, y)

def start_screen():
    screen.fill(BLACK)
    draw_text_center("SNAKE: Advanced Edition", big_font, GREEN, HEIGHT // 3)
    draw_text_center("Press ENTER to Play", font, WHITE, HEIGHT // 2)
    draw_text_center("Press ESC to Quit", font, GRAY, HEIGHT // 2 + 40)
    pygame.display.update()
    wait_for_start()

def wait_for_start():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over(score, high_score):
    screen.fill(BLACK)
    draw_text_center("GAME OVER", big_font, RED, HEIGHT // 3)
    draw_text_center(f"Your Score: {score}", font, WHITE, HEIGHT // 2)
    draw_text_center(f"High Score: {high_score}", font, GOLD, HEIGHT // 2 + 40)
    draw_text_center("Press ENTER to Play Again", font, WHITE, HEIGHT - 80)
    pygame.display.update()
    wait_for_start()

def main():
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    food = generate_item(snake, [])
    golden_food = None
    trap = None
    score = 0
    high_score = load_high_score()
    golden_timer = 0

    running = True
    while running:
        clock.tick(FPS + score // 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(max(score, high_score))
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)

        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_head in snake or
            new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head == trap):
            play_sound(gameover_sound)
            save_high_score(max(score, high_score))
            game_over(score, max(score, high_score))
            return main()

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = generate_item(snake, [golden_food, trap])
            play_sound(eat_sound)

            if score % 5 == 0 and golden_food is None:
                golden_food = generate_item(snake, [food, trap])
            if score % 4 == 0 and trap is None:
                trap = generate_item(snake, [food, golden_food])
        elif golden_food and new_head == golden_food:
            score += 5
            golden_food = None
            play_sound(eat_sound)
        else:
            snake.pop()

        screen.fill((10, 10, 30))
        draw_snake(snake)
        screen.blit(apple_img, food)
        if golden_food:
            screen.blit(golden_img, golden_food)
        if trap:
            screen.blit(trap_img, trap)

        draw_text_center(f"Score: {score}", font, WHITE, 20)
        draw_text_center(f"High Score: {max(score, high_score)}", font, GOLD, 50)
        pygame.display.update()

if __name__ == "__main__":
    start_screen()
    main()
