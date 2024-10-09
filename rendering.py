import pygame
import math
from settings import *


class Renderer:
    def __init__(self, screen, game_map):
        self.screen = screen
        self.game_map = game_map
        self.textures = {
            '#': pygame.image.load(WALL_TEXTURE_PATH).convert(),
        }

    def render(self, player, enemies, weapon_system):
        self.draw_background()
        wall_depths = self.cast_rays(player)
        self.draw_enemies(player, enemies, wall_depths)
        self.draw_weapon(weapon_system.get_weapon_image())

    def draw_background(self):
        self.screen.fill(CEILING_COLOR)
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def cast_rays(self, player):
        wall_depths = []
        start_angle = player.angle - FOV / 2
        for ray in range(NUM_RAYS):
            sin_a = math.sin(start_angle)
            cos_a = math.cos(start_angle)
            for depth in range(0, MAX_DEPTH, 5):
                x = player.x + depth * cos_a
                y = player.y + depth * sin_a
                if self.game_map.is_wall(x, y):
                    depth *= math.cos(player.angle - start_angle)
                    wall_depths.append(depth)
                    proj_height = min(PROJ_COEFF / (depth + 0.0001), HEIGHT)
                    self.draw_wall_column(ray, proj_height, depth, x, y)
                    break
            else:
                wall_depths.append(MAX_DEPTH)
            start_angle += DELTA_ANGLE
        return wall_depths

    def draw_wall_column(self, ray, proj_height, depth, x, y):
        texture = self.textures['#']
        tx = int((x % TILE) / TILE * texture.get_width())
        wall_column = pygame.transform.scale(
            texture.subsurface(tx, 0, 1, texture.get_height()),
            (SCALE, int(proj_height))
        )
        self.screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))

    def draw_enemies(self, player, enemies, wall_depths):
        for enemy in enemies:
            dx, dy = enemy.x - player.x, enemy.y - player.y
            distance = math.hypot(dx, dy)
            angle = math.atan2(dy, dx) - player.angle
            angle = (angle + math.pi) % (2 * math.pi) - math.pi
            if -FOV / 2 < angle < FOV / 2 and distance > 30:
                proj_height = min(PROJ_COEFF / (distance + 0.0001), HEIGHT * 2)
                if proj_height > 0:
                    enemy_x = HALF_WIDTH + math.tan(angle) * DIST
                    enemy_y = HALF_HEIGHT - proj_height // 2
                    enemy_size = int(proj_height)
                    if enemy_y + enemy_size < HEIGHT:
                        enemy_frame = enemy.get_current_frame()
                        enemy_surface = pygame.transform.scale(enemy_frame, (enemy_size, enemy_size))
                        enemy_surface_rect = enemy_surface.get_rect(center=(int(enemy_x), int(enemy_y + enemy_size // 2)))
                        start_i = max(0, enemy_surface_rect.left)
                        end_i = min(WIDTH - 1, enemy_surface_rect.right)
                        for i in range(start_i, end_i):
                            ray = min(int((i / WIDTH) * NUM_RAYS), NUM_RAYS - 1)
                            if distance < wall_depths[ray]:
                                column = i - enemy_surface_rect.left
                                column_surface = enemy_surface.subsurface(pygame.Rect(column, 0, 1, enemy_size))
                                self.screen.blit(column_surface, (i, int(enemy_y)))

    def draw_weapon(self, weapon_image):
        weapon_rect = weapon_image.get_rect(centerx=HALF_WIDTH, bottom=HEIGHT - 10)
        self.screen.blit(weapon_image, weapon_rect)
