"""
AI module implementing a chess AI using the minimax algorithm with alpha-beta pruning.
This module contains the AI class that handles computer player moves and game state evaluation.
"""

from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:
    """
    AI class that implements a chess computer player using minimax algorithm with alpha-beta pruning.
    The AI evaluates board positions and makes moves based on piece values and positional advantages.
    """

    # Global variable to store temporary moves during evaluation
    global tp
    tp = []

    def __init__(self):
        """Initialize the AI player"""
        pass

    def evaluate(self, gametiles):
        """
        Evaluate the current board position and select the best move.
        
        Args:
            gametiles: The current state of the game board
            
        Returns:
            tuple: The coordinates of the best move (start_y, start_x, end_y, end_x)
        """
        min = 100000
        count = 0
        count2 = 0
        chuk = []
        movex = move()
        tp.clear()
        # Run minimax search with depth 3
        xp = self.minimax(gametiles, 3, -1000000000, 1000000000, False)

        # Find moves with the minimum evaluation score
        for zoom in tp:
            if zoom[4] < min:
                chuk.clear()
                chuk.append(zoom)
                min = zoom[4]
            if zoom[4] == min:
                chuk.append(zoom)
        # Randomly select one of the best moves
        fx = random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0], chuk[fx][1], chuk[fx][2], chuk[fx][3]

    def reset(self, gametiles):
        """
        Reset the moved status of kings and rooks for castling.
        
        Args:
            gametiles: The current state of the game board
        """
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring() == 'k' or gametiles[x][y].pieceonTile.tostring() == 'r':
                    gametiles[x][y].pieceonTile.moved = False

    def updateposition(self, x, y):
        """
        Convert board coordinates to position index.
        
        Args:
            x: Row coordinate
            y: Column coordinate
            
        Returns:
            int: Position index (0-63)
        """
        a = x * 8
        b = a + y
        return b

    def checkmate(self, gametiles):
        """
        Check if the current position is checkmate.
        
        Args:
            gametiles: The current state of the game board
            
        Returns:
            bool: True if the position is checkmate, False otherwise
        """
        movex = move()
        if movex.checkw(gametiles)[0] == 'checked':
            array = movex.movesifcheckedw(gametiles)
            if len(array) == 0:
                return True

        if movex.checkb(gametiles)[0] == 'checked':
            array = movex.movesifcheckedb(gametiles)
            if len(array) == 0:
                return True

    def stalemate(self, gametiles, player):
        """
        Check if the current position is stalemate.
        
        Args:
            gametiles: The current state of the game board
            player: True for White, False for Black
            
        Returns:
            bool: True if the position is stalemate, False otherwise
        """
        movex = move()
        if player == False:
            if movex.checkb(gametiles)[0] == 'notchecked':
                check = False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance == 'Black':
                            moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1 = movex.pinnedb(gametiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    return True

        if player == True:
            if movex.checkw(gametiles)[0] == 'notchecked':
                check = False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance == 'White':
                            moves1 = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1 = movex.pinnedw(gametiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    return True

    def minimax(self, gametiles, depth, alpha, beta, player):
        """
        Implement minimax algorithm with alpha-beta pruning.
        
        Args:
            gametiles: The current state of the game board
            depth: Current depth in the search tree
            alpha: Alpha value for alpha-beta pruning
            beta: Beta value for alpha-beta pruning
            player: True for maximizing player (White), False for minimizing player (Black)
            
        Returns:
            int: Evaluation score of the position
        """
        if depth == 0 or self.checkmate(gametiles) == True or self.stalemate(gametiles, player) == True:
            return self.calculateb(gametiles)
        if not player:
            minEval = 100000000
            kp, ks = self.eva(gametiles, player)
            for lk in kp:
                for move in lk:
                    mts = gametiles[move[2]][move[3]].pieceonTile
                    gametiles = self.move(gametiles, move[0], move[1], move[2], move[3])
                    evalk = self.minimax(gametiles, depth-1, alpha, beta, True)
                    if evalk < minEval and depth == 3:
                        tp.clear()
                        tp.append(move)
                    if evalk == minEval and depth == 3:
                        tp.append(move)
                    minEval = min(minEval, evalk)
                    beta = min(beta, evalk)
                    gametiles = self.revmove(gametiles, move[2], move[3], move[0], move[1], mts)
                    if beta <= alpha:
                        break

                if beta <= alpha:
                    break
            return minEval

        else:
            maxEval = -100000000
            kp, ks = self.eva(gametiles, player)
            for lk in ks:
                for move in lk:
                    mts = gametiles[move[2]][move[3]].pieceonTile
                    gametiles = self.movew(gametiles, move[0], move[1], move[2], move[3])
                    evalk = self.minimax(gametiles, depth-1, alpha, beta, False)
                    maxEval = max(maxEval, evalk)
                    alpha = max(alpha, evalk)
                    gametiles = self.revmove(gametiles, move[2], move[3], move[0], move[1], mts)
                    if beta <= alpha:
                        break
                if beta <= alpha:
                    break

            return maxEval

    def printboard(self, gametilles):
        """
        Print the current state of the board to console.
        
        Args:
            gametilles: The current state of the game board
        """
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|", end='\n')

    def checkeva(self, gametiles, moves):
        """
        Evaluate a list of moves.
        
        Args:
            gametiles: The current state of the game board
            moves: List of moves to evaluate
            
        Returns:
            list: List of evaluated moves with their scores
        """
        arr = []
        for move in moves:
            lk = [[move[2], move[3]]]
            arr.append(self.calci(gametiles, move[0], move[1], lk))

        return arr

    def eva(self, gametiles, player):
        """
        Evaluate all possible moves for the current player.
        
        Args:
            gametiles: The current state of the game board
            player: True for White, False for Black
            
        Returns:
            tuple: Lists of evaluated moves for both players
        """
        lx = []
        moves = []
        kp = []
        ks = []
        movex = move()
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.alliance == 'Black' and player == False:
                    if movex.checkb(gametiles)[0] == 'checked':
                        moves = movex.movesifcheckedb(gametiles)
                        arr = self.checkeva(gametiles, moves)
                        kp = arr
                        return kp, ks
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if len(moves) == 0:
                        continue
                    else:
                        if(gametiles[y][x].pieceonTile.tostring() == 'K'):
                            ax = movex.castlingb(gametiles)
                            if not len(ax) == 0:
                                for l in ax:
                                    if l == 'ks':
                                        moves.append([0, 6])
                                    if l == 'qs':
                                        moves.append([0, 2])
                    if gametiles[y][x].pieceonTile.alliance == 'Black':
                        lx = movex.pinnedb(gametiles, moves, y, x)
                    moves = lx
                    if len(moves) == 0:
                        continue
                    kp.append(self.calci(gametiles, y, x, moves))

                if gametiles[y][x].pieceonTile.alliance == 'White' and player == True:
                    if movex.checkw(gametiles)[0] == 'checked':
                        moves = movex.movesifcheckedw(gametiles)
                        arr = self.checkeva(gametiles, moves)
                        ks = arr
                        return kp, ks
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves == None:
                        print(y)
                        print(x)
                        print(gametiles[y][x].pieceonTile.position)
                    if len(moves) == 0:
                        continue
                    else:
                        if(gametiles[y][x].pieceonTile.tostring() == 'k'):
                            ax = movex.castlingw(gametiles)
                            if not len(ax) == 0:
                                for l in ax:
                                    if l == 'ks':
                                        moves.append([7, 6])
                                    if l == 'qs':
                                        moves.append([7, 2])
                    if gametiles[y][x].pieceonTile.alliance == 'White':
                        lx = movex.pinnedw(gametiles, moves, y, x)
                    moves = lx
                    if len(moves) == 0:
                        continue
                    ks.append(self.calci(gametiles, y, x, moves))

        return kp, ks

    def calci(self, gametiles, y, x, moves):
        """
        Calculate evaluation scores for a list of moves.
        
        Args:
            gametiles: The current state of the game board
            y: Starting row
            x: Starting column
            moves: List of moves to evaluate
            
        Returns:
            list: List of moves with their evaluation scores
        """
        arr = []
        jk = object
        for move in moves:
            jk = gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile = gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile = nullpiece()
            mk = self.calculateb(gametiles)
            gametiles[y][x].pieceonTile = gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile = jk
            arr.append([y, x, move[0], move[1], mk])
        return arr

    def calculateb(self, gametiles):
        piece_values = {
            'P': -100, 'N': -320, 'B': -330, 'R': -500,
            'Q': -900, 'K': -20000,
            'p': 100, 'n': 320, 'b': 330, 'r': 500,
            'q': 900, 'k': 20000
        }
        
        # Position tables for better positional evaluation
        pawn_positions = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        knight_positions = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        value = 0
        
        # Material and positional evaluation
        for y in range(8):
            for x in range(8):
                piece = gametiles[y][x].pieceonTile
                piece_str = piece.tostring()
                
                # Material value
                value += piece_values.get(piece_str, 0)
                
                # Positional value
                if piece_str == 'P':
                    value -= pawn_positions[y][x]
                elif piece_str == 'p':
                    value += pawn_positions[7-y][x]
                elif piece_str == 'N':
                    value -= knight_positions[y][x]
                elif piece_str == 'n':
                    value += knight_positions[7-y][x]
                
                # King safety
                if piece_str in ['K', 'k']:
                    if x in [0, 1, 6, 7] or y in [0, 1, 6, 7]:
                        value -= 100 if piece_str == 'K' else 100
                    else:
                        value += 50 if piece_str == 'K' else -50
                
                # Piece mobility
                if piece_str in ['Q', 'q', 'R', 'r', 'B', 'b', 'N', 'n']:
                    moves = piece.legalmoveb(gametiles)
                    if moves is not None:
                        value += len(moves) * (10 if piece_str.islower() else -10)
                
                # Pawn structure
                if piece_str in ['P', 'p']:
                    if x in [2, 3, 4, 5]:
                        value += 10 if piece_str == 'p' else -10
                    
        return value
    
    #pawn promotion for AI Player
    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
