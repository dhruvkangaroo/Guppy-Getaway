import pygame
from spritesheet import SpriteSheet
from sys import exit
import math
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
GUPPY_WIDTH = 96
GUPPY_HEIGHT = 96
GUPPY_ANIMATION_STEPS = 8
GUPPY_ANIMATION_COOLDOWN = 50
START_SPEED = 7
MAX_SPEED = 5
TILE_SIZE = 275
SCROLL_SPEED = 10
FISH_BOBBING_AMPLITUDE = 5
OBSTACLE_BOBBING_AMPLITUDE = 1
BOBBING_SPEED = 0.3

# Initialize Pygame and Display
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guppy Getaway")
icon = pygame.image.load("Project\Assets\Icon.png")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

# Load assets
guppy_image = pygame.image.load("Project\Assets\Guppy-1-Sheet.png").convert_alpha()
water_background = pygame.transform.scale(pygame.image.load("Project\Assets\Water.png"), (TILE_SIZE, TILE_SIZE))
mine_image = pygame.transform.scale(pygame.image.load("Project\Assets\Mine.png"), (120, 120))
plant_image = pygame.transform.scale(pygame.image.load("Project\Assets\Anubias.png"), (80, 80))
spritesheet = SpriteSheet(guppy_image)

# Animation frames
animation_list = [spritesheet.get_guppy(x, 24, 24, 4) for x in range(GUPPY_ANIMATION_STEPS)]
frame = 0
last_update = pygame.time.get_ticks()

# Music
pygame.mixer.music.load("Project\Assets\guppy_getaway_music.mp3")
pygame.mixer.music.play(-1, 0.0)

# Fonts
font = pygame.font.Font("Project\Assets\Pixel.ttf", 30)
menu_font = pygame.font.Font("Project\Assets\Pixel.ttf", 50)

def draw_background():
    global scroll_y
    scroll_y += SCROLL_SPEED
    if scroll_y >= TILE_SIZE:
        scroll_y = 0
    for y in range(-TILE_SIZE, SCREEN_HEIGHT, TILE_SIZE):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            screen.blit(water_background, (x, y + scroll_y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, hitbox_scale=1.0):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([random.randint(100, SCREEN_WIDTH - self.rect.width - 100),
                                     random.randint(0, 50), random.randint(SCREEN_WIDTH - 50, SCREEN_WIDTH)])
        self.rect.y = random.randint(-200, -50)
        self.original_y = self.rect.y
        self.bobbing_offset = random.uniform(0, math.pi * 2)
        self.hitbox = self.rect.inflate(-self.rect.width * (1 - hitbox_scale), -self.rect.height * (1 - hitbox_scale))

    def update(self):
        self.rect.y += 10
        if self.image == plant_image:
            self.rect.y += math.sin(pygame.time.get_ticks() * 0.005 + self.bobbing_offset) * 0.65
        else:
            self.rect.y += math.sin(pygame.time.get_ticks() * 0.005 + self.bobbing_offset) * OBSTACLE_BOBBING_AMPLITUDE
        self.hitbox.center = self.rect.center

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randint(-200, -50)
            self.rect.x = random.choice([random.randint(100, SCREEN_WIDTH - self.rect.width - 100),
                                         random.randint(0, 50), random.randint(SCREEN_WIDTH - 50, SCREEN_WIDTH)])
            self.original_y = self.rect.y
            self.bobbing_offset = random.uniform(0, math.pi * 2)

def menu():
    while True:
        screen.fill((0, 0, 0))
        title_text = menu_font.render("GUPPY GETAWAY", True, (255, 255, 255))
        play_text = font.render("Press SPACE to Play", True, (255, 255, 255))
        quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

        screen.blit(title_text, title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)))
        screen.blit(play_text, play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def main():
    global frame, scroll_y
    obstacles = pygame.sprite.Group()
    for _ in range(5):
        obstacle = Obstacle(random.choice([mine_image, plant_image]), hitbox_scale=0.7)
        obstacles.add(obstacle)

    guppy_x, guppy_y = 350, 555
    score, frame, scroll_y = 0, 0, 0
    speed = START_SPEED
    elapsed_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            guppy_x = max(20, guppy_x - speed)
        if keys[pygame.K_d]:
            guppy_x = min(SCREEN_WIDTH - GUPPY_WIDTH - 20, guppy_x + speed)

        elapsed_time += clock.get_time() / 1000
        if elapsed_time >= 30:
            elapsed_time = 0
            speed = min(MAX_SPEED, speed + 1)

        frame = (frame + 1) % GUPPY_ANIMATION_STEPS
        obstacles.update()

        if pygame.Rect(guppy_x, guppy_y, GUPPY_WIDTH, GUPPY_HEIGHT).collidelist([obs.hitbox for obs in obstacles]) != -1:
            return

        draw_background()
        screen.blit(animation_list[frame], (guppy_x, guppy_y))
        obstacles.draw(screen)

        score_text = font.render(f"SCORE: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, 30))
        pygame.display.update()

        score += 1
        clock.tick(30)

if __name__ == "__main__":
    while True:
        menu()
        main()
 