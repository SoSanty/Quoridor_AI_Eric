import random
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

board = QuoridorBoard()
@app.get("/state")
def get_mock_game_state():
    """
    Returns a mock game state with random player positions and walls.
    """
    board.place_fence(5, 4, 'V')
    walls = board.fences
    mock_state = {
        "player_positions": {"player1": (4,0), "player2": (4,8)},
        "walls": walls,
        "turn": "player1",
        "board": []  # The GUI does not need full board details
    }
    
    return mock_state

if __name__ == "__main__":
    import uvicorn
    print("Starting mock FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)