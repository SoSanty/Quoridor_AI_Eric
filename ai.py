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

        print(f"✅ Valid moves for player {player}: {valid_moves}")
        return valid_moves



    def get_valid_fences(self):
        """Returns a list of valid fences the AI can place."""
        valid_fences = []
        print(self.game_state)
        for x in range(8):  # Da 0 a 8 perché una barriera è tra due caselle
            for y in range(8):
                for orientation in ["H", "V"]:  # Orizzontale o verticale
                    if orientation == "H" and ((x, y, orientation) not in self.game_state["walls"] or (x-1, y, orientation) not in self.game_state["walls"]):
                        valid_fences.append((x, y, orientation))
                    if orientation == "V" and ((x, y, orientation) not in self.game_state["walls"] or (x, y-1, orientation) not in self.game_state["walls"]):
                        valid_fences.append((x, y, orientation))
        return valid_fences


    def heuristic(self, player):
        """
        Evaluate the game state for the player.  
        The closer the player is to the winning row, the higher the score.  
        If the opponent is close to victory, the score is lower.
        """
        opponent = 2 if player == 1 else 1
        player_y = self.game_state["player_positions"][f"player{player}"][1]
        opponent_y = self.game_state["player_positions"][f"player{opponent}"][1]

        goal_row = 8 if player == 1 else 0  # Riga vincente

        # Punteggio basato sulla distanza dalla vittoria
        player_score = goal_row - player_y if player == 1 else player_y - goal_row
        opponent_score = goal_row - opponent_y if opponent == 1 else opponent_y - goal_row

        return opponent_score - player_score  # L'AI cerca di massimizzare questo valore

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

        # Test all possible fences with Minimax
        for fence in valid_fences:
            x, y, orientation = fence
            self.game_state["walls"].append(fence)  # Simulate fence
            fence_value = self.minimax(depth=3, alpha=-float('inf'), beta=float('inf'),
                                        maximizing_player=False, player=2 if player == 1 else 1)
            self.game_state["walls"].remove(fence)  # Reset fence

            if fence_value > best_value:
                best_value = fence_value
                best_action = ("fence", fence)

        # 🔍 3. Compare A* move vs. Minimax move
        if a_star_move:
            print(f"✅ A* suggests move: {a_star_move[1]}")
            # If Minimax doesn't suggest a better alternative, use A* move
            if best_action is None or best_value < 0:
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
                return action[0], new_position
            else:
                print(f" AI tried to move player {player} to {new_position}, but move was invalid.")

        elif action[0] == "fence":
            x, y, orientation = action[1]
            success = self.board.place_fence(x, y, orientation)
            if success:
                self.game_state = self.read_game_state()
                print(f" AI placed a fence at ({x}, {y}) with orientation {orientation}")
                return action[0], action[1]
            else:
                print(f" AI tried to place a fence at ({x}, {y}), but it was invalid.")
