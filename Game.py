class Game:
    def __init__(self, gameId):
        self.ready = False
        self.player_to_play = 1
        self.player_won = None
        self.isP1Connected = False
        self.isP2Connected = False
        self.board = [" " for _ in range(9)]  # Represents the Tic Tac Toe board
        self.p1Moves = []
        self.p2Moves = []
        self.winningMoves = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                             (0, 3, 6), (1, 4, 7), (2, 5, 8),
                             (0, 4, 8), (2, 4, 6)]
        self.winner = None
        self.gameId = gameId

    def playerMoves(self, player, loc):
        location = int(loc)
        if self.board[location] == " ":
            if player == 1:
                self.p1Moves.append(location)
                self.board[location] = "X"
                if self.check_winner(self.p1Moves):
                    self.player_won = 1
                    return
                self.player_to_play = 2
            elif player == 2:
                self.p2Moves.append(location)
                self.board[location] = "O"
                if self.check_winner(self.p2Moves):
                    self.player_won = 2
                    return
                self.player_to_play = 1

    def is_connected(self):
        """ if the server is ready """
        return self.ready

    def bothWent(self):
        """ If both players played"""
        return self.isP1Connected and self.isP2Connected

    def check_winner(self, player_moves):
        for each_winning_tuple in self.winningMoves:
            all_exist = all(item in player_moves for item in each_winning_tuple)
            if all_exist:
                return True
        return False

    def resetWent(self):
        self.isP1Connected = False
        self.isP2Connected = False