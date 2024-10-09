import random

import pygame
import math
from PIL import Image
from settings import *


class Enemy:
    animation_frames = []

    @classmethod
    def load_animation_frames(cls, gif_path):
        if not cls.animation_frames:
            with Image.open(gif_path) as gif:
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    frame_surface = pygame.image.fromstring(
                        gif.convert("RGBA").tobytes(), gif.size, "RGBA"
                    )
                    cls.animation_frames.append(frame_surface)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 100
        self.speed = 1
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_counter = 0

    def move(self, dx, dy, game_map):
        if not game_map.is_wall(self.x + dx, self.y): self.x += dx
        if not game_map.is_wall(self.x, self.y + dy): self.y += dy

    def take_damage(self, amount):
        self.health -= amount

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.animation_frames)
            self.frame_counter = 0

    def get_current_frame(self):
        return self.animation_frames[self.current_frame]


class EnemyManager:
    def __init__(self, game_map):
        self.enemies = []
        self.game_map = game_map
        self.last_spawn_time = 0
        Enemy.load_animation_frames(ENEMY_ANIMATION_PATH)
        self.spawn_initial_enemies()

    def spawn_initial_enemies(self):
        self.spawn_enemy(300, 300)
        self.spawn_enemy(500, 500)

    def spawn_enemy(self, x, y):
        self.enemies.append(Enemy(x, y))

    def update(self, player, game_map, game_state, sound_manager):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > ENEMY_SPAWN_INTERVAL:
            self.spawn_random_enemies()
            self.last_spawn_time = current_time

        for enemy in self.enemies[:]:
            dx, dy = player.x - enemy.x, player.y - enemy.y
            dist = math.hypot(dx, dy)
            if dist > TILE / 2:
                dx_norm, dy_norm = dx / dist * enemy.speed, dy / dist * enemy.speed
                enemy.move(dx_norm, dy_norm, game_map)
            else:
                player.take_damage(1)
                sound_manager.play_sound('hit')

            enemy.update()

            if enemy.health <= 0:
                self.enemies.remove(enemy)
                game_state.increment_score(100)
                sound_manager.play_sound('enemy_death')

    def spawn_random_enemies(self):
        for _ in range(random.randint(1, 2)):
            while True:
                x = random.randint(1, MAP_WIDTH - 2) * TILE + TILE // 2
                y = random.randint(1, MAP_HEIGHT - 2) * TILE + TILE // 2
                if (not self.game_map.is_wall(x, y) and
                        math.hypot(x - HALF_WIDTH, y - HALF_HEIGHT) > TILE * 3):
                    self.spawn_enemy(x, y)
                    break

    def reset(self):
        self.enemies.clear()
        self.last_spawn_time = 0
        self.spawn_initial_enemies()
