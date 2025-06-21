# Import required piece classes and tile class
from board.tile import Tile  # Import Tile class for board squares
from pieces.nullpiece import nullpiece  # Import empty piece representation
from pieces.queen import queen  # Import queen piece
from pieces.pawn import pawn  # Import pawn piece
from pieces.rook import rook  # Import rook piece
from pieces.bishop import bishop  # Import bishop piece
from pieces.king import king  # Import king piece
from pieces.knight import knight  # Import knight piece

class board:
    # Initialize 8x8 game board with empty tiles
    gameTiles = [[0 for x in range(8)] for y in range(8)]

    def __init__(self):
        """Initialize the chess board"""
        pass

    def createboard(self):
        """Create the initial chess board setup"""
        count = 0  # Initialize position counter
        
        # First create empty board with null pieces
        for rows in range(8):
            for column in range(8):
                self.gameTiles[rows][column] = Tile(count, nullpiece())  # Create empty tile
                count = count + 1  # Increment position counter

        # Set up Black pieces
        self.gameTiles[0][0] = Tile(0, rook("Black", 0))  # Black rook
        self.gameTiles[0][1] = Tile(1, knight("Black", 1))  # Black knight
        self.gameTiles[0][2] = Tile(2, bishop("Black", 2))  # Black bishop
        self.gameTiles[0][3] = Tile(3, queen("Black", 3))  # Black queen
        self.gameTiles[0][4] = Tile(4, king("Black", 4))  # Black king
        self.gameTiles[0][5] = Tile(5, bishop("Black", 5))  # Black bishop
        self.gameTiles[0][6] = Tile(6, knight("Black", 6))  # Black knight
        self.gameTiles[0][7] = Tile(7, rook("Black", 7))  # Black rook
        
        # Set up Black pawns
        for i in range(8):
            self.gameTiles[1][i] = Tile(8+i, pawn("Black", 8+i))  # Black pawns

        # Set up White pawns
        for i in range(8):
            self.gameTiles[6][i] = Tile(48+i, pawn("White", 48+i))  # White pawns

        # Set up White pieces
        self.gameTiles[7][0] = Tile(56, rook("White", 56))  # White rook
        self.gameTiles[7][1] = Tile(57, knight("White", 57))  # White knight
        self.gameTiles[7][2] = Tile(58, bishop("White", 58))  # White bishop
        self.gameTiles[7][3] = Tile(59, queen("White", 59))  # White queen
        self.gameTiles[7][4] = Tile(60, king("White", 60))  # White king
        self.gameTiles[7][5] = Tile(61, bishop("White", 61))  # White bishop
        self.gameTiles[7][6] = Tile(62, knight("White", 62))  # White knight
        self.gameTiles[7][7] = Tile(63, rook("White", 63))  # White rook

    def printboard(self):
        """Print the current state of the board to console"""
        count = 0  # Initialize counter
        for rows in range(8):
            for column in range(8):
                # Print each piece's string representation
                print('|', end=self.gameTiles[rows][column].pieceonTile.tostring())
            print("|", end='\n')  # New line after each row
