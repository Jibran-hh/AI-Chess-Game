from pieces.piece import piece
import math

class king(piece):
    """Represents a king piece in chess"""

    alliance = None  # Color of the king (Black or White)
    position = None  # Position on the board (0-63)
    moved = False  # Whether the king has moved (used for castling)

    def __init__(self, alliance, position):
        """
        Initialize a king
        Args:
            alliance (str): Color of the king ("Black" or "White")
            position (int): Starting position on the board (0-63)
        """
        self.alliance = alliance
        self.position = position

    def tostring(self):
        """
        Get string representation of the king
        Returns:
            str: "K" for black king, "k" for white king
        """
        return 'K' if self.alliance == "Black" else "k"

    def calculatecoordinates(self):
        """
        Convert position index to board coordinates
        Returns:
            list: [row, column] coordinates on the board
        """
        a = self.position/8  # Calculate row
        b = self.position%8  # Calculate column
        return [math.floor(a), b]

    def legalmoveb(self, gameTiles):
        """
        Calculate all legal moves for this king
        Args:
            gameTiles: The current state of the board
        Returns:
            list: List of legal move coordinates [row, column]
        """
        legalmoves = []
        x = self.calculatecoordinates()[0]  # Current row
        y = self.calculatecoordinates()[1]  # Current column

        if gameTiles[x][y].pieceonTile.alliance == 'Black':
            # Check all eight possible moves (one square in any direction)
            # Down-right diagonal
            if x+1 < 8 and y+1 < 8 and not gameTiles[x+1][y+1].pieceonTile.alliance == 'Black':
                legalmoves.append([x+1, y+1])

            # Down-left diagonal
            if x+1 < 8 and y-1 >= 0 and not gameTiles[x+1][y-1].pieceonTile.alliance == 'Black':
                legalmoves.append([x+1, y-1])

            # Down
            if x+1 < 8 and not gameTiles[x+1][y].pieceonTile.alliance == 'Black':
                legalmoves.append([x+1, y])

            # Left
            if y-1 >= 0 and not gameTiles[x][y-1].pieceonTile.alliance == 'Black':
                legalmoves.append([x, y-1])

            # Right
            if y+1 < 8 and not gameTiles[x][y+1].pieceonTile.alliance == 'Black':
                legalmoves.append([x, y+1])

            # Up
            if x-1 >= 0 and not gameTiles[x-1][y].pieceonTile.alliance == 'Black':
                legalmoves.append([x-1, y])

            # Up-right diagonal
            if x-1 >= 0 and y-1 >= 0 and not gameTiles[x-1][y-1].pieceonTile.alliance == 'Black':
                legalmoves.append([x-1, y-1])

            # Up-left diagonal
            if x-1 >= 0 and y+1 < 8 and not gameTiles[x-1][y+1].pieceonTile.alliance == 'Black':
                legalmoves.append([x-1, y+1])

            return legalmoves

        else:  # White king
            # Same logic as black king but checking for black pieces
            # Down-right diagonal
            if x+1 < 8 and y+1 < 8 and not gameTiles[x+1][y+1].pieceonTile.alliance == 'White':
                legalmoves.append([x+1, y+1])

            # Down-left diagonal
            if x+1 < 8 and y-1 >= 0 and not gameTiles[x+1][y-1].pieceonTile.alliance == 'White':
                legalmoves.append([x+1, y-1])

            # Down
            if x+1 < 8 and not gameTiles[x+1][y].pieceonTile.alliance == 'White':
                legalmoves.append([x+1, y])

            # Left
            if y-1 >= 0 and not gameTiles[x][y-1].pieceonTile.alliance == 'White':
                legalmoves.append([x, y-1])

            # Right
            if y+1 < 8 and not gameTiles[x][y+1].pieceonTile.alliance == 'White':
                legalmoves.append([x, y+1])

            # Up
            if x-1 >= 0 and not gameTiles[x-1][y].pieceonTile.alliance == "White":
                legalmoves.append([x-1, y])

            # Up-right diagonal
            if x-1 >= 0 and y-1 >= 0 and not gameTiles[x-1][y-1].pieceonTile.alliance == 'White':
                legalmoves.append([x-1, y-1])

            # Up-left diagonal
            if x-1 >= 0 and y+1 < 8 and not gameTiles[x-1][y+1].pieceonTile.alliance == 'White':
                legalmoves.append([x-1, y+1])

            return legalmoves





