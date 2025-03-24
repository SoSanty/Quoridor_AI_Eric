Quoridor AI Game

What is Quoridor?

Quoridor is a strategic board game for two players, where the goal is to move your pawn to the opposite side of the board before your opponent. Players can either move their pawn or place walls to block the opponent, making the game a tactical challenge between mobility and defense.


Implementation

We have developed Quoridor in Python with a well-structured logic divided into four main components:

    MainGame → Manages the game flow and allows user interaction.

    QuoridorBoard → Handles board logic, validates moves, and manages barrier placements.

    GUI → Implemented using Pygame, it provides a visual interface and updates the game in real time.

    AI → A computer opponent capable of playing against the user by making strategic decisions based on the board state.


How to Play

To start the game, open two separate terminals:
1. Start the GUI

In the first terminal, run the following command to launch the graphical interface:

python gui.py

2. Start the Main Game

In the second terminal, run:

python main.py

Now you can play against the AI! In the MainGame terminal, you will be prompted to:

    Move your pawn by typing M and entering the coordinates.

    Place a barrier by typing F and specifying the position and orientation (H for horizontal, V for vertical).



Requirements

Ensure that Python 3 is installed on your system.

To run the game, ensure you have the following Python libraries installed:

pip install pygame


AI Player

Our AI Player analyzes the board and makes strategic decisions to try and win the game. It can either move optimally or place barriers to block the human player.

Objective

Win by reaching the opposite side before the AI… if you can! Have fun!
