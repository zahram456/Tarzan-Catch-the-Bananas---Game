# Tarzan: Catch the Bananas

A fullscreen Pygame arcade game where you control Tarzan to catch falling bananas, dodge coconuts, and collect power-ups while the difficulty ramps across jungle levels.

## Features
- Menu, settings, pause, and game over flows
- Randomized falling objects: bananas, coconuts, golden bananas, hearts, shields
- Power-ups that boost score multiplier, add lives, or grant a temporary shield
- Dynamic difficulty scaling and three background levels
- Music and sound effects with toggles
- Persistent high-score tracking

## Controls
- Left/Right Arrow: Move
- P: Pause/Resume
- R: Restart after game over
- Esc: Quit

## Requirements
- Python 3.x
- pygame

## Setup
```powershell
pip install pygame
```

## Run
```powershell
python main.py
```

## Assets
Game assets are loaded from `images/` and `sounds/` folders in the project directory.

## Notes
The game stores the high score in `highscore.txt` in the project root.
