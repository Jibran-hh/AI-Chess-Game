# Import required piece class
from pieces.nullpiece import nullpiece  # Import empty piece representation

class Tile:
    """Represents a single square on the chess board"""
    
    def __init__(self, pos, piece):
        """
        Initialize a tile with position and piece
        Args:
            pos (int): Position index on the board (0-63)
            piece: The chess piece on this tile (or nullpiece if empty)
        """
        self.pos = pos  # Store position index
        self.pieceonTile = piece  # Store the piece on this tile

    def haspiece(self):
        """
        Check if this tile has a piece on it
        Returns:
            bool: True if tile has a piece, False if empty
        """
        return not isinstance(self.pieceonTile, nullpiece)  # Check if piece is not a nullpiece

    def getpiece(self):
        """
        Get the piece on this tile
        Returns:
            The chess piece on this tile
        """
        return self.pieceonTile  # Return the piece

    def setpiece(self, piece):
        """
        Place a piece on this tile
        Args:
            piece: The chess piece to place on this tile
        """
        self.pieceonTile = piece  # Set the new piece