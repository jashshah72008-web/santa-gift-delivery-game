import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Santa's Gift Drop")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 20, 50)
RED = (220, 20, 20)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
HOUSE_COLORS = [(70, 130, 180), (205, 92, 92), (60, 179, 113), (218, 165, 32)]

# Game Variables
score = 0
font = pygame.font.SysFont("Arial", 32, bold=True)

# --- Classes ---

class Snowflake:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(2, 5)
        self.speed = random.uniform(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-50, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


class House:
    def __init__(self, x, color):
        self.width = 100
        self.height = 120
        self.x = x
        self.y = HEIGHT - self.height - 40 # 40 px above bottom for snow ground
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.has_gift = False

    def draw(self, surface):
        # House body
        pygame.draw.rect(surface, self.color, self.rect)
        # Windows
        pygame.draw.rect(surface, YELLOW if self.has_gift else WHITE, (self.x + 15, self.y + 30, 25, 25))
        pygame.draw.rect(surface, YELLOW if self.has_gift else WHITE, (self.x + 60, self.y + 30, 25, 25))
        # Door
        pygame.draw.rect(surface, BROWN, (self.x + 35, self.y + 70, 30, 50))
        # Snowy Roof
        pygame.draw.polygon(surface, WHITE, [(self.x - 10, self.y), (self.x + self.width / 2, self.y - 60), (self.x + self.width + 10, self.y)])

        # Feedback if gift received
        if self.has_gift:
            text = font.render("+10", True, YELLOW)
            surface.blit(text, (self.x + 25, self.y - 90))


class Santa:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 80
        self.speed = 5
        self.width = 80
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def draw(self, surface):
        # Draw Sleigh (Red rectangle)
        pygame.draw.rect(surface, RED, self.rect, border_radius=10)
        # Draw Santa (Small white/red shapes)
        pygame.draw.circle(surface, WHITE, (self.x + 20, self.y - 10), 12) # Head/Beard
        pygame.draw.polygon(surface, RED, [(self.x + 10, self.y - 15), (self.x + 30, self.y - 15), (self.x + 20, self.y - 30)]) # Hat
        # Reindeer abstract shape
        pygame.draw.rect(surface, BROWN, (self.x + self.width, self.y + 10, 30, 20), border_radius=5)
        # Reins
        pygame.draw.line(surface, WHITE, (self.x + self.width, self.y + 15), (self.x + self.width + 10, self.y + 5), 2)


class Gift:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 4
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.active = True

    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > HEIGHT:
            self.active = False

    def draw(self, surface):
        pygame.draw.rect(surface, YELLOW, self.rect)
        # Ribbon
        pygame.draw.line(surface, RED, (self.x + self.size//2, self.y), (self.x + self.size//2, self.y + self.size), 3)
        pygame.draw.line(surface, RED, (self.x, self.y + self.size//2), (self.x + self.size, self.y + self.size//2), 3)

# --- Initialization ---
snowflakes = [Snowflake() for _ in range(150)]
houses = [House(100 + i * 180, HOUSE_COLORS[i % len(HOUSE_COLORS)]) for i in range(4)]
santa = Santa()
gifts = []

# --- Main Game Loop ---
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Drop a gift from center of sleigh
                gifts.append(Gift(santa.x + santa.width // 2 - 10, santa.y + santa.height))

    keys = pygame.key.get_pressed()

    # 2. Update Logic
    santa.update(keys)

    for flake in snowflakes:
        flake.update()

    # Reset house gift status timer visually
    for house in houses:
        if house.has_gift and random.random() < 0.02: # simple way to turn off light eventually
            house.has_gift = False

    for gift in gifts:
        if gift.active:
            gift.update()
            # Check collision with houses
            for house in houses:
                if gift.rect.colliderect(house.rect) and not house.has_gift:
                    gift.active = False
                    house.has_gift = True
                    score += 10
                    break

    # Remove inactive gifts
    gifts = [g for g in gifts if g.active]

    # 3. Drawing
    screen.fill(DARK_BLUE) # Night sky

    # Draw Moon
    pygame.draw.circle(screen, (220, 220, 240), (WIDTH - 150, 120), 60)

    # Draw Snow (Background layer)
    for flake in snowflakes:
        flake.draw(screen)

    # Draw Ground
    pygame.draw.rect(screen, WHITE, (0, HEIGHT - 40, WIDTH, 40))

    # Draw Houses
    for house in houses:
        house.draw(screen)

    # Draw Gifts
    for gift in gifts:
        gift.draw(screen)

    # Draw Santa
    santa.draw(screen)

    # Draw Score
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # Controls text
    controls_text = pygame.font.SysFont("Arial", 20).render("Use LEFT/RIGHT arrows to move. Press SPACE to drop gifts.", True, WHITE)
    screen.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, 20))

    # Update Display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
