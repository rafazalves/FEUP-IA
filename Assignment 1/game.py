from math import gcd

borders = [(0,-10), (1, -9), (2, -8), (3, -7), (4, -6), (5, -5), (-1, -9), (-2, -8), (-3, -7), (-4, -6), (-5, -5),(0, 10), (1, 9), (2, 8), (3, 7), (4, 6), (5, 5), (-1, 9), (-2, 8), (-3, 7), (-4, 6), (-5, 5), (5, -3), (5, -1), (5, 1), (5, 3), (-5, -3), (-5, -1), (-5, 1), (-5, 3)]
adjacent = [(-1, 1), (0, 2), (1, 1), (1, -1), (0, -2), (-1, -1)]

class Game (object):
    def __init__(self):
        self.player1 = [(-4,4), (-3,5), (-2,6), (-1,7), (0,6), (1,7), (2,6), (3,5), (4,4)]
        self.player2 = [(-4,-4), (-3,-5), (-2,-6), (-1,-7), (0,-6), (1,-7), (2,-6), (3,-5), (4,-4)]
        self.p1blocked = []
        self.p2blocked = []
        self.p1goal = (0, -8)
        self.p2goal = (0, 8)
        self.playing = 1
        self.selected_piece = None
        self.winner = 0	# 0 means no winner, 1 means player 1 wins, 2 means player 2 wins

    # Check if the move required can be made
    def get_valid_moves(self, piece):

        if (piece in self.p1blocked) or (piece in self.p2blocked):
            return []

        pieces = set()
        own_goal = tuple()

        match self.playing:
            case 1:
                pieces = set(self.player1)
                opponent_goal = self.p2goal
            case 2:
                pieces = set(self.player2)
                opponent_goal = self.p1goal

        x, y = piece
        moves = set(map(lambda pos: (pos[0] + x, pos[1] + y), adjacent))

        overlaps = moves & pieces
        while overlaps:
            moves -= pieces
            for pos in overlaps:
                distance = (pos[0] - x, pos[1] - y)
                divisor = gcd(*distance)
                direction = (distance[0] // divisor, distance[1] // divisor)
                
                # Purely vertical case
                direction = direction if direction[0] != 0 else (0, direction[1] * 2)

                moves.add((pos[0] + direction[0], pos[1] + direction[1]))
            overlaps = moves & pieces
            
        return [move for move in moves if move not in borders and move != opponent_goal]

    # Update position of a piece after a move
    def update(self, piece, move):

        own_pieces = []
        oponent_pieces = []

        match self.playing:
            case 1:
                own_pieces = self.player1
                oponent_pieces = self.player2
            case 2:
                own_pieces = self.player2
                oponent_pieces = self.player1
        
        if piece in own_pieces:
            own_pieces.remove(piece)
            own_pieces.append(move)
            if move in oponent_pieces:
                oponent_pieces.remove(move)
                self.updateblocked()
            self.updateblocked()

        self.selected_piece = None
    
    # Check pieces that need to be blocked/unblocked
    def updateblocked(self):
        self.p1blocked = []
        self.p2blocked = []
        for (x,y) in self.player1:
            neighbours = set(map(lambda pos: (pos[0] + x, pos[1] + y), adjacent)) & set(self.player2)
            if neighbours:
                self.p1blocked.append((x, y))
                self.p2blocked.extend(neighbours)

    def check_winner(self):
        if(len(self.get_all_moves()) == 0):
            self.winner = 1 if self.playing == 2 else 2
            return self.winner
        elif len(self.player1) == 0:
            print("Player 1 has no moves left")
            self.winner = 2
            return self.winner
        elif len(self.player2) == 0:
            print("Player 2 has no moves left")
            self.winner = 1
            return self.winner
        elif (0, 8) in self.player2:
            self.winner = 2
            return self.winner
        elif (0, -8) in self.player1:
            self.winner = 1
            return self.winner
        
        return self.winner
        
    def swap_turn(self):
        if(self.playing == 2):
            self.playing = 1
        else:
            self.playing = 2

    # Get all the possible moves for the pieces available
    def get_all_moves(self):
        moves = []
        if self.playing == 1:
            valid_piece = self.player1
        else:
            valid_piece = self.player2
        
        for piece in valid_piece:
            moves.extend([(piece, move) for move in self.get_valid_moves(piece)])
        return moves
        
    # Evaluates the value of a play by the current player, tries to block the opponent's moves
    def evaluate_offensive(self):
        player1_score = self.calculate_score_offensive(self.player1, self.p1goal, self.p2blocked)
        player2_score = self.calculate_score_offensive(self.player2, self.p2goal, self.p1blocked)
        return player1_score - player2_score

    def calculate_score_offensive(self, pieces, goal, blocked):
        score = 0
        for piece in pieces:
            if piece == goal:  # If piece can go to the goal cell, it's the best possible move
                score += 1000
            else:
                distance_to_goal = self.manhattan_distance(piece, goal)
                score += 10 / (distance_to_goal + 1)  # Closer pieces have higher values
                if piece in blocked:  # If piece can capture an enemy piece (blocked)
                    score += 50
        return score

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def evaluate_defensive(self):
        if(self.playing == 1):
            my_pieces = len(self.player1) - len(self.p1blocked)
            opponent_pieces = len(self.player2) - len(self.p2blocked)
        else:
            my_pieces = len(self.player2) - len(self.p2blocked)
            opponent_pieces = len(self.player1) - len(self.p1blocked)
        return my_pieces - opponent_pieces