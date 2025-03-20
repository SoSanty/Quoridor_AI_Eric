from quoridor_board import QuoridorBoard
import time

def main():
    board = QuoridorBoard()  # Crea un'istanza del gioco
    time.sleep(1)
    board.update_gui_game_state()
    time.sleep(1)


    while True:  # Loop to allow restarting the game
        current_player = 1  # Player 1 starts

        while True:
            
            print(f"Player {current_player}'s turn.")

            while True:
                move_type = input("Move the pawn (M) or place a fence (F)? ").strip().upper()

                if move_type == 'M':
                    try:
                        x, y = map(int, input("Enter the X and Y coordinates of the new position (separated by space): ").split())
                        if board.is_valid_pawn_move(current_player, (x, y)):
                            board.move_pawn(current_player, (x, y))
                            print("Valid move!")
                            board.update_gui_game_state()  # save the state in json
                        
                            break
                        else:
                            print("Invalid move, try again.")
                    except ValueError:
                        print("Enter valid coordinates (e.g., '4 3').")

                elif move_type == 'F':
                    try:
                        x, y = map(int, input("Enter the X and Y coordinates for the fence: ").split())
                        orientation = input("Enter orientation (H for horizontal, V for vertical): ").strip().upper()
                        if board.place_fence(x, y, orientation):
                            print("Fence placed successfully!")
                            board.update_gui_game_state()  # Salva lo stato nel file JSON
                            
                            break
                        else:
                            print("Invalid fence position, try again.")
                    except ValueError:
                        print("Enter valid coordinates.")

                else:
                    print("Invalid input. Use 'M' to move or 'F' to place a fence.")

            # Check for victory
            if board.player_positions[current_player][1] == (8 if current_player == 1 else 0):
                
                print(f"Player {current_player} wins!")
                board.update_gui_game_state()  # Salva lo stato finale nel file JSON
                break

            # Switch turn
            current_player = 2 if current_player == 1 else 1

        # Ask if the user wants to restart or exit
        restart = input("Do you want to play again? (Y for yes, any other key to exit): ").strip().upper()
        if restart != 'Y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()