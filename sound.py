import pygame
from settings import *

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.load_sounds()
        self.music_volume = 0.2
        self.sfx_volume = 0.5

    def load_sounds(self):
        sound_files = {
            'shoot': SHOOT_SOUND_PATH,
            'reload': RELOAD_SOUND_PATH,
            'hit': HIT_SOUND_PATH,
            'enemy_death': ENEMY_DEATH_SOUND_PATH,
        }
        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error as e:
                print(f"Error loading sound {name}: {e}")

    def play_menu_music(self):
        self._play_music(MENU_MUSIC_PATH)

    def play_music(self):
        self._play_music(BACKGROUND_MUSIC_PATH)

    def _play_music(self, music_path):
        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing music: {e}")

    def set_music_volume(self, volume):
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Warning: Sound '{sound_name}' not loaded")

    def stop_music(self):
        pygame.mixer.music.stop()