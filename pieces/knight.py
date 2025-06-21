from pieces.piece import piece
import math

class knight(piece):
    """Represents a knight piece in chess"""

    alliance = None  # Color of the knight (Black or White)
    position = None  # Position on the board (0-63)

    def __init__(self, alliance, position):
        """
        Initialize a knight
        Args:
            alliance (str): Color of the knight ("Black" or "White")
            position (int): Starting position on the board (0-63)
        """
        self.alliance = alliance
        self.position = position

    def tostring(self):
        """
        Get string representation of the knight
        Returns:
            str: "N" for black knight, "n" for white knight
        """
        return 'N' if self.alliance == "Black" else "n"

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
        Calculate all legal moves for this knight
        Args:
            gameTiles: The current state of the board
        Returns:
            list: List of legal move coordinates [row, column]
        """
        legalmoves = []
        x = self.calculatecoordinates()[0]  # Current row
        y = self.calculatecoordinates()[1]  # Current column

        # All possible knight moves (L-shaped)
        # Each move is 2 squares in one direction and 1 square perpendicular
        possible_moves = [
            [x+2, y+1], [x+2, y-1],  # Down 2, right/left 1
            [x-2, y+1], [x-2, y-1],  # Up 2, right/left 1
            [x+1, y+2], [x+1, y-2],  # Right 2, down/up 1
            [x-1, y+2], [x-1, y-2]   # Left 2, down/up 1
        ]

        # Check each possible move
        for move in possible_moves:
            a = move[0]  # Target row
            b = move[1]  # Target column
            
            # Check if move is within board boundaries
            if a >= 0 and a < 8 and b >= 0 and b < 8:
                # For black knight
                if gameTiles[x][y].pieceonTile.alliance == 'Black':
                    # Can move to empty square or capture white piece
                    if gameTiles[a][b].pieceonTile.alliance is None or gameTiles[a][b].pieceonTile.alliance == 'White':
                        legalmoves.append([a, b])
                # For white knight
                else:
                    # Can move to empty square or capture black piece
                    if gameTiles[a][b].pieceonTile.alliance is None or gameTiles[a][b].pieceonTile.alliance == 'Black':
                        legalmoves.append([a, b])

        return legalmoves


















