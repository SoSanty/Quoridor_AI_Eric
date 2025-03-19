import pygame
import requests
import time

# API URL for fetching game state
API_URL = "http://127.0.0.1:8000"

# Updated GUI size
WINDOW_SIZE = 700  # Increased to better fit the screen
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PLAYER_RADIUS = CELL_SIZE // 3
WALL_THICKNESS = 10  # Increased for visibility

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

def fetch_game_state():
    """
    Fetches the current game state from the FastAPI server.

    Returns:
        dict: The game state, including player positions and walls.
    """
    try:
        response = requests.get(f"{API_URL}/state")
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

def draw_grid(screen):
    """
    Draws the 9x9 Quoridor board grid.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
    """
    for i in range(GRID_SIZE + 1):  # Draw horizontal and vertical lines
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), 3)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), 3)

def draw_player(screen, position, color):
    """
    Draws a player at the given position.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        position (tuple): The (x, y) position of the player.
        color (tuple): The color of the player.
    """
    x, y = position
    center_x = y * CELL_SIZE + CELL_SIZE // 2
    center_y = x * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, color, (center_x, center_y), PLAYER_RADIUS)

def draw_wall(screen, x, y, orientation):
    """
    Draws a wall at the given position and orientation.

    Args:
        screen (pygame.Surface): The Pygame surface to draw on.
        x (int): The x-coordinate of the wall.
        y (int): The y-coordinate of the wall.
        orientation (str): "H" for horizontal, "V" for vertical.
    """
    if orientation == "H":
        pygame.draw.rect(screen, BLACK, (y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE - WALL_THICKNESS, CELL_SIZE * 2, WALL_THICKNESS))
    elif orientation == "V":
        pygame.draw.rect(screen, BLACK, (x * CELL_SIZE + CELL_SIZE - WALL_THICKNESS, y * CELL_SIZE, WALL_THICKNESS, CELL_SIZE * 2))

def main():
    """
    Main function to initialize the Pygame window and update the game board.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Quoridor Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(WHITE)  # Clear the screen
        draw_grid(screen)  # Draw the grid

        # Fetch game state
        game_state = fetch_game_state()
        if game_state:
            # Draw players
            draw_player(screen, game_state["player_positions"]["player1"], RED)
            draw_player(screen, game_state["player_positions"]["player2"], BLUE)

            # Draw walls
            for wall in game_state["walls"]:
                coord1, coord2, orientation = wall
                x1, y1 = coord1
                draw_wall(screen, x1, y1, orientation)

        pygame.display.flip()  # Refresh display
        clock.tick(1)  # Update every second

        # Handle quitting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()