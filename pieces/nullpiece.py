from pieces.piece import piece


class nullpiece(piece):
    """Represents an empty square on the chess board"""
    
    alliance = None  # No alliance since this is an empty square
    
    def __init__(self):
        """Initialize an empty square"""
        pass

    def tostring(self):
        """
        Get string representation of empty square
        Returns:
            str: "-" representing an empty square
        """
        return "-"

