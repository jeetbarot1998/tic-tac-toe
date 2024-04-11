import json
import pickle
import socket
from _thread import start_new_thread
from Game import Game

server = "192.168.0.113"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, tic-tac-toe Server Started")

games = {}  # Dictionary to save gameObj by gameId
idCount = 0  # Keeping track of how many people are connected to server


def threaded_client(conn: socket.socket, player_id: int, gameId: int):
    """ For every client a different thread is made. If there are 100
     clients then 100 threads are spun. These are like api. From where the client will
     Interact with the server """
    global idCount
    # Whenever a client connects, we will tell the client what player the client is:
    # like if you are p1 or p2
    # This line of code will only run for the 1st time the user connects to the server
    print(player_id)
    conn.send(str.encode(str(player_id)))  # return player id
    reply = ""

    # The lines below will be continuously executing for data transfer between
    # particular client and server
    while True:
        """ This part is like api. From where the client will Interact with the server """
        # We will get the move of the user by location
        try:
            data = conn.recv(4096).decode() # receive data from client of size 4096 bytes
            # if the client has not sent any data then break the connection

            # Get game object
            if (gameId in games):
                clients_game = games[gameId]
                print(games)
                print(gameId)
                print(data)
                if not data:
                    print("No data received. Disconnecting")
                    break
                elif data == "reset":
                    clients_game.resetWent()
                elif data in ["0","1","2","3","4","5","6","7","8"]:
                    clients_game.playerMoves(player_id, data)
                # constantly send the game object
                # move or no move; constantly give a response as a game object
                reply = {"board" : clients_game.board,
                         "player_to_play" : clients_game.player_to_play,
                         "player_won" : clients_game.player_won,
                         "ready" : clients_game.ready}
                # This object will be used by the client to show the game updates to the user.
                # Serialize the dictionary to JSON format
                json_data = json.dumps(reply)

                # Convert the JSON string to bytes
                json_bytes = json_data.encode('utf-8')
                conn.send(json_bytes)
            else:
                break
        except Exception as e:
            print("error as :" + str(e))
            break
    # Close the game and delete it as the user client is not connected anymore
    print("Lost connection")
    try:
        del games[gameId]
        print(f"Closing game {gameId}")
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    """ For continuously running the server """
    conn, addr = s.accept()
    print("Connected to : " + str(addr))

    # On the basis of idCount we will assign p1 and p2
    idCount += 1
    # Every 2 players will be given 1 gameId
    # If 10 players then 5 different gameIds.
    # gameId 0 => player id 1,2
    # gameId 1 => player id 1,2
    gameId = (idCount - 1) // 2
    # If the player does not have an existing game to join then make a new game

    if (idCount % 2 == 1):
        # Supposing a player entered when idCount = 2. Due to the new player
        # idCount = 3. It means a new game needs to be made.
        # A new player has joined and there is no game for it
        # Make a new game for the new player connected
        games[gameId] = Game(gameId)
        print("Creating a new game")
        games[gameId].ready = False
        player = 1
    else:
        # Game already exists and another player is ready.
        # As soon as the player is available. Make the game state as ready
        print("Entering existing game ")
        games[gameId].ready = True
        player = 2

    start_new_thread(threaded_client, (conn, player, gameId))
