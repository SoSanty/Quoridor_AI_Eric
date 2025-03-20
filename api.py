import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from quoridor_board import QuoridorBoard

app = FastAPI()

# Allow CORS so GUI requests don't get blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GRID_SIZE = 9
MAX_WALLS = 10


@app.get("/state")
def get_mock_game_state():
    """
    Returns a mock game state with random player positions and walls.
    """
    walls = board.fences
    player1 = board.player_positions[1]
    player2 = board.player_positions[2]
    mock_state = {
        "player_positions": {"player1": player1, "player2": player2},
        "walls": walls,
        "turn": "player1",
        "board": []  # The GUI does not need full board details
    }
    
    return mock_state

if __name__ == "__main__":
    print("Starting mock FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
    board = QuoridorBoard()
    board.move_pawn(1, (4, 1))  # Move Player 1 forward
    board.update_game_state()
    time.sleep(2)  # Wait for 5 seconds
    board.place_fence(4, 4, 'H')  # Place horizontal fence
    board.update_game_state()
    time.sleep(2)  # Wait for 5 seconds