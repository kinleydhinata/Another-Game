import pygame
import sys
import math
import random

pygame.init()
pygame.mouse.set_visible(False)

# Screen settings
WIDTH, HEIGHT = 1280, 720  # Increased screen size
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2
DASHBOARD_HEIGHT = 100  # Height of the dashboard at the bottom

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Modern FPS Game")
clock = pygame.time.Clock()

# Colors
WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE = (
    (255, 255, 255),
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (128, 0, 128),
)
CEILING_COLOR = (135, 206, 235)  # Sky blue
FLOOR_COLOR = (139, 69, 19)  # Saddle brown
DASHBOARD_COLOR = (50, 50, 50)  # Dark gray

# Map settings
MAP_SCALE = 5
MAP_WIDTH = 16
MAP_HEIGHT = 16
TILE = 100

player_pos = [HALF_WIDTH, HALF_HEIGHT]
player_angle = 0
player_speed = 2
player_health = 100
max_player_health = 100
health_regen_rate = 1  # health points per second
last_hit_time = 0
health_regen_delay = 5000  # 5 seconds in milliseconds

game_map = [
    '################',
    '#..............#',
    '#....######....#',
    '#..............#',
    '#...........####',
    '#..............#',
    '#....#####.....#',
    '#..............#',
    '###............#',
    '#..............#',
    '#....######....#',
    '#..............#',
    '#...........####',
    '#..............#',
    '#..............#',
    '################',
]

FOV = math.pi / 3
NUM_RAYS = 320  # Increased number of rays for better resolution
MAX_DEPTH = max(MAP_WIDTH, MAP_HEIGHT) * TILE
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(FOV / 2))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

# Load textures
textures = {
    '#': pygame.image.load('wall_texture.jpg').convert(),
}
enemy_texture = pygame.image.load('enemy_texture.png').convert_alpha()

# Weapon images
weapon_idle = pygame.image.load('weapon_idle.png').convert_alpha()
weapon_shoot = pygame.image.load('weapon_shoot.png').convert_alpha()
current_weapon_image = weapon_idle
weapon_rect = current_weapon_image.get_rect()
weapon_rect.centerx = HALF_WIDTH
weapon_rect.bottom = HEIGHT - 10  # Position above the dashboard

weapon_animation_time = 200  # milliseconds
last_weapon_animation_time = 0

enemies = [
    {'x': 300, 'y': 300, 'health': 100, 'speed': 1},
    {'x': 500, 'y': 500, 'health': 100, 'speed': 1},
]

font = pygame.font.SysFont('Arial', 36)
small_font = pygame.font.SysFont('Arial', 24)

bullet_speed = 15  # Increased bullet speed
bullets = []
magazine_size = 30
current_ammo = magazine_size
reload_time = 2000  # milliseconds
last_reload_time = 0
fire_rate = 200  # milliseconds
last_shot_time = 0

score = 0

enemy_spawn_interval = 10000  # Start at 10 seconds in milliseconds
last_enemy_spawn_time = 0


def cast_rays():
    start_angle = player_angle - FOV / 2
    wall_depths = []
    texture = textures['#']
    texture_width = texture.get_width()
    texture_height = texture.get_height()
    for ray in range(NUM_RAYS):
        sin_a = math.sin(start_angle)
        cos_a = math.cos(start_angle)
        for depth in range(0, MAX_DEPTH, 5):
            x = player_pos[0] + depth * cos_a
            y = player_pos[1] + depth * sin_a
            col, row = int(x / TILE), int(y / TILE)
            if 0 <= col < MAP_WIDTH and 0 <= row < MAP_HEIGHT:
                if game_map[row][col] == '#':
                    depth *= math.cos(player_angle - start_angle)
                    wall_depths.append(depth)
                    proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT - DASHBOARD_HEIGHT)
                    # Texture mapping
                    tx = int((x % TILE) / TILE * texture_width)
                    wall_column = texture.subsurface(tx, 0, 1, texture_height)
                    wall_column = pygame.transform.scale(wall_column, (SCALE, int(proj_height)))
                    screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
                    break
        else:
            wall_depths.append(MAX_DEPTH)
        start_angle += DELTA_ANGLE
    return wall_depths


def move_player(dx, dy):
    next_x, next_y = player_pos[0] + dx, player_pos[1] + dy
    if not wall_collision(next_x, player_pos[1]):
        player_pos[0] = next_x
    if not wall_collision(player_pos[0], next_y):
        player_pos[1] = next_y


def wall_collision(x, y):
    return game_map[int(y / TILE)][int(x / TILE)] == '#'


