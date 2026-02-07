import pygame
import random
import sys
import math
import os

# ---------------- INITIALIZATION ----------------
pygame.init()
pygame.font.init()
pygame.mixer.init()

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

# ---------------- SCREEN SETUP (FULLSCREEN) ----------------
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("TARZAN – Catch The Bananas")

clock = pygame.time.Clock()
FPS = 60

# ---------------- LOAD ASSETS ----------------
def load_image(filename, size):
    path = os.path.join(IMAGE_DIR, filename)
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Backgrounds
bg_levels = [
    load_image("jungle_level1.png", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    load_image("jungle_level2.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT)),
    load_image("jungle_level3.jpg", (SCREEN_WIDTH, SCREEN_HEIGHT))
]

# Sprites
player_img = load_image("tarzan.png", (90, 90))
banana_img = load_image("banana.png", (55, 55))
coconut_img = load_image("coconut.png", (55, 55))
golden_banana_img = load_image("golden_banana.png", (55, 55))
heart_img = load_image("heart.png", (55, 55))
shield_img = load_image("shield.png", (55, 55))

# ---------------- SOUNDS ----------------
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(SOUND_DIR, filename))

catch_sound = load_sound("catch.mp3")
hit_sound = load_sound("hit.mp3")
powerup_sound = load_sound("powerup.mp3")

pygame.mixer.music.load(os.path.join(SOUND_DIR, "background_music.mp3"))
pygame.mixer.music.play(-1)

music_on = True
effects_on = True

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont(None, 80)
big_font = pygame.font.SysFont(None, 60)
font = pygame.font.SysFont(None, 36)

# ---------------- PLAYER ----------------
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 90
PLAYER_SPEED = 9
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 30

# ---------------- GAME STATES ----------------
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
SETTINGS = "settings"
state = MENU

# ---------------- GAME VARIABLES ----------------
score = 0
lives = 3
combo = 0
multiplier = 1
shield_active = False
shield_timer = 0
OBJECT_SIZE = 55
falling_objects = []
level = 1

# ---------------- HIGH SCORE ----------------
def load_highscore():
    path = os.path.join(BASE_DIR, "highscore.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return int(f.read())
    return 0

def save_highscore(value):
    path = os.path.join(BASE_DIR, "highscore.txt")
    with open(path, "w") as f:
        f.write(str(value))

high_score = load_highscore()

# ---------------- OBJECT CREATION ----------------
def create_object():
    obj_type = random.choices(
        ["banana", "coconut", "golden_banana", "heart", "shield"],
        weights=[50, 40, 5, 3, 2],
        k=1
    )[0]

    return {
        "x": random.randint(0, SCREEN_WIDTH - OBJECT_SIZE),
        "y": random.randint(-600, -50),
        "type": obj_type,
        "speed": random.randint(3, 6),
        "angle": 0
    }

# ---------------- RESET GAME ----------------
def reset_game():
    global score, lives, combo, multiplier, shield_active, shield_timer
    global falling_objects, player_x, level, state

    score = 0
    lives = 3
    combo = 0
    multiplier = 1
    shield_active = False
    shield_timer = 0
    level = 1

    falling_objects = [create_object() for _ in range(8)]
    player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
    state = PLAYING

# ---------------- STATE CHANGE ----------------
def change_state(new_state):
    global state
    state = new_state

# ---------------- BUTTON CLASS ----------------
class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        pygame.draw.rect(surface,
                         self.hover_color if self.rect.collidepoint(mouse) else self.color,
                         self.rect)

        if self.rect.collidepoint(mouse) and click[0] and self.action:
            self.action()

        txt = font.render(self.text, True, (0, 0, 0))
        surface.blit(txt, (self.rect.centerx - txt.get_width() // 2,
                           self.rect.centery - txt.get_height() // 2))

# ---------------- SETTINGS ----------------
def toggle_music():
    global music_on
    music_on = not music_on
    pygame.mixer.music.unpause() if music_on else pygame.mixer.music.pause()

def toggle_effects():
    global effects_on
    effects_on = not effects_on

def quit_game():
    pygame.quit()
    sys.exit()

# ---------------- BUTTONS ----------------
start_button = Button("Start", SCREEN_WIDTH//2 - 100, 360, 200, 60,
                      (50, 200, 50), (100, 255, 100), reset_game)

settings_button = Button("Settings", SCREEN_WIDTH//2 - 100, 440, 200, 60,
                         (50, 50, 200), (100, 100, 255),
                         lambda: change_state(SETTINGS))

quit_button = Button("Quit", SCREEN_WIDTH//2 - 100, 520, 200, 60,
                     (200, 50, 50), (255, 100, 100), quit_game)

music_button = Button("Music ON / OFF", SCREEN_WIDTH//2 - 120, 300, 240, 50,
                      (150, 150, 50), (200, 200, 50), toggle_music)

effects_button = Button("Effects ON / OFF", SCREEN_WIDTH//2 - 120, 370, 240, 50,
                        (150, 150, 50), (200, 200, 50), toggle_effects)

back_button = Button("Back", SCREEN_WIDTH//2 - 60, 440, 120, 50,
                     (200, 200, 200), (255, 255, 255),
                     lambda: change_state(MENU))

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_game()
            if state == PLAYING and event.key == pygame.K_p:
                state = PAUSED
            elif state == PAUSED and event.key == pygame.K_p:
                state = PLAYING
            elif state == GAME_OVER and event.key == pygame.K_r:
                reset_game()
            if event.type == pygame.USEREVENT + 1:
                multiplier = 1
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)

    # ---------------- LEVELS (LONGER) ----------------
    level = 1 if score <= 50 else 2 if score <= 120 else 3

    # ---------------- GAME STATES ----------------
    if state == MENU:
        screen.blit(bg_levels[0], (0, 0))
        screen.blit(title_font.render("TARZAN", True, (255, 255, 255)),
                    (SCREEN_WIDTH//2 - 120, 220))
        screen.blit(big_font.render("Catch The Bananas", True, (255, 215, 0)),
                    (SCREEN_WIDTH//2 - 200, 300))
        start_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

    elif state == SETTINGS:
        screen.fill((40, 40, 40))
        music_button.draw(screen)
        effects_button.draw(screen)
        back_button.draw(screen)

    elif state == PLAYING:
        screen.blit(bg_levels[level - 1], (0, 0))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_x += PLAYER_SPEED

        for obj in falling_objects:
            obj["y"] += obj["speed"] + score // 12 + level
            if obj["type"] == "coconut":
                obj["angle"] += 5
            if obj["y"] > SCREEN_HEIGHT:
                obj.update(create_object())

            if (player_x < obj["x"] + OBJECT_SIZE and
                player_x + PLAYER_WIDTH > obj["x"] and
                player_y < obj["y"] + OBJECT_SIZE and
                player_y + PLAYER_HEIGHT > obj["y"]):

                if obj["type"] == "banana":
                    score += multiplier
                    if effects_on: catch_sound.play()

                elif obj["type"] == "coconut" and not shield_active:
                    lives -= 1
                    if effects_on: hit_sound.play()

                elif obj["type"] == "golden_banana":
                    multiplier = 2
                    pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
                    if effects_on: powerup_sound.play()

                elif obj["type"] == "heart":
                    lives += 1
                    if effects_on: powerup_sound.play()

                elif obj["type"] == "shield":
                    shield_active = True
                    shield_timer = 300
                    if effects_on: powerup_sound.play()

                obj.update(create_object())

            if obj["type"] == "banana":
                screen.blit(banana_img, (obj["x"], obj["y"]))
            elif obj["type"] == "golden_banana":
                screen.blit(golden_banana_img, (obj["x"], obj["y"]))
            elif obj["type"] == "coconut":
                screen.blit(pygame.transform.rotate(coconut_img, obj["angle"]),
                            (obj["x"], obj["y"]))
            elif obj["type"] == "heart":
                screen.blit(heart_img, (obj["x"], obj["y"]))
            elif obj["type"] == "shield":
                screen.blit(shield_img, (obj["x"], obj["y"]))

        screen.blit(player_img, (player_x, player_y))

        if shield_active:
            pygame.draw.circle(screen, (0, 255, 255),
                               (player_x + PLAYER_WIDTH//2,
                                player_y + PLAYER_HEIGHT//2), 55, 4)
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (20, 15))
        screen.blit(font.render(f"Lives: {lives}", True, (255, 80, 80)),
                    (SCREEN_WIDTH - 150, 15))

        if lives <= 0:
            save_highscore(max(score, high_score))
            state = GAME_OVER

    elif state == GAME_OVER:
        screen.fill((0, 0, 0))
        screen.blit(big_font.render("GAME OVER", True, (255, 0, 0)),
                    (SCREEN_WIDTH//2 - 150, 260))
        screen.blit(font.render(f"Final Score: {score}", True, (255, 255, 255)),
                    (SCREEN_WIDTH//2 - 120, 330))
        screen.blit(font.render(f"High Score: {load_highscore()}", True, (255, 215, 0)),
                    (SCREEN_WIDTH//2 - 120, 370))
        screen.blit(font.render("Press R to Restart", True, (255, 255, 255)),
                    (SCREEN_WIDTH//2 - 130, 420))

    pygame.display.flip()

pygame.quit()
sys.exit()
