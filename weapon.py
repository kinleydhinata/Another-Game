import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self):
        self.x += math.cos(self.angle) * BULLET_SPEED
        self.y += math.sin(self.angle) * BULLET_SPEED

    def check_collision(self, game_map):
        return game_map.is_wall(self.x, self.y)

class WeaponSystem:
    def __init__(self):
        self.bullets = []
        self.current_ammo = MAGAZINE_SIZE
        self.last_shot_time = 0
        self.last_reload_time = 0
        self.weapon_state = 'idle'
        self.last_state_change = 0
        self.weapon_idle = pygame.image.load(WEAPON_IDLE_PATH).convert_alpha()
        self.weapon_shoot = pygame.image.load(WEAPON_SHOOT_PATH).convert_alpha()

    def update(self, player, enemies, game_state, sound_manager, game_map):
        current_time = pygame.time.get_ticks()
        if self.weapon_state == 'shoot' and current_time - self.last_state_change > WEAPON_ANIMATION_TIME:
            self.weapon_state = 'idle'

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.check_collision(game_map):
                self.bullets.remove(bullet)
            else:
                for enemy in enemies[:]:
                    if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < TILE // 3:
                        enemy.take_damage(20)
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            game_state.increment_score(100)
                            sound_manager.play_sound('enemy_death')
                        self.bullets.remove(bullet)
                        break

    def shoot(self, player, sound_manager):
        current_time = pygame.time.get_ticks()
        if self.current_ammo > 0 and current_time - self.last_shot_time > FIRE_RATE:
            self.bullets.append(Bullet(player.x, player.y, player.angle))
            self.current_ammo -= 1
            self.last_shot_time = current_time
            self.weapon_state = 'shoot'
            self.last_state_change = current_time
            sound_manager.play_sound('shoot')

    def reload(self, sound_manager):
        current_time = pygame.time.get_ticks()
        if self.current_ammo < MAGAZINE_SIZE and current_time - self.last_reload_time > RELOAD_TIME:
            self.current_ammo = MAGAZINE_SIZE
            self.last_reload_time = current_time
            sound_manager.play_sound('reload')

    def get_weapon_image(self):
        return self.weapon_shoot if self.weapon_state == 'shoot' else self.weapon_idle

    def reset(self):
        self.bullets.clear()
        self.current_ammo = MAGAZINE_SIZE
        self.last_shot_time = 0
        self.last_reload_time = 0
        self.weapon_state = 'idle'
        self.last_state_change = 0