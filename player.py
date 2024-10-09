import pygame
import math
from settings import *


class Player:
    def __init__(self, x, y, sensitivity=0.0015):
        self.x = x
        self.y = y
        self.angle = 0
        self.sensitivity = sensitivity
        self.health = MAX_PLAYER_HEALTH
        self.last_hit_time = 0
        self.last_mouse_pos = (HALF_WIDTH, HALF_HEIGHT)

    def update(self, game_map):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx = dy = 0
        speed = PLAYER_SPEED * (pygame.key.get_pressed()[pygame.K_LSHIFT] + 1)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: dx += cos_a * speed; dy += sin_a * speed
        if keys[pygame.K_s]: dx -= cos_a * speed; dy -= sin_a * speed
        if keys[pygame.K_a]: dx += sin_a * speed; dy -= cos_a * speed
        if keys[pygame.K_d]: dx -= sin_a * speed; dy += cos_a * speed
        self.move(dx, dy, game_map)

        current_mouse_pos = pygame.mouse.get_pos()
        mouse_dx = current_mouse_pos[0] - self.last_mouse_pos[0]

        # Apply smoothing to mouse movement
        smoothing_factor = 0.5
        smoothed_dx = mouse_dx * smoothing_factor

        self.angle += smoothed_dx * self.sensitivity
        self.angle %= math.tau

        # Reset mouse position if it's near the edge of the screen
        if current_mouse_pos[0] <= 10 or current_mouse_pos[0] >= WIDTH - 10 or \
                current_mouse_pos[1] <= 10 or current_mouse_pos[1] >= HEIGHT - 10:
            pygame.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
            self.last_mouse_pos = (HALF_WIDTH, HALF_HEIGHT)
        else:
            self.last_mouse_pos = current_mouse_pos

    def move(self, dx, dy, game_map):
        if not game_map.is_wall(self.x + dx, self.y): self.x += dx
        if not game_map.is_wall(self.x, self.y + dy): self.y += dy

    def take_damage(self, amount):
        self.health -= amount
        self.last_hit_time = pygame.time.get_ticks()

    def regenerate_health(self, dt):
        if pygame.time.get_ticks() - self.last_hit_time > HEALTH_REGEN_DELAY:
            self.health = min(self.health + HEALTH_REGEN_RATE * dt, MAX_PLAYER_HEALTH)

    def reset(self):
        self.x = HALF_WIDTH
        self.y = HALF_HEIGHT
        self.angle = 0
        self.health = MAX_PLAYER_HEALTH
        self.last_hit_time = 0
        self.last_mouse_pos = (HALF_WIDTH, HALF_HEIGHT)