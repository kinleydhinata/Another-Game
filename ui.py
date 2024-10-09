import pygame
import asyncio
from settings import *

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 36)
        self.small_font = pygame.font.SysFont('Arial', 24)

    def draw_dashboard(self, player, weapon_system, game_state):
        pygame.draw.rect(self.screen, DASHBOARD_COLOR, (0, HEIGHT - DASHBOARD_HEIGHT, WIDTH, DASHBOARD_HEIGHT))
        self.draw_health_bar(player)
        self.draw_ammo(weapon_system)
        self.draw_score(game_state)
        self.draw_crosshair()
        self.draw_instructions()

    def draw_health_bar(self, player):
        health_bar_width = 200
        health_bar_height = 25
        health_ratio = player.health / MAX_PLAYER_HEALTH
        pygame.draw.rect(self.screen, RED, (20, HEIGHT - DASHBOARD_HEIGHT + 20, health_bar_width * health_ratio, health_bar_height))
        pygame.draw.rect(self.screen, WHITE, (20, HEIGHT - DASHBOARD_HEIGHT + 20, health_bar_width, health_bar_height), 2)

    def draw_ammo(self, weapon_system):
        ammo_text = self.font.render(f'Ammo: {weapon_system.current_ammo}/{MAGAZINE_SIZE}', True, WHITE)
        self.screen.blit(ammo_text, (250, HEIGHT - DASHBOARD_HEIGHT + 15))

    def draw_score(self, game_state):
        score_text = self.font.render(f'Score: {game_state.score}', True, WHITE)
        self.screen.blit(score_text, (WIDTH - 220, HEIGHT - DASHBOARD_HEIGHT + 15))

    def draw_crosshair(self):
        pygame.draw.line(self.screen, WHITE, (HALF_WIDTH - 15, HALF_HEIGHT), (HALF_WIDTH + 15, HALF_HEIGHT), 2)
        pygame.draw.line(self.screen, WHITE, (HALF_WIDTH, HALF_HEIGHT - 15), (HALF_WIDTH, HALF_HEIGHT + 15), 2)

    def draw_instructions(self):
        instructions = ["WASD: Move", "Mouse: Aim", "Left Click: Shoot", "R: Reload", "ESC: Exit"]
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, WHITE)
            self.screen.blit(text, (20, HEIGHT - DASHBOARD_HEIGHT + 60 + i * 20))

    async def show_game_over_async(self, game_state):
        self.screen.fill(BLACK)
        game_over_text = self.font.render('GAME OVER', True, RED)
        restart_text = self.font.render('Press R to Restart or Q to Quit', True, WHITE)
        final_score_text = self.font.render(f'Final Score: {game_state.score}', True, WHITE)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT - 100)))
        self.screen.blit(restart_text, restart_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT)))
        self.screen.blit(final_score_text, final_score_text.get_rect(center=(HALF_WIDTH, HALF_HEIGHT + 100)))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        return False
            await asyncio.sleep(0)  # Allow other async tasks to run
        return False