import pygame
import json
import os
import time

class QuoridorGame:
    def __init__(self, window_size=700, grid_size=9):
        self.window_size = window_size
        self.grid_size = grid_size
        self.cell_size = window_size // grid_size
        self.player_radius = self.cell_size // 3
        self.wall_thickness = 10
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (200, 0, 0)
        self.blue = (0, 0, 200)

        # Initialize player positions and previous positions
        self.last_player1_pos = None
        self.last_player2_pos = None

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Quoridor Game")

    def read_game_state(self):
        """Reads the latest game state from the JSON file, or restarts the game state if the file doesn't exist."""
        if not os.path.exists("game_state.json"):  # If the file doesn't exist, restart the game state
            return None  # Returning None will cause the GUI to display the initial state (white grid)
        
        try:
            with open("game_state.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def draw_split_circle(self, position):
        """Draws a split blue-red circle when both players are in the same position."""
        x, y = position
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        radius = self.player_radius

        # Draw left half red, right half blue
        pygame.draw.circle(self.screen, self.red, (center_x, center_y), radius)
        pygame.draw.polygon(
            self.screen, self.blue,
            [(center_x, center_y - radius), (center_x, center_y + radius), (center_x + radius, center_y)]
        )

    def draw_grid(self):
        """Draws the 9x9 Quoridor board grid with row and column numbers."""
        font = pygame.font.Font(None, 24)  # Load a default font
        
        for i in range(self.grid_size + 1):
            # Draw horizontal and vertical grid lines
            pygame.draw.line(self.screen, self.black, (0, i * self.cell_size), (self.window_size, i * self.cell_size), 3)
            pygame.draw.line(self.screen, self.black, (i * self.cell_size, 0), (i * self.cell_size, self.window_size), 3)

            if i < self.grid_size:
                # Draw row numbers on the left side
                row_text = font.render(str(i), True, self.black)
                self.screen.blit(row_text, (5, i * self.cell_size + self.cell_size // 3))

                # Draw column numbers on the top side
                col_text = font.render(str(i), True, self.black)
                self.screen.blit(col_text, (i * self.cell_size + self.cell_size // 3, 5))

    def draw_player(self, position, color):
        """Draws a player at the given position."""
        x, y = position
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, color, (center_x, center_y), self.player_radius)

    def draw_wall(self, x, y, orientation):
        """Draws a wall at the given position and orientation."""
        if orientation == "H":
            pygame.draw.rect(self.screen, self.black, (x * self.cell_size, y * self.cell_size + self.cell_size - self.wall_thickness, self.cell_size * 2, self.wall_thickness))
        elif orientation == "V":
            pygame.draw.rect(self.screen, self.black, (x * self.cell_size + self.cell_size - self.wall_thickness, y * self.cell_size, self.wall_thickness, self.cell_size * 2))

    def update_game_state(self):
        """Handles the game state update and rendering."""
        running = True
        last_state = None
        self.screen.fill(self.white)  # Only fill the screen once

        while running:
            self.draw_grid()

            # Read the game state from file
            game_state = self.read_game_state()

            if game_state and game_state != last_state:  # Only update if state has changed
                last_state = game_state
                print("New game state loaded:", game_state)

                player1_pos = game_state["player_positions"]["player1"]
                player2_pos = game_state["player_positions"]["player2"]

                # Erase and draw the players at their new positions
                if self.last_player1_pos != game_state["player_positions"]["player1"]:
                    # Clear the previous dot (if there is one) and draw the new position
                    if self.last_player1_pos:
                        self.draw_player(self.last_player1_pos, self.white)  # Erase by drawing white over it
                    if player1_pos == player2_pos:
                    # If both players are at the same position, draw a split circle
                        self.draw_split_circle(player1_pos)
                        self.last_player1_pos = player1_pos
                        self.last_player2_pos = player2_pos
                    else:
                        self.draw_player(game_state["player_positions"]["player1"], self.red)
                        self.draw_player(game_state["player_positions"]["player2"], self.blue)
                        self.last_player1_pos = game_state["player_positions"]["player1"]

                if self.last_player2_pos != game_state["player_positions"]["player2"]:
                    # Clear the previous dot (if there is one) and draw the new position
                    if self.last_player2_pos:
                        self.draw_player(self.last_player2_pos, self.white)  # Erase by drawing white over it
                    if player1_pos == player2_pos:
                    # If both players are at the same position, draw a split circle
                        self.draw_split_circle(player1_pos)
                        self.last_player1_pos = player1_pos
                        self.last_player2_pos = player2_pos
                    else:
                        self.draw_player(game_state["player_positions"]["player1"], self.red)
                        self.draw_player(game_state["player_positions"]["player2"], self.blue)
                        self.last_player2_pos = game_state["player_positions"]["player2"]

     
                # Draw the walls based on the game state
                for wall in game_state["walls"]:
                    x1, y1, orientation = wall
                    self.draw_wall(x1, y1, orientation)
            elif not game_state:
                # If the game state is empty, clear the board
                self.screen.fill(self.white)
                self.draw_grid()
                self.last_player1_pos = None
                self.last_player2_pos = None

            pygame.display.flip()
            time.sleep(1)  # Check for updates every second

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()


if __name__ == "__main__":
    game = QuoridorGame()
    game.update_game_state()