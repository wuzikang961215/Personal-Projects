# test.py
from gameData import GameManager

def print_game_details():
    manager = GameManager.load_state()
    manager.print_all_game_details()

def delete_last_game():
    manager = GameManager.load_state()
    manager.delete_last_game()
    manager.save_state()

def correct_last_game():
    manager = GameManager.load_state()
    # Conditions or checks that determine if the last game needs correction
    manager.correct_last_game_data()
    manager.save_state()  # Save the corrected state


if __name__ == "__main__":
    print_game_details()
    # delete_last_game()
    #correct_last_game()
    # manager = GameManager.load_state()
    # manager.update_board_structures()
    # manager.save_state()
    

    