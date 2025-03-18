import unittest
from quoridor_board import QuoridorBoard

class TestQuoridorBoard(unittest.TestCase):
    """Unit tests for the QuoridorBoard class."""

    def setUp(self):
        """Initialize a new board before each test."""
        self.board = QuoridorBoard()
    
    def test_initial_positions(self):
        """Test if players start at the correct positions."""
        self.assertEqual(self.board.player_positions[1], (4, 0))
        self.assertEqual(self.board.player_positions[2], (4, 8))
    
    def test_valid_pawn_move(self):
        """Test if a valid pawn move is executed correctly."""
        self.assertTrue(self.board.move_pawn(1, (4, 1)))  # Move forward
        self.assertEqual(self.board.player_positions[1], (4, 1))
    
    def test_invalid_pawn_move_outside_board(self):
        """Test if an invalid move outside the board is rejected."""
        self.assertFalse(self.board.move_pawn(1, (4, -1)))  # Move outside board
    
    def test_invalid_pawn_jump_without_opponent(self):
        """Test if jumping without an opponent is rejected."""
        self.assertFalse(self.board.move_pawn(1, (4, 2)))  # Trying to jump over empty space
    
    def test_pawn_jump_over_opponent(self):
        """Test if a valid jump over an opponent is allowed."""
        self.board.player_positions[2] = (4, 2)
        self.board.move_pawn(2, (4, 1))  # Move Player 2 in front of Player 1
        self.assertTrue(self.board.move_pawn(1, (4, 2)))  # Jump over Player 2
        self.assertEqual(self.board.player_positions[1], (4, 2))
    
    def test_fence_H_saved(self):
        """Test if a valid fence can be placed."""
         # Test horizontal fence placement
        self.board.place_fence(7, 3, 'H')
        self.assertIn(((7, 3), (8, 3), 'H'), self.board.fences)  # Check if the fence is in the set of fences
    
    def test_fence_V_saved(self):
         # Test horizontal fence placement
        self.board.place_fence(3, 3, 'V')
        self.assertIn(((3, 3), (3, 4), 'V'), self.board.fences)  # Check if the fence is in the set of fences

    def test_invalid_H_fence_placement(self):
        # Test invalid H fence placement (outside of board)
        result = self.board.place_fence(9, 9, 'H')  # Out of bounds
        self.assertFalse(result)  # It should fail

    def test_invalid_V_placement(self):
        # Test invalid V fence placement (outside of board)
        result = self.board.place_fence(9, 9, 'V')  # Out of bounds
        self.assertFalse(result)  # It should fail

    def test_fence_H_occupied_space(self):
        # Test placing a fence on an already occupied space
        self.board.place_fence(3, 3, 'H')  # Place a horizontal fence
        result = self.board.place_fence(3, 3, 'H')  # Try to place another horizontal fence at the same spot
        self.assertFalse(result)  # It should fail (fence already placed)

    def test_fence_V_occupied_space(self):
        # Test placing a vertical fence where one already exists in the same position
        self.board.place_fence(4, 3, 'V')  # Place a vertical fence
        result = self.board.place_fence(4, 3, 'V')  # Try to place another vertical fence at the same spot
        self.assertFalse(result)  # It should fail (fence already placed)

    def test_fence_invalid_cross_placement(self):
        # Test preventing cross placement (horizontal on top of vertical)
        self.board.place_fence(3, 3, 'V')  # Place a vertical fence
        result = self.board.place_fence(3, 3, 'H')  # Try to place a horizontal fence at the same position
        self.assertFalse(result)  # It should fail (cross placement)
    
    def test_H_fence_blocking_movement(self):
        """Test if a pawn cannot move through a fence."""
        self.board.player_positions[1] = (7, 4)
        self.board.place_fence(7, 3, 'H')  # Place a horizontal fence blocking Player 1
        self.board.place_fence(6, 4, 'H')  # Place a horizontal fence blocking Player 1
        self.assertFalse(self.board.move_pawn(1, (8, 4)))

    def test_V_fence_blocking_movement(self):
        """Test if a pawn cannot move through a fence."""
        self.board.player_positions[1] = (4, 1)
        self.board.place_fence(3, 0, 'V')  # Place a horizontal fence blocking Player 1
        self.assertFalse(self.board.move_pawn(1, (3, 1)))
    
    def test_path_existence_after_fence_placement(self):
        """Test if the board correctly validates path existence after fence placement."""
        self.assertTrue(self.board.has_path_to_goal(1))
        self.assertTrue(self.board.has_path_to_goal(2))
    
    def test_fence_preventing_path(self):
        """Test if placing a fence that blocks all paths is rejected."""
        
        self.board.place_fence(0, 4, 'H')
        self.board.place_fence(2, 4, 'H')
        self.board.place_fence(4, 4, 'H')
        self.board.place_fence(6, 4, 'H')
        self.board.place_fence(7, 3, 'H')
        self.assertFalse(self.board.place_fence(6, 3, 'V'))  # Final block should fail
    
    def test_display_board(self):
        """Test if the board display does not raise errors."""
        self.board.place_fence(4, 0, 'H')
        self.board.place_fence(5, 1, 'V')
        self.board.place_fence(4, 1, 'V')
        self.board.place_fence(4, 2, 'H')
        self.board.place_fence(7, 0, 'V')


        try:
            self.board.display_board()
        except Exception as e:
            self.fail(f"display_board() raised an error: {e}")
    
if __name__ == "__main__":
    unittest.main()
