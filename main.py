import asyncio
import sys
import traceback

print("main.py: Starting imports", file=sys.stderr)
import pygame
from settings import *
from player import Player
from enemy import EnemyManager
from weapon import WeaponSystem
from map import GameMap
from rendering import Renderer
from ui import UI
from sound import SoundManager
from game_state import GameState
from main_menu import MainMenu
print("main.py: Imports completed", file=sys.stderr)

class Game:
    def __init__(self):
        print("main.py: Initializing game...", file=sys.stderr)
        self.screen = None
        self.clock = None
        self.sound_manager = None
        self.main_menu = None
        self.sensitivity = 0.002
        print("main.py: Game object initialized", file=sys.stderr)

    async def async_init(self):
        try:
            print("main.py: Starting async initialization...", file=sys.stderr)
            await asyncio.sleep(0)
            print("main.py: Initializing Pygame", file=sys.stderr)
            pygame.init()
            print("main.py: Pygame initialized", file=sys.stderr)
            pygame.mouse.set_visible(True)
            print(f"main.py: Setting display mode: {WIDTH}x{HEIGHT}", file=sys.stderr)
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            print("main.py: Display set", file=sys.stderr)
            pygame.display.set_caption("Just Another Game by Kinley")
            self.clock = pygame.time.Clock()
            print("main.py: Creating SoundManager", file=sys.stderr)
            self.sound_manager = SoundManager()
            print("main.py: SoundManager created", file=sys.stderr)
            print("main.py: Creating MainMenu", file=sys.stderr)
            self.main_menu = MainMenu(self.screen, self.sound_manager)
            print("main.py: MainMenu created", file=sys.stderr)
        except Exception as e:
            print(f"main.py: Error in async_init: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    async def run_async(self):
        try:
            print("main.py: Starting run_async", file=sys.stderr)
            await self.async_init()
            print("main.py: Async initialization completed", file=sys.stderr)
            while True:
                print("main.py: In main game loop", file=sys.stderr)
                action, sensitivity = await self.main_menu.run_async()
                print(f"main.py: Menu action: {action}, sensitivity: {sensitivity}", file=sys.stderr)
                if action == 'start':
                    if sensitivity is not None:
                        self.sensitivity = sensitivity
                    self.initialize_game_objects()
                    await self.game_loop_async()
                elif action == 'quit':
                    break
                await asyncio.sleep(0)
        except Exception as e:
            print(f"main.py: Error in run_async: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        finally:
            print("main.py: Exiting game", file=sys.stderr)
            pygame.quit()

    def initialize_game_objects(self):
        try:
            print("Initializing game objects...", file=sys.stderr)
            self.game_map = GameMap()
            self.player = Player(HALF_WIDTH, HALF_HEIGHT, sensitivity=self.sensitivity)
            self.enemy_manager = EnemyManager(self.game_map)
            self.weapon_system = WeaponSystem()
            self.renderer = Renderer(self.screen, self.game_map)
            self.ui = UI(self.screen)
            self.game_state = GameState()
            print("Game objects initialized", file=sys.stderr)
        except Exception as e:
            print(f"Error in initialize_game_objects: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    async def game_loop_async(self):
        print("Starting gameplay loop", file=sys.stderr)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.sound_manager.play_music()
        try:
            while True:
                if not self.handle_events():
                    break
                self.update()
                self.render()
                if self.game_state.is_game_over():
                    if await self.game_over_async():
                        self.reset_game()
                    else:
                        break
                await asyncio.sleep(0)
                self.clock.tick(FPS)
        except Exception as e:
            print(f"Error in game_loop_async: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        finally:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            print("Exiting gameplay loop", file=sys.stderr)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.weapon_system.reload(self.sound_manager)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.weapon_system.shoot(self.player, self.sound_manager)
        if pygame.mouse.get_pressed()[0]:
            self.weapon_system.shoot(self.player, self.sound_manager)
        return True

    def update(self):
        self.player.update(self.game_map)
        self.enemy_manager.update(self.player, self.game_map, self.game_state, self.sound_manager)
        self.weapon_system.update(self.player, self.enemy_manager.enemies, self.game_state, self.sound_manager, self.game_map)
        self.game_state.update(self.player, self.clock.get_time() / 1000)

    def render(self):
        try:
            self.renderer.render(self.player, self.enemy_manager.enemies, self.weapon_system)
            self.ui.draw_dashboard(self.player, self.weapon_system, self.game_state)
            pygame.display.flip()
            print("Frame rendered", file=sys.stderr)
        except Exception as e:
            print(f"Error in render: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    async def game_over_async(self):
        return await self.ui.show_game_over_async(self.game_state)

    def reset_game(self):
        self.player.reset()
        self.enemy_manager.reset()
        self.weapon_system.reset()
        self.game_state.reset()

print("main.py: Game class defined", file=sys.stderr)

if __name__ == '__main__':
    print("main.py: Creating Game instance", file=sys.stderr)
    game = Game()
    print("main.py: Running game", file=sys.stderr)
    asyncio.run(game.run_async())
    print("main.py: Game execution completed", file=sys.stderr)