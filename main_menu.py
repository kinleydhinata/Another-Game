import pygame
import asyncio
import math
from settings import *

class MainMenu:
    def __init__(self, screen, sound_manager, initial_sensitivity=0.0015):
        self.screen = screen
        self.sound_manager = sound_manager
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)

        self.title = self.font_large.render("Just Another Game by Kinley", True, (224, 224, 224))
        self.start_text = self.font_medium.render("Start Game", True, WHITE)
        self.settings_text = self.font_medium.render("Settings", True, WHITE)
        self.quit_text = self.font_medium.render("Quit", True, WHITE)

        self.start_rect = self.start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.settings_rect = self.settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 160))

        self.background = pygame.image.load(MENU_BACKGROUND_PATH).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.in_settings = False
        self.music_volume = 0.5
        self.sfx_volume = 0.5

        self.sensitivity_options = [
            ("Very Low", 0.0005),
            ("Low", 0.001),
            ("Medium Low", 0.0015),
            ("Medium", 0.002),
            ("Medium High", 0.0025),
            ("High", 0.003),
            ("Very High", 0.0035)
        ]
        self.sensitivity_index = self.find_closest_sensitivity(initial_sensitivity)
        self.sensitivity = self.sensitivity_options[self.sensitivity_index][1]

        self.scanline_surface = self.create_scanline_surface()
        self.vignette_surface = self.create_vignette_surface()

    async def run_async(self):
        self.sound_manager.play_menu_music()
        while True:
            self.draw()
            pygame.display.flip()
            action = await self.handle_events_async()
            if action:
                if action == 'start':
                    return action, self.sensitivity
                return action, None
            await asyncio.sleep(0)  # Allow other async tasks to run

    async def handle_events_async(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if not self.in_settings:
                        if self.start_rect.collidepoint(event.pos):
                            return 'start'
                        elif self.settings_rect.collidepoint(event.pos):
                            self.in_settings = True
                        elif self.quit_rect.collidepoint(event.pos):
                            return 'quit'
                    else:
                        if HEIGHT // 2 + 175 < event.pos[1] < HEIGHT // 2 + 225:
                            self.in_settings = False
                        elif HEIGHT // 2 + 85 < event.pos[1] < HEIGHT // 2 + 115:
                            if event.pos[0] < WIDTH // 2:
                                self.change_sensitivity(-1)
                            else:
                                self.change_sensitivity(1)
                        else:
                            self.handle_setting_change(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:  # Left mouse button held down
                    self.handle_setting_change(event.pos)
        await asyncio.sleep(0)  # Allow other async tasks to run
        return None

    def find_closest_sensitivity(self, target):
        return min(range(len(self.sensitivity_options)),
                   key=lambda i: abs(self.sensitivity_options[i][1] - target))

    def create_scanline_surface(self):
        scanline_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for y in range(0, HEIGHT, 4):
            pygame.draw.line(scanline_surface, (0, 0, 0, 50), (0, y), (WIDTH, y))
        return scanline_surface

    def create_vignette_surface(self):
        vignette_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for x in range(WIDTH):
            for y in range(HEIGHT):
                distance = math.sqrt((x - WIDTH // 2) ** 2 + (y - HEIGHT // 2) ** 2)
                max_distance = math.sqrt((WIDTH // 2) ** 2 + (HEIGHT // 2) ** 2)
                alpha = min(int(255 * (distance / max_distance) ** 1.5), 200)
                vignette_surface.set_at((x, y), (0, 0, 0, alpha))
        return vignette_surface

    def draw_glowing_text(self, text, position, base_color, glow_color, glow_amount=2):
        glow_surf = self.font_medium.render(text, True, glow_color)
        text_surf = self.font_medium.render(text, True, base_color)
        glow_size = int(glow_amount * 2)
        glow_surf = pygame.transform.scale(glow_surf,
                                           (glow_surf.get_width() + glow_size, glow_surf.get_height() + glow_size))
        text_rect = text_surf.get_rect(center=position)
        glow_rect = glow_surf.get_rect(center=position)
        self.screen.blit(glow_surf, glow_rect)
        self.screen.blit(text_surf, text_rect)

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if not self.in_settings:
            title_rect = self.title.get_rect(center=(WIDTH // 2, 100))
            self.screen.blit(self.title, title_rect)

            self.draw_glowing_text("Start Game", self.start_rect.center, WHITE, GREEN)
            self.draw_glowing_text("Settings", self.settings_rect.center, WHITE, GREEN)
            self.draw_glowing_text("Quit", self.quit_rect.center, WHITE, GREEN)
        else:
            self.draw_settings()

        self.screen.blit(self.scanline_surface, (0, 0))
        self.screen.blit(self.vignette_surface, (0, 0))

    def draw_settings(self):
        music_text = self.font_small.render(f"Music Volume: {int(self.music_volume * 100)}%", True, WHITE)
        sfx_text = self.font_small.render(f"SFX Volume: {int(self.sfx_volume * 100)}%", True, WHITE)
        sensitivity_text = self.font_small.render(f"Sensitivity: {self.sensitivity_options[self.sensitivity_index][0]}", True, WHITE)
        back_text = self.font_medium.render("Back", True, WHITE)

        music_rect = music_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        sfx_rect = sfx_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        sensitivity_rect = sensitivity_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

        self.screen.blit(music_text, music_rect)
        self.screen.blit(sfx_text, sfx_rect)
        self.screen.blit(sensitivity_text, sensitivity_rect)
        self.screen.blit(back_text, back_rect)

        pygame.draw.rect(self.screen, WHITE, (WIDTH // 4, HEIGHT // 2 - 75, WIDTH // 2, 10), 2)
        pygame.draw.rect(self.screen, WHITE, (WIDTH // 4, HEIGHT // 2 + 25, WIDTH // 2, 10), 2)

        left_arrow = self.font_medium.render("<", True, WHITE)
        right_arrow = self.font_medium.render(">", True, WHITE)
        self.screen.blit(left_arrow, (WIDTH // 4 - 30, HEIGHT // 2 + 85))
        self.screen.blit(right_arrow, (3 * WIDTH // 4 + 10, HEIGHT // 2 + 85))

        pygame.draw.circle(self.screen, GREEN,
                           (int(WIDTH // 4 + self.music_volume * WIDTH // 2), HEIGHT // 2 - 70), 15)
        pygame.draw.circle(self.screen, GREEN,
                           (int(WIDTH // 4 + self.sfx_volume * WIDTH // 2), HEIGHT // 2 + 30), 15)

    def handle_setting_change(self, pos):
        if HEIGHT // 2 - 80 < pos[1] < HEIGHT // 2 - 60:
            self.music_volume = max(0, min(1, (pos[0] - WIDTH // 4) / (WIDTH // 2)))
            self.sound_manager.set_music_volume(self.music_volume)
        elif HEIGHT // 2 + 20 < pos[1] < HEIGHT // 2 + 40:
            self.sfx_volume = max(0, min(1, (pos[0] - WIDTH // 4) / (WIDTH // 2)))
            self.sound_manager.set_sfx_volume(self.sfx_volume)

    def change_sensitivity(self, direction):
        self.sensitivity_index = (self.sensitivity_index + direction) % len(self.sensitivity_options)
        self.sensitivity = self.sensitivity_options[self.sensitivity_index][1]