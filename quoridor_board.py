from collections import deque
from typing import List, Tuple, Set
import time
import json
import os


class QuoridorBoard:
    """
    Represents the Quoridor game board.
    
    Attributes:
        size (int): The board size (9x9 in standard Quoridor).
        player_positions (dict): Stores the positions of the two players.
        fences (set): Stores placed fences as tuples (x, y, orientation).
    """
    
    def __init__(self):
        """Initializes the Quoridor board with starting positions and an empty fence set."""
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
        Moves a player's pawn if the move is valid.
        
        Args:
            player (int): The player number (1 or 2).
            new_position (Tuple[int, int]): The target position (x, y).
        
        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if not self.is_valid_pawn_move(player, new_position):
            return False
        
        self.player_positions[player] = new_position
        return True
    
    def is_valid_pawn_move(self, player: int, new_position: Tuple[int, int]) -> bool:
        """
        Checks if a pawn move is valid based on adjacency and fence restrictions.
        """
        x, y = self.player_positions[player]
        new_x, new_y = new_position


        
        # Ensure the move is within board boundaries
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            print("Move is outside the board boundaries.")
            return False

        # Check for simple adjacent moves
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
        Places a fence if valid, with adjusted coordinate placement for horizontal and vertical fences.
        
        Args:
            x (int): The x-coordinate of the fence (or y for vertical).
            y (int): The y-coordinate of the fence (or x for vertical).
            orientation (str): 'H' for horizontal, 'V' for vertical.
        
        Returns:
            bool: True if the fence was placed, False otherwise.
        """
        if self.fences_left[player] <= 0:
            return False


        # Check if any wall in self.fences has the same first coordinate
        for wall in self.fences:
            coord1, coord2, orient = wall  # Unpack the wall coordinates and orientation
            if (coord1 == (x, y) or coord2 == (x, y)) and orient == orientation:  # 
                return False
            if coord1 == (x+1, y) and orient == orientation:
                return False
            if (coord1 == (x, y) and orient != orientation):  # Prevent crossing walls
                return False  # If there's a cross, return False

        # Handle horizontal fence placement (between (x, y) and (x, y+1))
        if orientation == 'H':
            if y < 0 or y >= self.size - 1 or x < 0 or x >= self.size - 1:
                return False  # Ensure coordinates are valid for horizontal placement
            wall = ((x, y), (x + 1, y), 'H')

        # Handle vertical fence placement (between (x, y) and (x+1, y))
        elif orientation == 'V':
            if x < 0 or x >= self.size - 1 or y < 0 or y >= self.size - 1:
                return False  # Ensure coordinates are valid for vertical placement
            wall = ((x, y), (x , y + 1), 'V')
        
        # Add the new wall to the fence set
        self.fences.add(wall)
        # Ensure both players still have a path to their goal
        if not self.has_path_to_goal(1) or not self.has_path_to_goal(2):
            # Undo the fence placement if it blocks paths
            self.fences.remove((wall))
            return False

        # **Decreases the number of remaining walls**
        self.fences_left[player] -= 1

        return True
    
    def is_fence_blocking(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """
        Checks if a fence blocks movement between two positions.

        Args:
        x1, y1, x2, y2 (int): The coordinates of the move.

        Returns:
        bool: True if a fence is blocking, False otherwise.
        """
        for wall in self.fences:
            (fx1, fy1), (fx2, fy2), orient = wall

            if orient == 'H':  
                # Horizontal walls block vertical movement (up/down)
                if ((y1 > y2 and (fx1, fy1) == (x1, y2)) or (y2 > y1 and (fx1, fy1) == (x1, y1)) or
                    (y1 > y2 and (fx2, fy2) == (x1, y2)) or (y2 > y1 and (fx2, fy2) == (x1, y1))):
                    return True  # Moving up or down but blocked

            elif orient == 'V':  
                # Vertical walls block horizontal movement (left/right)
                if ((x1 > x2 and (fx1, fy1) == (x2, y1)) or (x2 > x1 and (fx1, fy1) == (x1, y1)) or
                    (x1 > x2 and (fx2, fy2) == (x2, y1)) or (x2 > x1 and (fx2, fy2) == (x1, y1))):
                    return True  # Moving left or right but blocked

        return False
    
    def has_path_to_goal(self, player: int) -> bool:
        """
        Checks if a player has a path to their goal using DFS.
        
        Args:
            player (int): The player (1 or 2).
        
        Returns:
            bool: True if there is a valid path, False if blocked.
        """
        start_x, start_y = self.player_positions[player]
        goal_row = 8 if player == 1 else 0  # Player 1 must reach row 8, Player 2 must reach row 0
        stack = [(start_x, start_y)]  # Use a stack for DFS
        visited = set()

        while stack:
            x, y = stack.pop()

            # If we reach any tile in the goal row, there is a valid path
            if (player == 1 and y == goal_row) or (player == 2 and y == goal_row):
                return True

            if (x, y) in visited:
                continue
            visited.add((x, y))

            # Check all possible moves (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                    if not self.is_fence_blocking(x, y, nx, ny):  
                        stack.append((nx, ny))  # Add to stack for DFS

        # If we exit the loop, no valid path was found
        return False
    
    def update_gui_game_state(self):
        """Saves the game state to a JSON file."""

        walls = list(self.fences)
        for wall in walls:
            coord1, coord2, orient = wall
            x , y = coord1
            self.fences_gui.add((x, y, orient))

        player1 = self.player_positions[1]
        player2 = self.player_positions[2]

        self.game_state = {
        "player_positions": {"player1": player1, "player2": player2},
        "walls": list(self.fences_gui),  # Lista dei muri
        "walls_remaining": {
            "player_1": self.fences_left[1],  # Walls left for player 1
            "player_2": self.fences_left[2]   # Walls left for player 1
        },
        "turn": "player1",  # Actual turn
        "board": []  # Board state
    }

        with open("game_state.json", "w") as file:
            json.dump(self.game_state, file)