def draw_enemies(wall_depths):
    for enemy in enemies:
        dx, dy = enemy['x'] - player_pos[0], enemy['y'] - player_pos[1]
        distance = math.hypot(dx, dy)
        angle = math.atan2(dy, dx) - player_angle
        # Normalize angle to (-pi, pi)
        angle = (angle + math.pi) % (2 * math.pi) - math.pi
        if -FOV / 2 < angle < FOV / 2 and distance > 30:
            proj_height = min(PROJ_COEFF / (distance + 0.0001), HEIGHT * 2)
            if proj_height > 0:
                enemy_x = HALF_WIDTH + math.tan(angle) * DIST
                enemy_y = HALF_HEIGHT - proj_height // 2
                enemy_size = int(proj_height)
                if enemy_y + enemy_size < HEIGHT - DASHBOARD_HEIGHT:
                    # Scale the enemy texture
                    enemy_surface = pygame.transform.scale(enemy_texture, (enemy_size, enemy_size))
                    enemy_surface_rect = enemy_surface.get_rect(
                        center=(int(enemy_x), int(enemy_y + enemy_size // 2))
                    )
                    # Occlusion check
                    start_i = max(0, enemy_surface_rect.left)
                    end_i = min(WIDTH - 1, enemy_surface_rect.right)
                    for i in range(start_i, end_i):
                        ray = int((i / WIDTH) * NUM_RAYS)
                        if ray >= NUM_RAYS:
                            ray = NUM_RAYS - 1
                        if distance < wall_depths[ray]:
                            column = i - enemy_surface_rect.left
                            column_surface = enemy_surface.subsurface(
                                pygame.Rect(column, 0, 1, enemy_size)
                            )
                            screen.blit(column_surface, (i, int(enemy_y)))


def draw_ui():
    # Draw dashboard background
    pygame.draw.rect(
        screen, DASHBOARD_COLOR, (0, HEIGHT - DASHBOARD_HEIGHT, WIDTH, DASHBOARD_HEIGHT)
    )

    # Draw health bar
    health_bar_width = 200
    health_bar_height = 25
    health_ratio = player_health / max_player_health
    pygame.draw.rect(
        screen,
        RED,
        (
            20,
            HEIGHT - DASHBOARD_HEIGHT + 20,
            health_bar_width * health_ratio,
            health_bar_height,
        ),
    )
    pygame.draw.rect(
        screen,
        WHITE,
        (20, HEIGHT - DASHBOARD_HEIGHT + 20, health_bar_width, health_bar_height),
        2,
    )

    # Draw ammo
    ammo_text = font.render(f'Ammo: {current_ammo}/{magazine_size}', True, WHITE)
    screen.blit(ammo_text, (250, HEIGHT - DASHBOARD_HEIGHT + 15))

    # Draw score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (WIDTH - 220, HEIGHT - DASHBOARD_HEIGHT + 15))

    # Draw crosshair
    pygame.draw.line(
        screen,
        WHITE,
        (HALF_WIDTH - 15, HALF_HEIGHT),
        (HALF_WIDTH + 15, HALF_HEIGHT),
        2,
    )
    pygame.draw.line(
        screen,
        WHITE,
        (HALF_WIDTH, HALF_HEIGHT - 15),
        (HALF_WIDTH, HALF_HEIGHT + 15),
        2,
    )


def shoot():
    global current_ammo, last_shot_time, current_weapon_image, last_weapon_animation_time
    current_time = pygame.time.get_ticks()
    if current_ammo > 0 and current_time - last_shot_time > fire_rate:
        current_ammo -= 1
        last_shot_time = current_time
        bullets.append({'x': player_pos[0], 'y': player_pos[1], 'angle': player_angle})
        # Switch to shooting weapon image
        current_weapon_image = weapon_shoot
        last_weapon_animation_time = current_time


def update_bullets():
    for bullet in bullets[:]:
        prev_x, prev_y = bullet['x'], bullet['y']
        bullet['x'] += math.cos(bullet['angle']) * bullet_speed
        bullet['y'] += math.sin(bullet['angle']) * bullet_speed
        # Draw bullet trail
        pygame.draw.line(
            screen, YELLOW, (prev_x, prev_y), (bullet['x'], bullet['y']), 2
        )
        if wall_collision(bullet['x'], bullet['y']):
            bullets.remove(bullet)
        else:
            for enemy in enemies[:]:
                if math.hypot(bullet['x'] - enemy['x'], bullet['y'] - enemy['y']) < TILE // 3:
                    enemy['health'] -= 20
                    if enemy['health'] <= 0:
                        enemies.remove(enemy)
                        increment_score(100)
                    bullets.remove(bullet)
                    break


def reload():
    global current_ammo, last_reload_time
    current_time = pygame.time.get_ticks()
    if current_ammo < magazine_size and current_time - last_reload_time > reload_time:
        current_ammo = magazine_size
        last_reload_time = current_time


def move_enemy(enemy, dx, dy):
    next_x = enemy['x'] + dx
    next_y = enemy['y'] + dy
    if not wall_collision(next_x, enemy['y']):
        enemy['x'] = next_x
    if not wall_collision(enemy['x'], next_y):
        enemy['y'] = next_y


def move_enemies():
    global player_health, last_hit_time
    for enemy in enemies:
        dx, dy = player_pos[0] - enemy['x'], player_pos[1] - enemy['y']
        dist = math.hypot(dx, dy)
        if dist > TILE / 2:
            dx_norm = dx / dist * enemy['speed']
            dy_norm = dy / dist * enemy['speed']
            move_enemy(enemy, dx_norm, dy_norm)
        else:
            player_health -= 1
            last_hit_time = pygame.time.get_ticks()


def increment_score(points):
    global score
    score += points


def spawn_enemies():
    global last_enemy_spawn_time, enemy_spawn_interval
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > enemy_spawn_interval:
        num_enemies_to_spawn = random.randint(1, 2)
        for _ in range(num_enemies_to_spawn):
            while True:
                x = random.randint(1, MAP_WIDTH - 2) * TILE + TILE // 2
                y = random.randint(1, MAP_HEIGHT - 2) * TILE + TILE // 2
                if (
                    not wall_collision(x, y)
                    and math.hypot(x - player_pos[0], y - player_pos[1]) > TILE * 3
                ):
                    enemies.append({'x': x, 'y': y, 'health': 100, 'speed': 1})
                    break
        last_enemy_spawn_time = current_time


def regenerate_health():
    global player_health
    current_time = pygame.time.get_ticks()
    if current_time - last_hit_time > health_regen_delay:
        player_health = min(player_health + health_regen_rate / 60, max_player_health)


def game_over():
    game_over_text = font.render('GAME OVER', True, RED)
    restart_text = font.render('Press R to Restart or Q to Quit', True, WHITE)
    final_score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(
        game_over_text,
        (HALF_WIDTH - game_over_text.get_width() // 2, HALF_HEIGHT - 100),
    )
    screen.blit(
        restart_text,
        (HALF_WIDTH - restart_text.get_width() // 2, HALF_HEIGHT),
    )
    screen.blit(
        final_score_text,
        (HALF_WIDTH - final_score_text.get_width() // 2, HALF_HEIGHT + 100),
    )
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False
    return False


def reset_game():
    global player_pos, player_angle, player_health, current_ammo, score
    global enemies, bullets, last_hit_time, last_enemy_spawn_time, enemy_spawn_interval
    player_pos = [HALF_WIDTH, HALF_HEIGHT]
    player_angle = 0
    player_health = max_player_health
    current_ammo = magazine_size
    score = 0
    enemies.clear()
    enemies.extend(
        [
            {'x': 300, 'y': 300, 'health': 100, 'speed': 1},
            {'x': 500, 'y': 500, 'health': 100, 'speed': 1},
        ]
    )
    bullets.clear()
    last_hit_time = 0
    last_enemy_spawn_time = 0
    enemy_spawn_interval = 10000


def draw_instructions():
    instructions = [
        "WASD: Move",
        "Mouse: Aim",
        "Left Click: Shoot",
        "R: Reload",
        "ESC: Exit",
    ]
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, WHITE)
        screen.blit(text, (20, HEIGHT - DASHBOARD_HEIGHT + 60 + i * 20))


def game_loop():
    global player_health, player_angle, current_weapon_image, last_weapon_animation_time
    running = True
    pygame.event.set_grab(True)
    while running:
        screen.fill(CEILING_COLOR)
        pygame.draw.rect(
            screen,
            FLOOR_COLOR,
            (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT - DASHBOARD_HEIGHT),
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reload()
                if event.key == pygame.K_ESCAPE:
                    running = False

        mouse_dx, _ = pygame.mouse.get_rel()
        player_angle += mouse_dx * 0.002
        player_angle %= 2 * math.pi

        keys = pygame.key.get_pressed()
        dx = dy = 0
        sin_a = math.sin(player_angle)
        cos_a = math.cos(player_angle)
        if keys[pygame.K_w]:
            dx += cos_a * player_speed
            dy += sin_a * player_speed
        if keys[pygame.K_s]:
            dx -= cos_a * player_speed
            dy -= sin_a * player_speed
        if keys[pygame.K_a]:
            dx += sin_a * player_speed
            dy -= cos_a * player_speed
        if keys[pygame.K_d]:
            dx -= sin_a * player_speed
            dy += cos_a * player_speed
        move_player(dx, dy)

        wall_depths = cast_rays()
        move_enemies()
        update_bullets()
        spawn_enemies()
        regenerate_health()
        draw_enemies(wall_depths)
        draw_ui()
        draw_instructions()

        # Weapon animation timing
        current_time = pygame.time.get_ticks()
        if current_weapon_image == weapon_shoot and current_time - last_weapon_animation_time > weapon_animation_time:
            current_weapon_image = weapon_idle

        # Draw weapon image
        weapon_rect = current_weapon_image.get_rect()
        weapon_rect.centerx = HALF_WIDTH
        weapon_rect.bottom = HEIGHT - 10  # Position above the dashboard
        screen.blit(current_weapon_image, weapon_rect)

        pygame.display.flip()
        clock.tick(60)

        if player_health <= 0:
            if game_over():
                reset_game()
            else:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    game_loop()