from pieces.piece import piece
import math

class bishop(piece):
    """Represents a bishop piece in chess"""

    alliance = None  # Color of the bishop (Black or White)
    position = None  # Position on the board (0-63)

    def __init__(self, alliance, position):
        """
        Initialize a bishop
        Args:
            alliance (str): Color of the bishop ("Black" or "White")
            position (int): Starting position on the board (0-63)
        """
        self.alliance = alliance
        self.position = position

    def tostring(self):
        """
        Get string representation of the bishop
        Returns:
            str: "B" for black bishop, "b" for white bishop
        """
        return 'B' if self.alliance == "Black" else "b"

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
        Calculate all legal moves for this bishop
        Args:
            gameTiles: The current state of the board
        Returns:
            list: List of legal move coordinates [row, column]
        """
        legalmoves = []
        x = self.calculatecoordinates()[0]  # Current row
        y = self.calculatecoordinates()[1]  # Current column
        a = 0  # Temporary row coordinate
        b = 0  # Temporary column coordinate
        count = 0  # Counter for move calculation

        if gameTiles[x][y].pieceonTile.alliance == 'Black':
            # Check moves in all four diagonal directions
            # Moving down-right
            while True:
                if count == 0:
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                # Can move until hitting a piece or board edge
                if a < 8 and b < 8 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a < 8 and b < 8 and gameTiles[a][b].pieceonTile.alliance == 'White':
                    legalmoves.append([a, b])  # Can capture white piece
                    break
                else:
                    break

            # Moving down-left
            count = 0
            while True:
                if count == 0:
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if a < 8 and b >= 0 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a < 8 and b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'White':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            # Moving up-right
            count = 0
            while True:
                if count == 0:
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if a >= 0 and b < 8 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a >= 0 and b < 8 and gameTiles[a][b].pieceonTile.alliance == 'White':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            # Moving up-left
            count = 0
            while True:
                if count == 0:
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if a >= 0 and b >= 0 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a >= 0 and b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'White':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves

        else:  # White bishop
            # Same logic as black bishop but checking for black pieces to capture
            while True:
                if count == 0:
                    a = x + 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b + 1
                if a < 8 and b < 8 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a < 8 and b < 8 and gameTiles[a][b].pieceonTile.alliance == 'Black':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if count == 0:
                    a = x + 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a + 1
                    b = b - 1
                if a < 8 and b >= 0 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a < 8 and b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'Black':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if count == 0:
                    a = x - 1
                    b = y + 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b + 1
                if a >= 0 and b < 8 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a >= 0 and b < 8 and gameTiles[a][b].pieceonTile.alliance == 'Black':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            count = 0
            while True:
                if count == 0:
                    a = x - 1
                    b = y - 1
                    count = count + 1
                else:
                    a = a - 1
                    b = b - 1
                if a >= 0 and b >= 0 and gameTiles[a][b].pieceonTile.alliance is None:
                    legalmoves.append([a, b])
                    continue
                elif a >= 0 and b >= 0 and gameTiles[a][b].pieceonTile.alliance == 'Black':
                    legalmoves.append([a, b])
                    break
                else:
                    break

            return legalmoves









