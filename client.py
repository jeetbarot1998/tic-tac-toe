import json

import pygame

from network import Network

def draw(board):
    for i in range(0, 9, 3):
        print("-------------")
        print(f"| {board[i]} | {board[i + 1]} | {board[i + 2]} |")
    print("-------------")

def validate_user_input(user_input):
    if user_input in range(0,9):
        return True
    return False
def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            received_data = n.send("get") # get player number on connecting
        except:
            run = False
            print("Couldn't get game")
            break
        if received_data:
            # Decode the received bytes to a JSON string
            json_data = received_data.decode('utf-8')

            # Deserialize the JSON string to a Python dictionary
            data_dict = json.loads(json_data)

            if player == data_dict["player_to_play"] and data_dict["ready"] and data_dict["player_won"] is None:
                draw(data_dict["board"])
                user_input = None
                while not(validate_user_input(user_input)):
                    user_input = int(input("Enter a Number between 0-8"))
                n.send(str(user_input))
            elif data_dict["player_won"] is not None:
                if(player == data_dict["player_won"]):
                    print("You won")
                else:
                    print("Player 2 won")
            else:
                continue

            print(data_dict)
main()

