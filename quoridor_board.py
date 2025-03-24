from collections import deque
from typing import List, Tuple, Set
import time
import json
import os


class QuoridorBoard:
    """
    Represents the Quoridor game board and its logic.
    
    Attributes:
        size (int): The board size (9x9 in standard Quoridor).
        player_positions (dict): Maps player number to their current position.
        fences (set): Tracks all placed fences as tuples ((x1, y1), (x2, y2), orientation).
        fences_gui (set): Subset of fences formatted for GUI rendering.
        game_state (dict): Stores current game state to be exported as JSON.
        fences_left (dict): Number of remaining walls for each player.
    """

    def __init__(self):
        """
        Initializes the Quoridor board, placing players at their start positions and resetting fences.
        Also deletes any previous game state JSON file to start fresh.
        """
        self.size = 9  # 9x9 Board
        self.player_positions = {1: (4, 0), 2: (4, 8)}  # Player 1 starts at (4,0), Player 2 at (4,8)
        self.fences = set()
        self.fences_gui = set()
        self.game_state = {}
        self.fences_left = {1: 10, 2: 10}  # Every player has 10 walls

        # Delete the game_state.json file if it exists
        if os.path.exists("game_state.json"):
            os.remove("game_state.json")  # Delete the file completely
            print("Game state file deleted.")

    def move_pawn(self, player: int, new_position: Tuple[int, int]) -> bool:
        """
        Moves the pawn of a given player to a new position, if the move is valid.

        Args:
            player (int): Player number (1 or 2).
            new_position (Tuple[int, int]): Desired position (x, y).

        Returns:
            bool: True if the move was valid and executed, False otherwise.
        """
        if not self.is_valid_pawn_move(player, new_position):
            return False

        self.player_positions[player] = new_position
        return True

    def is_valid_pawn_move(self, player: int, new_position: Tuple[int, int]) -> bool:
        """
        Validates if a pawn move is legal based on board boundaries and fence positions.

        Args:
            player (int): Player number (1 or 2).
            new_position (Tuple[int, int]): Desired position (x, y).

        Returns:
            bool: True if the move is allowed, False otherwise.
        """
        x, y = self.player_positions[player]
        new_x, new_y = new_position


        # Ensure the move is within board boundaries
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            print("Move is outside the board boundaries.")
            return False

        # Check for simple adjacent moves (orthogonal only)
        if (abs(new_x - x) == 1 and new_y == y) or (abs(new_y - y) == 1 and new_x == x):
            if self.is_fence_blocking(x, y, new_x, new_y):
                print("Fence is blocking the move.")
                return False
            print("Move is valid (simple adjacent).")
            return True

        print("Move is invalid (no valid conditions met).")
        return False

    def place_fence(self, x: int, y: int, orientation: str, player: int) -> bool:
        """
        Attempts to place a fence on the board for a given player.

        Args:
            x (int): Horizontal coordinate of the fence origin.
            y (int): Vertical coordinate of the fence origin.
            orientation (str): Fence orientation, either 'H' (horizontal) or 'V' (vertical).
            player (int): Player number (1 or 2).

        Returns:
            bool: True if fence placement was successful, False otherwise.
        """
        if self.fences_left[player] <= 0:
            return False

        # Check if a fence already exists in that location
        for wall in self.fences:
            coord1, coord2, orient = wall  # Unpack the wall coordinates and orientation
            if (coord1 == (x, y) or coord2 == (x, y)) and orient == orientation:  # 
                return False
            if coord1 == (x+1, y) and orient == orientation:
                return False
            if (coord1 == (x, y) and orient != orientation):  # Prevent crossing walls
                return False  # If there's a cross, return False

        # Handle horizontal fence placement
        if orientation == 'H':
            if y < 0 or y >= self.size - 1 or x < 0 or x >= self.size - 1:
                return False
            wall = ((x, y), (x + 1, y), 'H')

        # Handle vertical fence placement
        elif orientation == 'V':
            if x < 0 or x >= self.size - 1 or y < 0 or y >= self.size - 1:
                return False
            wall = ((x, y), (x, y + 1), 'V')

        self.fences.add(wall)
        print(f"Fences:{self.fences}")

        # Ensure both players still have a valid path to goal
        if not self.has_path_to_goal(1) or not self.has_path_to_goal(2):
            self.fences.remove((wall))
            return False

        self.fences_left[player] -= 1
        return True

    def is_fence_blocking(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """
        Determines if a fence blocks the move between two adjacent cells.

        Args:
            x1, y1, x2, y2 (int): Coordinates of the movement direction.

        Returns:
            bool: True if the path is blocked by a fence, False otherwise.
        """
        for wall in self.fences:
            (fx1, fy1), (fx2, fy2), orient = wall

            if orient == 'H':
                if ((y1 > y2 and (fx1, fy1) == (x1, y2)) or (y2 > y1 and (fx1, fy1) == (x1, y1)) or
                    (y1 > y2 and (fx2, fy2) == (x1, y2)) or (y2 > y1 and (fx2, fy2) == (x1, y1))):
                    return True

            elif orient == 'V':
                if ((x1 > x2 and (fx1, fy1) == (x2, y1)) or (x2 > x1 and (fx1, fy1) == (x1, y1)) or
                    (x1 > x2 and (fx2, fy2) == (x2, y1)) or (x2 > x1 and (fx2, fy2) == (x1, y1))):
                    return True

        return False

    def has_path_to_goal(self, player: int) -> bool:
        """
        Uses DFS to determine if a player still has a valid path to their goal row.

        Args:
            player (int): Player number (1 or 2).

        Returns:
            bool: True if a path exists, False if blocked.
        """
        start_x, start_y = self.player_positions[player]
        goal_row = 8 if player == 1 else 0
        stack = [(start_x, start_y)]
        visited = set()

        while stack:
            x, y = stack.pop()

            if (player == 1 and y == goal_row) or (player == 2 and y == goal_row):
                return True

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Explore adjacent tiles
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                    if not self.is_fence_blocking(x, y, nx, ny):
                        stack.append((nx, ny))

        print(f'Player {player} has no path to goal.')
        return False

    def update_gui_game_state(self):
        """
        Serializes and saves the current game state to a JSON file,
        so that the GUI component can read and reflect the latest status.
        """
        walls = list(self.fences)
        for wall in walls:
            coord1, coord2, orient = wall
            x, y = coord1
            self.fences_gui.add((x, y, orient))

        player1 = self.player_positions[1]
        player2 = self.player_positions[2]

        self.game_state = {
            "player_positions": {"player1": player1, "player2": player2},
            "walls": list(self.fences_gui),
            "walls_remaining": {
                "player_1": self.fences_left[1],
                "player_2": self.fences_left[2]
            },
            "turn": "player1",
            "board": []
        }

        with open("game_state.json", "w") as file:
            json.dump(self.game_state, file)

        print("Game state saved to file:", self.game_state)
