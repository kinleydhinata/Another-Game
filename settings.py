import sys

print("settings.py: Starting imports", file=sys.stderr)
import os
import math
print("settings.py: Imports completed", file=sys.stderr)

print("settings.py: Defining constants", file=sys.stderr)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def path(filename):
    return os.path.join('assets', filename)

# Update all asset paths to use the path function
WALL_TEXTURE_PATH = path('images/wall_texture.jpg')
ENEMY_ANIMATION_PATH = path('images/enemy_animation.gif')
WEAPON_IDLE_PATH = path('images/weapon_idle.png')
WEAPON_SHOOT_PATH = path('images/weapon_shoot.png')
SHOOT_SOUND_PATH = path('audio/shoot.wav')
RELOAD_SOUND_PATH = path('audio/reload.wav')
HIT_SOUND_PATH = path('audio/hit.wav')
ENEMY_DEATH_SOUND_PATH = path('audio/enemy_death.wav')
BACKGROUND_MUSIC_PATH = path('audio/background_music.mp3')
MENU_MUSIC_PATH = path('audio/menu_music.mp3')
MENU_BACKGROUND_PATH = path('images/menu_background.jpg')

WIDTH, HEIGHT = 1280, 720
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
DASHBOARD_HEIGHT = 100
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CEILING_COLOR = (135, 206, 235)
FLOOR_COLOR = (139, 69, 19)
DASHBOARD_COLOR = (50, 50, 50)

MAP_WIDTH, MAP_HEIGHT = 16, 16
TILE = 100

PLAYER_SPEED = 2
MAX_PLAYER_HEALTH = 100
HEALTH_REGEN_RATE = 1
HEALTH_REGEN_DELAY = 5000

FOV = math.pi / 3
NUM_RAYS = 320
MAX_DEPTH = max(MAP_WIDTH, MAP_HEIGHT) * TILE
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

WEAPON_ANIMATION_TIME = 200
BULLET_SPEED = 15
MAGAZINE_SIZE = 30
RELOAD_TIME = 2000
FIRE_RATE = 200

ENEMY_SPAWN_INTERVAL = 10000

print("settings.py: Constants defined", file=sys.stderr)