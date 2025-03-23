from quoridor_board import QuoridorBoard
import time
from ai import AI

class MainGame:

    def __init__(self, window_size=700, grid_size=9):
        self.board = QuoridorBoard()
        self.ai = AI(self.board)
        self.fences_player1 = 10  # Counter for fences placed by player 1
        

    def main(self):
        time.sleep(1)
        self.board.update_gui_game_state()
        time.sleep(1)


        while True:  # Loop to allow restarting the game
            current_player = 1  # Player 1 starts

            while True:
                if current_player == 1:
                    print(f"Player {current_player}'s turn.")

                    while True:
                        move_type = input("Move the pawn (M) or place a fence (F)? ").strip().upper()
                        if move_type == 'M':
                            try:
                                x, y = map(int, input("Enter the X and Y coordinates of the new position (separated by space): ").split())
                                if self.board.is_valid_pawn_move(current_player, (x, y)):
                                    self.board.move_pawn(current_player, (x, y))
                                    print("Valid move!")
                                    self.board.update_gui_game_state()  # save the state in json
                                
                                    break
                                else:
                                    print("Invalid move, try again.")
                            except ValueError:
                                print("Enter valid coordinates (e.g., '4 3').")

                        elif move_type == 'F':
                            if  (self.fences_player1 > 0): #it checks if the user put 10 walls
                                try:
                                    x, y = map(int, input("Enter the X and Y coordinates for the fence: ").split())
                                    orientation = input("Enter orientation (H for horizontal, V for vertical): ").strip().upper()

                                    if  self.board.place_fence(x, y, orientation,current_player):
                                        self.fences_player1 -= 1  # Increment fence counter for player 1
                                        print("Fence placed successfully!")
                                        self.board.update_gui_game_state()  # Save the state in json
                                        
                                        break
                                    else:
                                        print("Invalid fence position, try again.")
                                except ValueError:
                                    print("Enter valid coordinates.")
                            else:
                                print("You have already placed 10 fences. You cannot place more.")
                        else:
                            print("Invalid input. Use 'M' to move or 'F' to place a fence.")
                else:
                    
                    self.ai.make_move(current_player)
                    self.board.update_gui_game_state()  # Save the state in the JSON file


                # Check for victory
                if self.board.player_positions[current_player][1] == (8 if current_player == 1 else 0):
                    
                    print(f"Player {current_player} wins!")
                    self.board.update_gui_game_state()  # Save the final state in the JSON file
                    break

                # Switch turn
                current_player = 2 if current_player == 1 else 1

            # Ask if the user wants to restart or exit
            restart = input("Do you want to play again? (Y for yes, any other key to exit): ").strip().upper()
            if restart != 'Y':
                print("Goodbye!")
                break

if __name__ == "__main__":
    main_game = MainGame()
    main_game.main()

