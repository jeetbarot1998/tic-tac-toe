""" Defines the networking protocol and how data will be sent b/2 client and server """
import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.113"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        """ When connecting the server will tell you if you are player 1 or 2 """
        try:
            self.client.connect(self.addr) # send the connection request to the server
            return self.client.recv(2048).decode() # get player id from server and sent it to the client
        except:
            pass

    def send(self, data):
        """ Continuously sending data to the server """
        try:
            self.client.send(str.encode(data)) # send data to the server as get, reset or move as string.
            return self.client.recv(2048) # get game object from server and send it to client
        except socket.error as e:
            print(e)


# n = Network()
# player = n.getP()
# print(player)

