from pieces.piece import piece
import math

class pawn(piece):
    """Represents a pawn piece in chess"""

    alliance = None  # Color of the pawn (Black or White)
    position = None  # Position on the board (0-63)
    enpassant = False  # Whether the pawn can be captured en passant

    def __init__(self, alliance, position):
        """
        Initialize a pawn
        Args:
            alliance (str): Color of the pawn ("Black" or "White")
            position (int): Starting position on the board (0-63)
        """
        self.alliance = alliance
        self.position = position

    def tostring(self):
        """
        Get string representation of the pawn
        Returns:
            str: "P" for black pawn, "p" for white pawn
        """
        return 'P' if self.alliance == "Black" else "p"

    def calculatecoordinates(self):
        """
        Convert position index to board coordinates
        Returns:
            list: [row, column] coordinates on the board
        """
        a = self.position/8  # Calculate row
        b = self.position%8  # Calculate column
        return [math.floor(a), b]

    def legalmoveb(self, gametiles):
        """
        Calculate all legal moves for this pawn
        Args:
            gametiles: The current state of the board
        Returns:
            list: List of legal move coordinates [row, column]
        """
        legalmoves = []
        x = self.calculatecoordinates()[0]  # Current row
        y = self.calculatecoordinates()[1]  # Current column
        
        if gametiles[x][y].pieceonTile.alliance == 'Black':
            # Black pawn moves (moving down the board)
            if x == 1:  # Starting position
                # Can move forward one or two squares if path is clear
                if gametiles[x+1][y].pieceonTile.tostring() == '-':
                    legalmoves.append([x+1, y])
                    if gametiles[x+2][y].pieceonTile.tostring() == '-':
                        legalmoves.append([x+2, y])
                
                # Can capture diagonally
                if y+1 > 7:  # Right edge
                    if gametiles[x+1][y-1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y-1])
                if y-1 < 0:  # Left edge
                    if gametiles[x+1][y+1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y+1])
                if y+1 < 8 and y-1 >= 0:  # Middle of board
                    if gametiles[x+1][y-1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y-1])
                    if gametiles[x+1][y+1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y+1])
                return legalmoves
            else:
                # Normal moves (not from starting position)
                if gametiles[x+1][y].pieceonTile.tostring() == '-':
                    legalmoves.append([x+1, y])
                if y+1 > 7:  # Right edge
                    if gametiles[x+1][y-1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y-1])
                if y-1 < 0:  # Left edge
                    if gametiles[x+1][y+1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y+1])
                if y+1 < 8 and y-1 >= 0:  # Middle of board
                    if gametiles[x+1][y-1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y-1])
                    if gametiles[x+1][y+1].pieceonTile.alliance == 'White':
                        legalmoves.append([x+1, y+1])
                return legalmoves

        if gametiles[x][y].pieceonTile.alliance == 'White':
            # White pawn moves (moving up the board)
            if x == 6:  # Starting position
                # Can move forward one or two squares if path is clear
                if gametiles[x-1][y].pieceonTile.tostring() == '-':
                    legalmoves.append([x-1, y])
                    if gametiles[x-2][y].pieceonTile.tostring() == '-':
                        legalmoves.append([x-2, y])
                
                # Can capture diagonally
                if y+1 > 7:  # Right edge
                    if gametiles[x-1][y-1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y-1])
                if y-1 < 0:  # Left edge
                    if gametiles[x-1][y+1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y+1])
                if y+1 < 8 and y-1 >= 0:  # Middle of board
                    if gametiles[x-1][y-1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y-1])
                    if gametiles[x-1][y+1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y+1])
                return legalmoves
            else:
                # Normal moves (not from starting position)
                if gametiles[x-1][y].pieceonTile.tostring() == '-':
                    legalmoves.append([x-1, y])
                if y+1 > 7:  # Right edge
                    if gametiles[x-1][y-1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y-1])
                if y-1 < 0:  # Left edge
                    if gametiles[x-1][y+1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y+1])
                if y+1 < 8 and y-1 >= 0:  # Middle of board
                    if gametiles[x-1][y-1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y-1])
                    if gametiles[x-1][y+1].pieceonTile.alliance == 'Black':
                        legalmoves.append([x-1, y+1])
                return legalmoves









