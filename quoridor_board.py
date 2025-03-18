from collections import deque
from typing import List, Tuple, Set

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
        self.player_positions = {1: (5, 1), 2: (4, 8)}  # Player 1 starts at (4,0), Player 2 at (4,8)
        self.fences = set()
    
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

        print(f"Player {player} at ({x}, {y}) attempting to move to ({new_x}, {new_y})")

        # Ensure the move is within board boundaries
        if not (0 <= new_x < self.size and 0 <= new_y < self.size):
            print("Move is outside the board boundaries.")
            return False

        # Check for simple adjacent moves
        if (abs(new_x - x) == 1 and new_y == y) or (abs(new_y - y) == 1 and new_x == x):
            print("Checking for simple adjacent move.")
            if self.is_fence_blocking(x, y, new_x, new_y):
                print("Fence is blocking the move.")
                return False
            print("Move is valid (simple adjacent).")
            return True

        # Check for jump moves over opponent
        opponent = 2 if player == 1 else 1
        ox, oy = self.player_positions[opponent]
        print(f"Opponent at ({ox}, {oy})")

        # Check if the opponent is directly in front of the player
        if (ox == x and abs(oy - y) == 1):  # Opponent is directly in front
            print("Opponent is directly in front. Checking for jump.")
            jump_x, jump_y = x, 2 * oy - y  # Calculate jump position
            if (0 <= jump_x < self.size and 0 <= jump_y < self.size):  # Ensure jump is within bounds
                if not self.is_fence_blocking(x, y, ox, oy) and not self.is_fence_blocking(ox, oy, jump_x, jump_y):
                    print("Move is valid (jump over opponent).")
                    return True

        # Check for side-stepping (if a fence prevents straight jump)
        if (x, y) == (ox, oy - 1) and (new_x, new_y) in [(ox - 1, oy), (ox + 1, oy)]:
            print("Checking for side-step move.")
            if self.is_fence_blocking(x, y, ox, oy):
                print("Fence is blocking the side-step (first segment).")
                return False
            if self.is_fence_blocking(ox, oy, new_x, new_y):
                print("Fence is blocking the side-step (second segment).")
                return False
            print("Move is valid (side-step).")
            return True

        if (x, y) == (ox, oy + 1) and (new_x, new_y) in [(ox - 1, oy), (ox + 1, oy)]:
            print("Checking for side-step move.")
            if self.is_fence_blocking(x, y, ox, oy):
                print("Fence is blocking the side-step (first segment).")
                return False
            if self.is_fence_blocking(ox, oy, new_x, new_y):
                print("Fence is blocking the side-step (second segment).")
                return False
            print("Move is valid (side-step).")
            return True

        print("Move is invalid (no valid conditions met).")
        return False
    
    def place_fence(self, x: int, y: int, orientation: str) -> bool:
        """
        Places a fence if valid, with adjusted coordinate placement for horizontal and vertical fences.
        
        Args:
            x (int): The x-coordinate of the fence (or y for vertical).
            y (int): The y-coordinate of the fence (or x for vertical).
            orientation (str): 'H' for horizontal, 'V' for vertical.
        
        Returns:
            bool: True if the fence was placed, False otherwise.
        """
        
        # Check if any wall in self.fences has the same first coordinate
        for wall in self.fences:
            coord1, coord2, orient = wall  # Unpack the wall coordinates and orientation
            if coord1 == (x, y) or coord2== (x, y):  # If the first coordinate matches, return False
                return False
            if (coord1 == (x, y) and orient != orientation):  # Prevent crossing walls
                    return False  # If there's a cross, return False

        # Handle horizontal fence placement (between (x, y) and (x, y+1))
        if orientation == 'H':
            if y < 0 or y >= self.size - 1 or x < 0 or x >= self.size:
                return False  # Ensure coordinates are valid for horizontal placement
            wall = ((x, y), (x + 1, y), 'H')

        # Handle vertical fence placement (between (x, y) and (x+1, y))
        elif orientation == 'V':
            if x < 0 or x >= self.size - 1 or y < 0 or y >= self.size:
                return False  # Ensure coordinates are valid for vertical placement
            wall = ((x, y), (x , y + 1), 'V')
        
        # Add the new wall to the fence set
        self.fences.add(wall)
        print(self.fences)
        # Ensure both players still have a path to their goal
        if not self.has_path_to_goal(1) or not self.has_path_to_goal(2):
            # Undo the fence placement if it blocks paths
            self.fences.remove((wall))
            return False


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
                # Horizontal wall blocks vertical movement only
                if (x1 == x2 and fx1 == x1 - 1 and fy1 == min(y1, y2)):
                    return True  # Moving upward but blocked
                if (x1 == x2 and fx1 == x1 and fy1 == min(y1, y2)):
                    return True  # Moving downward but blocked

            elif orient == 'V':
                # Vertical wall blocks horizontal movement only
                if (y1 == y2 and fy1 == y1 - 1 and fx1 == min(x1, x2)):
                    return True  # Moving left but blocked
                if (y1 == y2 and fy1 == y1 and fx1 == min(x1, x2)):
                    return True  # Moving right but blocked

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
                print(f"Already visited ({x}, {y})")
                continue
            visited.add((x, y))
            print(f"Visiting ({x}, {y})")

            # Check all possible moves (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and (nx, ny) not in visited:
                    if not self.is_fence_blocking(x, y, nx, ny):  
                        stack.append((nx, ny))  # Add to stack for DFS
                    elif self.is_fence_blocking(x, y, nx, ny):
                        print(f"Blocked by fence at ({nx}, {ny})")

        print(f'Player {player} has no path to goal.')
        # If we exit the loop, no valid path was found
        return False
    
    def display_board(self):
    # Create an empty grid with spaces for walls
        board_display = [[' ' for _ in range(self.size * 2 - 1)] for _ in range(self.size * 2 - 1)]
        # Place players
        for player, (x, y) in self.player_positions.items():
            board_display[y * 2][x * 2] = 'P'  # Players centered on the board
        # Place fences
        for (x1, y1), (x2, y2), orientation in self.fences:
            if orientation == 'H':  # Horizontal wall
                board_display[y1 * 2 + 1][x1 * 2] = '--'  # Place between two tiles horizontally
                board_display[y1 * 2 + 1][x1 * 2 + 1] = '--'  # Extend the wall
            elif orientation == 'V':  # Vertical wall
                board_display[y1 * 2][x1 * 2 + 1] = '|'  # Place between two tiles vertically
                board_display[y1 * 2 + 1][x1 * 2 + 1] = '|'  # Extend the wall
        # Print the board
        for row in board_display:
            print(''.join(row))
        print('\n')

# Example Usage
if __name__ == "__main__":
    board = QuoridorBoard()
    board.display_board()
    board.move_pawn(1, (4, 1))  # Move Player 1 forward
    board.display_board()
    board.place_fence(4, 4, 'H')  # Place horizontal fence
    board.display_board()
