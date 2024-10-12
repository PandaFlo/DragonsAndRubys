# Dragons and Rubys Game

**Dragons and Rubys** is a 2D game inspired by the classic Snake game. Players control a dragon that grows in size by collecting rubies scattered on the game board. The objective is to collect as many rubies as possible without crashing into the walls or the dragon’s own body. The game is built using Python and the `pygame` library for an interactive and fun experience.

## Features

- **Snake-inspired Gameplay**: Control a dragon that grows with each ruby collected.
- **Multiple Board Sizes**: Choose between small, medium, or large board sizes for varying levels of difficulty.
- **Random Ruby Placement**: Every game session places rubies randomly on the board, making each playthrough unique.
- **Customizable Game Settings**: You can modify the board size, game speed, and dragon colors for a personalized experience.
- **Smooth Game Experience**: The game runs in real-time, offering responsive controls for a fun, seamless experience.

## Requirements

- Python 3.x
- Pygame library

Install Pygame using:
```bash
pip install pygame
```

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/PandaFlo/DragonsAndRubys.git
    ```

2. Navigate into the project directory:
    ```bash
    cd DragonsAndRubys
    ```

3. Install the necessary dependencies:
    ```bash
    pip install pygame
    ```

4. Run the game:
    ```bash
    python dragon_ruby_game.py
    ```

## How to Play

1. When the game starts, you will be prompted to choose a board size: small, medium, or large.
2. Use the arrow keys to move the dragon in the desired direction.
3. Collect rubies to make the dragon grow.
4. Avoid hitting the walls or your dragon's body. If you do, the game will reset.

## Controls

- **Arrow Keys**: Move the dragon (Up, Down, Left, Right).
- **Q**: Pause the game and open the quit dialog.

## Customization

- **Board Size**: Modify the `get_game_size()` function in the source code to set custom board sizes.
- **Ruby Colors**: You can adjust the ruby’s appearance by changing the color values in the `cube` class for rubies.
- **Game Speed**: Adjust the delay and tick rate in the main game loop to change how fast the game plays.

## Future Enhancements

- **Improved AI**: Adding an AI-controlled dragon as a potential opponent.
- **Multiplayer Mode**: A feature allowing two players to compete locally.
- **Power-ups**: Introducing items that can temporarily change the game dynamics (e.g., speed boosts or invincibility).

