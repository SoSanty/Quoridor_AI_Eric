import pygame
import json
import os
import time

class QuoridorGame:
    """
    GUI class for rendering the Quoridor board and handling visual updates
    based on the current game state stored in a JSON file.
    """
    def __init__(self, window_size=700, grid_size=9):
        """
        Initializes the graphical interface for the game board, including grid,
        player visuals, wall thickness, and display window.

        Args:
            window_size (int): Pixel dimension of the window width and height.
            grid_size (int): Number of grid cells (default is 9 for Quoridor).
        """
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
        self.screen = pygame.display.set_mode((self.window_size + 250, self.window_size))
        pygame.display.set_caption("Quoridor Game")

    def read_game_state(self):
        """
        Reads the game state from the game_state.json file. If the file does
        not exist or is corrupted, returns None to signal the need for
        initialization.

        Returns:
            dict or None: Parsed game state or None if unavailable.
        """
        if not os.path.exists("game_state.json"):
            return None
        try:
            with open("game_state.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def draw_split_circle(self, position):
        """
        Renders a split-colored circle to represent both players standing on
        the same tile. The circle is half red (Player 1) and half blue (Player 2).

        Args:
            position (tuple): Coordinates (x, y) of the player.
        """
        x, y = position
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        radius = self.player_radius

        pygame.draw.circle(self.screen, self.red, (center_x, center_y), radius)
        pygame.draw.polygon(
            self.screen, self.blue,
            [(center_x, center_y - radius), (center_x, center_y + radius), (center_x + radius, center_y)]
        )

    def draw_grid(self):
        """
        Draws the board grid and labels with row and column numbers.
        """
        font = pygame.font.Font(None, 24)

        for i in range(self.grid_size + 1):
            pygame.draw.line(self.screen, self.black, (0, i * self.cell_size), (self.window_size, i * self.cell_size), 3)
            pygame.draw.line(self.screen, self.black, (i * self.cell_size, 0), (i * self.cell_size, self.window_size), 3)

            if i < self.grid_size:
                row_text = font.render(str(i), True, self.black)
                self.screen.blit(row_text, (5, i * self.cell_size + self.cell_size // 3))
                col_text = font.render(str(i), True, self.black)
                self.screen.blit(col_text, (i * self.cell_size + self.cell_size // 3, 5))

    def draw_player(self, position, color):
        """
        Renders a single player at a specified position.

        Args:
            position (tuple): Coordinates (x, y) for the player.
            color (tuple): RGB color code for the player.
        """
        x, y = position
        center_x = x * self.cell_size + self.cell_size // 2
        center_y = y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, color, (center_x, center_y), self.player_radius)

    def draw_wall(self, x, y, orientation):
        """
        Draws a wall on the board given its top-left coordinate and orientation.

        Args:
            x (int): X-coordinate on the grid.
            y (int): Y-coordinate on the grid.
            orientation (str): 'H' for horizontal, 'V' for vertical.
        """
        if orientation == "H":
            pygame.draw.rect(self.screen, self.black, (x * self.cell_size, y * self.cell_size + self.cell_size - self.wall_thickness, self.cell_size * 2, self.wall_thickness))
        elif orientation == "V":
            pygame.draw.rect(self.screen, self.black, (x * self.cell_size + self.cell_size - self.wall_thickness, y * self.cell_size, self.wall_thickness, self.cell_size * 2))

    def draw_wall_count(self, player1_walls, player2_walls):
        """
        Displays the remaining number of walls for each player on the right
        sidebar of the GUI.

        Args:
            player1_walls (int): Walls left for Player 1.
            player2_walls (int): Walls left for Player 2.
        """
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(self.screen, self.white, (self.window_size, 0, 250, self.window_size))

        player1_text = font.render(f"Player 1 Walls: {player1_walls}", True, self.red)
        self.screen.blit(player1_text, (self.window_size + 20, 50))

        player2_text = font.render(f"Player 2 Walls: {player2_walls}", True, self.blue)
        self.screen.blit(player2_text, (self.window_size + 20, 100))

    def update_game_state(self):
        """
        Main loop to update the GUI by polling the game state JSON file. 
        Redraws the board, players, and walls based on changes.
        """
        running = True
        last_state = None
        self.screen.fill(self.white)

        while running:
            self.draw_grid()
            game_state = self.read_game_state()

            if game_state and game_state != last_state:
                last_state = game_state
                print("New game state loaded:", game_state)

                player1_pos = game_state["player_positions"]["player1"]
                player2_pos = game_state["player_positions"]["player2"]

                if self.last_player1_pos != player1_pos:
                    if self.last_player1_pos:
                        self.draw_player(self.last_player1_pos, self.white)
                    if player1_pos == player2_pos:
                        self.draw_split_circle(player1_pos)
                        self.last_player1_pos = player1_pos
                        self.last_player2_pos = player2_pos
                    else:
                        self.draw_player(player1_pos, self.red)
                        self.draw_player(player2_pos, self.blue)
                        self.last_player1_pos = player1_pos

                if self.last_player2_pos != player2_pos:
                    if self.last_player2_pos:
                        self.draw_player(self.last_player2_pos, self.white)
                    if player1_pos == player2_pos:
                        self.draw_split_circle(player1_pos)
                        self.last_player1_pos = player1_pos
                        self.last_player2_pos = player2_pos
                    else:
                        self.draw_player(player1_pos, self.red)
                        self.draw_player(player2_pos, self.blue)
                        self.last_player2_pos = player2_pos

                for wall in game_state["walls"]:
                    x1, y1, orientation = wall
                    self.draw_wall(x1, y1, orientation)

                self.draw_wall_count(game_state["walls_remaining"]["player_1"], game_state["walls_remaining"]["player_2"])

            elif not game_state:
                self.screen.fill(self.white)
                self.draw_grid()
                self.last_player1_pos = None
                self.last_player2_pos = None

            pygame.display.flip()
            time.sleep(1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()

if __name__ == "__main__":
    game = QuoridorGame()
    game.update_game_state()