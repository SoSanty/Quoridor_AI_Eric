Quoridor - Game with Artificial Intelligence (AI) Description

Quoridor is a board game where two players compete to reach the opposite side of the board while using barriers to block the opponent’s path. This project is developed in Python and consists of three main modules:

    Game Logic (board, movements, move validation).
    Graphical User Interface (GUI) for user interaction.
    Main to manage the game flow, player input, and AI interaction.

In this project, we implemented a GUI for the game and an AI that manages the second player, allowing you to play against the computer. Additionally, a batch file has been created to streamline the game execution on Windows.
Features

    Two-player game: The game can be played by two players.
    Player vs AI: The second player can be controlled by an AI that makes decisions based on a predefined algorithm.
    Graphical User Interface (GUI): An intuitive GUI to play Quoridor, view the board, and interact with the game.
    Batch file for execution: A batch file (run_game.bat) that starts the game, manages the turns, and runs the GUI in the background.

Technologies Used

    Python: Programming language used for game logic, GUI, and AI.
    Artificial Intelligence: Implemented for the second player to simulate intelligent decisions.
    Batch file: A Windows batch script (run_game.bat) for starting the game and launching the GUI.

How to Play

    Run the run_game.bat file. This will start the game, launch the GUI in the background, and set up the game environment.
    The first player can make their moves using the GUI.
    The second player can be controlled by either another human player or by the AI.
    Players take turns moving their pieces and placing barriers.
    The game ends when a player reaches the opposite side of the board.

Running the Game
Prerequisites

    Ensure that Python 3 is installed on your system.
    Install the required Python packages if necessary.

To Run the Game:

    Double-click on the run_game.bat file. This will execute the batch file which will:
        Launch the GUI in the background.
        Start the main game logic.
        Prompt the user for input to control the game.

    Play the game either with a friend or against the AI.

File Structure

Quoridor/
│
├── board.py              # Game logic: board setup and movement rules
├── gui.py                # Graphical User Interface for the game
├── main.py               # Main game loop and interaction
├── ai.py                 # AI for the second player 
└── run_game.bat          # Batch file to run the game



Future Improvements

    Improve AI algorithms to make the computer play more intelligently.
    Add more customization options (board size, number of barriers, etc.).
    Implement an online multiplayer mode.
