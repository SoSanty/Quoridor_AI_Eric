import os
import json
from quoridor_board import QuoridorBoard
import heapq

class AI:
    """Class that handles AI decision-making in Quoridor."""

    def __init__(self, board):
        """Initialize the AI agent and load the game state."""
        self.board = board  # Create an instance of the game board
        self.game_state = {}
        self.game_state = self.read_game_state()  # Ensure game state is loaded or initialized

    def read_game_state(self):
        """Reads the latest game state from the JSON file or initializes a new one if the file does not exist."""
        try:
            with open("game_state.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error reading game_state.json. Recreating the game state...")
            return self.game_state

    def get_valid_moves(self, player):
        """Returns a list of valid moves for the given player based on the current game state."""
        if not self.game_state:
            return []

        player_position = self.game_state["player_positions"].get(f"player{player}", None)
        if not player_position:
            return []

        x, y = player_position
        possible_moves = [
            (x, y - 1),  # Up
            (x, y + 1),  # Down
            (x - 1, y),  # Left
            (x + 1, y)   # Right
        ]

        valid_moves = []
        for nx, ny in possible_moves:
            if 0 <= nx < 9 and 0 <= ny < 9:  # Ensure the move is inside the board
                if not self.board.is_fence_blocking(x, y, nx, ny):
                    valid_moves.append((nx, ny))
                else:
                    print(f"Move to ({nx}, {ny}) is blocked by a fence.")

        return valid_moves

    def get_valid_fences(self):
        """Returns a list of valid fences the AI can place."""
        valid_fences = []
        print(self.game_state)
        # Assume that self.game_state is already defined and contains the "walls" key.
        walls = self.game_state.get("walls", [])  # Get the list of walls from game state (default empty list)

        # Convert walls from lists to tuples for proper comparison
        walls_set = {tuple(wall) for wall in walls}  # Convert walls to a set of tuples for efficient comparison

        valid_fences = []  # List to store valid fences

        # Iterate through the possible fence locations and orientations
        for x in range(8):  # From 0 to 7 because a fence is placed between two squares
            for y in range(8):
                for orientation in ["H", "V"]:  # Horizontal or Vertical fence
                    if orientation == "H":
                        # Check if the horizontal fence at (x, y) is valid (not blocked by a wall)
                        if (x, y, orientation) not in walls_set and (x + 1, y, orientation) not in walls_set and (x - 1, y, orientation) not in walls_set and (x,y,'V') not in walls_set:
                            valid_fences.append((x, y, orientation))  # Add valid horizontal fence
                    if orientation == "V":
                        # Check if the vertical fence at (x, y) is valid (not blocked by a wall)
                        if (x, y, orientation) not in walls_set and (x, y + 1, orientation) not in walls_set and (x, y - 1, orientation) not in walls_set and (x,y,'H') not in walls_set:
                            valid_fences.append((x, y, orientation))  # Add valid vertical fence
        return valid_fences

    def heuristic(self, player):
        """Evaluates the game state based on A* shortest paths."""
        opponent = 2 if player == 1 else 1

        player_path = self.find_shortest_path(player)
        opponent_path = self.find_shortest_path(opponent)

        player_distance = len(player_path)-1 if player_path else float('inf')
        opponent_distance = len(opponent_path)-1 if opponent_path else float('inf')

        # Include the number of walls placed as a factor in the heuristic
        player_walls = self.game_state.get("player_walls", {}).get(f"player{player}", 0)
        opponent_walls = self.game_state.get("player_walls", {}).get(f"player{opponent}", 0)

        # Adjust the heuristic to consider the impact of walls more significantly
        return opponent_distance - player_distance + (player_walls - opponent_walls) * 0.5  # AI wants a larger gap in its favor

    def minimax(self, depth, alpha, beta, maximizing_player, player):
            if depth == 0:
                return self.heuristic(player)  # Valutiamo lo stato con l'euristica

            valid_moves = self.get_valid_moves(player)
            if not valid_moves:
                return -1000  # Se non ci sono mosse valide, pessimo punteggio

            if maximizing_player:
                max_eval = -float('inf')
                for move in valid_moves:
                    original_position = self.game_state["player_positions"][f"player{player}"]
                    self.game_state["player_positions"][f"player{player}"] = move  # Simula la mossa

                    eval = self.minimax(depth - 1, alpha, beta, False, 2 if player == 1 else 1)

                    self.game_state["player_positions"][f"player{player}"] = original_position  # Reset mossa
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Pruning
                return max_eval
            else:
                min_eval = float('inf')
                for move in valid_moves:
                    original_position = self.game_state["player_positions"][f"player{player}"]
                    self.game_state["player_positions"][f"player{player}"] = move  # Simula la mossa

                    eval = self.minimax(depth - 1, alpha, beta, True, 2 if player == 1 else 1)

                    self.game_state["player_positions"][f"player{player}"] = original_position  # Reset mossa
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Pruning
                return min_eval

    def find_shortest_path(self, player):
        """Trova il percorso più breve per il giocatore evitando i muri usando A*."""
        start = tuple(self.game_state["player_positions"][f"player{player}"])
        goal_y = 8 if player == 1 else 0  # Riga vincente

        queue = []
        heapq.heappush(queue, (0, start))  # (costo stimato, posizione)
        came_from = {start: None}
        cost_so_far = {start: 0}

        while queue:
            _, current = heapq.heappop(queue)

            if current[1] == goal_y:
                break  # Arrivati alla destinazione

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Su, giù, sinistra, destra
                next_pos = (current[0] + dx, current[1] + dy)

                if 0 <= next_pos[0] < 9 and 0 <= next_pos[1] < 9:  # Dentro i limiti del board
                    if not self.board.is_fence_blocking(current[0], current[1], next_pos[0], next_pos[1]):
                        new_cost = cost_so_far[current] + 1
                        if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                            cost_so_far[next_pos] = new_cost
                            priority = new_cost + abs(goal_y - next_pos[1])  # Heuristica di distanza
                            heapq.heappush(queue, (priority, next_pos))
                            came_from[next_pos] = current

        if goal_y not in [pos[1] for pos in cost_so_far.keys()]:  
            print(" No possible path found!")
            return []

        path = []
        current = min(cost_so_far.keys(), key=lambda pos: abs(goal_y - pos[1]))  
        while current is not None:
            path.append(current)
            current = came_from[current]

        path.reverse()
        return path


    def choose_move(self, player):
        """Selects the best move using A* for the shortest path and Minimax for strategic decisions."""
        
        valid_moves = self.get_valid_moves(player)
        valid_fences = self.get_valid_fences()

        if not valid_moves and not valid_fences:
            print("❌ No valid moves or fences available.")
            return None  # No possible action

        # 🔍 1. Use A* to find the shortest path
        path = self.find_shortest_path(player)
        a_star_move = None
        if len(path) > 1:
            next_step = path[1]
            if next_step in valid_moves:
                a_star_move = ("move", next_step)  # Save the best A* move (don't return yet!)
        
        print(f"A* path for player {a_star_move}")  # Debugging

        # 🔍 2. Use Minimax to evaluate if another move is better
        best_action = None
        best_value = -float('inf')

        # Test all possible pawn moves with Minimax
        for move in valid_moves:
            original_position = self.game_state["player_positions"][f"player{player}"]
            self.game_state["player_positions"][f"player{player}"] = move

            move_value = self.minimax(depth=3, alpha=-float('inf'), beta=float('inf'),
                                        maximizing_player=False, player=2 if player == 1 else 1)

            self.game_state["player_positions"][f"player{player}"] = original_position  # Reset

            if move_value > best_value:
                best_value = move_value
                best_action = ("move", move)
                print(f"🔍 Best move value from Minimax: {move_value}, {best_value}, {best_action}")

        # 🔍 Test all possible fences, but now evaluate them properly
        for fence in valid_fences:
            x, y, orientation = fence
            opponent = 2 if player == 1 else 1

            # Store original opponent path before placing the fence
            original_opponent_path = self.find_shortest_path(opponent)
            original_opponent_distance = len(original_opponent_path) if original_opponent_path else float('inf')

            # ✅ Correctly place the fence in QuoridorBoard
            self.board.fences.add(((x, y), (x + (1 if orientation == "H" else 0), y + (1 if orientation == "V" else 0)), orientation))
            self.board.update_gui_game_state()  # ✅ Ensure game state is updated

            # ✅ Recalculate the opponent’s shortest path
            new_opponent_path = self.find_shortest_path(opponent)
            new_opponent_distance = len(new_opponent_path) if new_opponent_path else float('inf')

            # ✅ Reset the fence by removing it from `self.board.fences`
            self.board.fences.remove(((x, y), (x + (1 if orientation == "H" else 0), y + (1 if orientation == "V" else 0)), orientation))
            self.board.fences_gui.remove((x, y, orientation))
            self.board.update_gui_game_state()  # ✅ Reset game state

            slowdown = new_opponent_distance - original_opponent_distance
            fence_value = slowdown * 5  # Assign a weight to opponent slowdown
            print(f"Fence:{x,y,orientation} Slowdown: {slowdown}, Fence value: {fence_value}")

            if fence_value > best_value:
                best_value = fence_value
                best_action = ("fence", fence)
                print(f"🔍 Best fence value from Minimax: {fence_value}, {best_value}, {best_action}")

        

        # 🔍 3. Compare A* move vs. Minimax move
        if a_star_move:
            print(f"✅ A* suggests move: {a_star_move[1]}")
            # If Minimax doesn't suggest a better alternative, use A* move
            if best_action is None:
                return a_star_move  

        print(f"🔍 Minimax chose: {best_action}")  # Debugging
        return best_action  # If A* was skipped, return Minimax best action

    def make_move(self, player):
        """Applies a move for the AI and updates the game state using the board functions."""
        self.game_state = self.read_game_state()
        action = self.choose_move(player)

        if action is None:
            print(f" AI has no valid moves for player {player}")
            return

        if action[0] == "move":
            new_position = action[1]
            success = self.board.move_pawn(player, new_position)
            if success:
                self.game_state = self.read_game_state()
                print(f" AI moved player {player} to {new_position}")
            else:
                print(f" AI tried to move player {player} to {new_position}, but move was invalid.")

        if action[0] == "fence":
            x, y, orientation = action[1]
            success = self.board.place_fence(x, y, orientation)
            if success:
                self.game_state = self.read_game_state()
                print(f" AI placed a fence at ({x}, {y}) with orientation {orientation}")
            else:
                print(f" AI tried to place a fence at ({x}, {y}), but it was invalid.")
