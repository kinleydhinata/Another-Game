# Just Another Game by Kinley

## Overview

**Just Another Game by Kinley** is a first-person shooter (FPS) game built with Python and Pygame. It features shooting enemies, earning points, and navigating a grid-based map, along with a main menu and intuitive gameplay mechanics for an engaging experience. This game also features HSK background music to help players learn Mandarin while playing. Additionally, it uses raycasting to create a pseudo-3D visual effect, enhancing the immersive experience. The game aims to be web-playable using pygbag, but currently faces challenges, particularly with compatibility and stability. If you're experienced with pygbag and would like to help, please contribute or reach out!



## Features 🚀

- **Pseudo-3D Rendering**: Uses raycasting for an immersive, pseudo-3D visual effect.
- **Main Menu**: Start Game, Settings, Quit options.
- **Dynamic Sensitivity**: Adjustable mouse sensitivity for better control.
- **Real-time Combat**: Shoot enemies with sound effects.
- **Health and Ammo**: Manage health and ammo, with reloading options.
- **Game Map**: Navigate, avoid walls, and eliminate enemies.
- **Enemies**: Basic AI for movement and attacks.
- **UI Elements**: Dashboard showing health, ammo, and score.
- **Web-Playable**: Web compatibility using pygbag.

## Requirements 📦

- Python 3.x
- Pygame 2.5.2
- Pygbag 0.8.3

To install dependencies:

```sh
pip install -r requirements.txt
```

## File Structure 🗂️

- **main.py**: Main entry point, handling game flow.
- **main\_menu.py**: Implements the main menu.
- **player.py**: Manages player properties like movement and health.
- **enemy.py**: Handles enemy movement, damage, and animations.
- **weapon.py**: Manages shooting, reloading, and bullet interactions.
- **sound.py**: Handles game sounds.
- **map.py**: Defines the game map.
- **rendering.py**: Handles rendering the game world.
- **ui.py**: Manages UI elements like health and score.
- **game\_state.py**: Maintains game state including score and health.
- **pygbag\_main.py**: Sets up web compatibility.
- **index.html**: HTML for web deployment.
- **settings.py**: Contains game constants and configurations.
- **requirements.txt**: Lists dependencies.

## How to Play 🎮

1. **Launch the Game**: Run `main.py` using Python.
2. **Main Menu**: Start, adjust settings, or quit.
3. **Controls**:
   - **WASD 🕹️**: Move.
   - **Mouse 🖱️**: Aim.
   - **Left Click 🔫**: Shoot.
   - **R ♻️**: Reload.
   - **ESC 🚪**: Exit.
4. **Gameplay**: Navigate, shoot enemies, manage health and ammo, and achieve a high score.

## Contributing 🤝

Contributions are welcome!

1. Fork the repository.
2. Create a new branch.
3. Commit changes.
4. Push to the branch.
5. Open a Pull Request.

## License 📄

This project is licensed under the MIT License.

## Credits 🙏

Developed by Kinley with the help of Claude AI.

Assets are credited to their respective owners.

## Contact ✉️

For questions or suggestions, feel free to contact me or open an issue on the GitHub repository.
