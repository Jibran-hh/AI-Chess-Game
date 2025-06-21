"""
Human player module implementing a chess player that accepts user input for moves.
This module contains the HumanPlayer class that handles human player interactions and move validation.
"""

from board.move import move

class HumanPlayer:
    """
    HumanPlayer class that implements a chess player controlled by human input.
    The class handles move validation and execution for human players.
    """

    def __init__(self, color="White"):
        """Initialize the human player"""
        self.color = color
        self.move_handler = move()

    def get_valid_moves(self, board, piece_pos):
        """Get valid moves for a selected piece"""
        x, y = piece_pos
        moves = []
        if board.gameTiles[y][x].pieceonTile.alliance == self.color:
            moves = board.gameTiles[y][x].pieceonTile.legalmoveb(board.gameTiles)
            if board.gameTiles[y][x].pieceonTile.tostring() == 'k':
                # Handle castling for king
                ax = self.move_handler.castlingw(board.gameTiles)
                if ax:
                    for l in ax:
                        if l == 'ks':
                            moves.append([7, 6])
                        if l == 'qs':
                            moves.append([7, 2])
            
            # Handle en passant for pawns
            if board.gameTiles[y][x].pieceonTile.tostring() == 'p':
                ay = self.move_handler.enpassantb(board.gameTiles, y, x)
                if ay:
                    if ay[1] == 'r':
                        moves.append([y-1, x+1])
                    else:
                        moves.append([y-1, x-1])
            
            # Filter moves based on pins
            moves = self.move_handler.pinnedw(board.gameTiles, moves, y, x)
        
        return moves

    def validate_move(self, board, from_pos, to_pos):
        """Validate if a move is legal"""
        valid_moves = self.get_valid_moves(board, from_pos)
        return to_pos in valid_moves

    def make_move(self, board, from_pos, to_pos):
        """Make a move on the board"""
        if self.validate_move(board, from_pos, to_pos):
            fx, fy = from_pos
            tx, ty = to_pos
            
            # Handle special moves (castling, en passant, promotion)
            piece = board.gameTiles[fy][fx].pieceonTile
            
            # Update piece position
            board.gameTiles[ty][tx].pieceonTile = piece
            board.gameTiles[fy][fx].pieceonTile = None
            
            # Handle pawn promotion
            if piece.tostring() == 'p' and ty == 0:
                return "promotion"
            
            return True
        return False 