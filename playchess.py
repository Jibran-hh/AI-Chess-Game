# Import required libraries and modules
import pygame  # Main game library for graphics and event handling
from board.chessboard import board  # Chess board representation
import math  # For mathematical calculations
from pieces.nullpiece import nullpiece  # Empty piece representation
from pieces.queen import queen  # Queen piece
from pieces.rook import rook  # Rook piece
from pieces.knight import knight  # Knight piece
from pieces.bishop import bishop  # Bishop piece
from player.AI import AI  # AI opponent
import copy  # For deep copying game state
from board.move import move  # Move validation and execution

# Initialize Pygame
pygame.init()
gamedisplay = pygame.display.set_mode((800, 800))  # Create 800x800 game window
pygame.display.set_caption("pychess")  # Set window title
clock = pygame.time.Clock()  # Clock for controlling frame rate

# Initialize game components
chessBoard = board()  # Create chess board
chessBoard.createboard()  # Set up initial piece positions
chessBoard.printboard()  # Print board state to console
movex = move()  # Move handler
ai = AI()  # AI opponent

# Lists to store game elements
allTiles = []  # Store all board tiles
allpieces = []  # Store all pieces with their images and positions

######################
######################
# UI Colors and Styling
BACKGROUND_COLOR = (40, 40, 40)  # Dark gray background
TITLE_COLOR = (255, 215, 0)      # Gold for titles
BUTTON_COLOR = (101, 67, 33)     # Dark brown for buttons
BUTTON_HOVER_COLOR = (139, 69, 19)  # Darker brown for button hover
TEXT_COLOR = (255, 248, 220)     # Cream white for text
BORDER_COLOR = (255, 215, 0)     # Gold for borders
HIGHLIGHT_COLOR = (255, 0, 0, 128)  # Semi-transparent red for highlighting
VALID_MOVE_COLOR = (0, 255, 0, 128)  # Semi-transparent green for valid moves
STATUS_BAR_COLOR = (30, 30, 30)  # Darker gray for status bar

# Fonts for different text elements
font = pygame.font.Font('freesansbold.ttf', 64)  # Large font for titles
button_font = pygame.font.Font('freesansbold.ttf', 32)  # Medium font for buttons
status_font = pygame.font.Font('freesansbold.ttf', 24)  # Small font for status messages

# Text elements for UI
text = font.render('AI Chess Game', True, TITLE_COLOR)  # Main title
text1 = button_font.render('Start Game', True, TEXT_COLOR)  # Start button text
text3 = font.render('Black won by checkmate', True, TEXT_COLOR)  # Black win message
text4 = font.render('White won by checkmate', True, TEXT_COLOR)  # White win message
text5 = font.render('Stalemate', True, TEXT_COLOR)  # Stalemate message

# Center all text elements
textRect = text.get_rect()
textRect1 = text1.get_rect()
textRect3 = text3.get_rect()
textRect4 = text4.get_rect()
textRect5 = text5.get_rect()

textRect.center = (400, 150)  # Center title
textRect1.center = (400, 350)  # Center start button text
textRect3.center = (400, 400)  # Center black win message
textRect4.center = (400, 400)  # Center white win message
textRect5.center = (400, 400)  # Center stalemate message

# Button rectangle for start game
button1_rect = pygame.Rect(300, 300, 200, 100)

# Game state variables
saki = ''  # Game mode/state
quitgame = False  # Flag to exit game

# Status bar setup
STATUS_BAR_HEIGHT = 40  # Height of status bar in pixels
STATUS_BAR_Y = 800 - STATUS_BAR_HEIGHT  # Y position of status bar

def draw_status_bar():
    """
    Draw the status bar at the bottom of the game window.
    This bar displays game status messages.
    """
    # Draw status bar background
    pygame.draw.rect(gamedisplay, STATUS_BAR_COLOR, [0, STATUS_BAR_Y, 800, STATUS_BAR_HEIGHT])
    pygame.draw.line(gamedisplay, BORDER_COLOR, (0, STATUS_BAR_Y), (800, STATUS_BAR_Y), 2)

def draw_status_message(message, color=TEXT_COLOR):
    """
    Display a message in the status bar.
    
    Args:
        message (str): The message to display
        color (tuple): RGB color for the text
    """
    draw_status_bar()
    text = status_font.render(message, True, color)
    rect = text.get_rect()
    rect.center = (400, STATUS_BAR_Y + STATUS_BAR_HEIGHT // 2)
    gamedisplay.blit(text, rect)

# Main menu loop
while not quitgame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitgame = True
            pygame.quit()
            quit()

        # Fill background
        gamedisplay.fill(BACKGROUND_COLOR)
        
        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw button with hover effect
        if button1_rect.collidepoint(mouse_pos):
            pygame.draw.rect(gamedisplay, BUTTON_HOVER_COLOR, button1_rect)
            pygame.draw.rect(gamedisplay, BORDER_COLOR, button1_rect, 2)  # Gold border
        else:
            pygame.draw.rect(gamedisplay, BUTTON_COLOR, button1_rect)
            pygame.draw.rect(gamedisplay, BORDER_COLOR, button1_rect, 2)  # Gold border

        # Draw text elements
        gamedisplay.blit(text, textRect)
        gamedisplay.blit(text1, textRect1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(event.pos):
                saki = 'ai'  # Set game mode to AI vs Human
                quitgame = True

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

def square(x, y, w, h, color):
    """
    Draw a square on the game board.
    
    Args:
        x, y (int): Position coordinates
        w, h (int): Width and height of square
        color (tuple): RGB color of square
    """
    pygame.draw.rect(gamedisplay, color, [x, y, w, h])
    allTiles.append([color, [x, y, w, h]])

def drawchesspieces():
    """
    Draw the chess board and all pieces.
    This function creates the visual representation of the game state.
    """
    xpos = 0
    ypos = 0
    color = 0
    width = 100
    height = 100
    black = (101, 67, 33)  # Dark brown for black squares
    white = (255, 248, 220)  # Cream white for white squares
    number = 0

    # Clear previous pieces
    allTiles.clear()
    allpieces.clear()

    # Draw the 8x8 chess board
    for rows in range(8):
        for column in range(8):
            if color % 2 == 0:
                square(xpos, ypos, width, height, white)
                # If there's a piece on this tile, load and draw its image
                if not chessBoard.gameTiles[rows][column].pieceonTile.tostring() == "-":
                    img = pygame.image.load("./chessart/"
                                            + chessBoard.gameTiles[rows][column].pieceonTile.alliance[0].upper()
                                            + chessBoard.gameTiles[rows][column].pieceonTile.tostring().upper()
                                            + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    allpieces.append([img, [xpos, ypos], chessBoard.gameTiles[rows][column].pieceonTile])

                xpos += 100

            else:
                square(xpos, ypos, width, height, black)
                # If there's a piece on this tile, load and draw its image
                if not chessBoard.gameTiles[rows][column].pieceonTile.tostring() == "-":
                    img = pygame.image.load("./chessart/"
                                        + chessBoard.gameTiles[rows][column].pieceonTile.alliance[0].upper()
                                        + chessBoard.gameTiles[rows][column].pieceonTile.tostring().upper()
                                        + ".png")
                    img = pygame.transform.scale(img, (100, 100))
                    allpieces.append([img, [xpos, ypos], chessBoard.gameTiles[rows][column].pieceonTile])

                xpos += 100

            color += 1
            number += 1

        color += 1
        xpos = 0
        ypos += 100
        # Draw all pieces on the board
        for img in allpieces:
            gamedisplay.blit(img[0], img[1])

def updateposition(x, y):
    """
    Convert board coordinates to position index.
    
    Args:
        x, y (int): Board coordinates (row, column)
        
    Returns:
        int: Position index (0-63)
    """
    a = x * 8
    b = a + y
    return b

def givecolour(x, y):
    """
    Determine the color of a square at given coordinates.
    
    Args:
        x, y (int): Board coordinates
        
    Returns:
        list: RGB color values
    """
    if y % 2 == 0:
        if x % 2 == 0:
            return [143, 155, 175]  # Light blue
        else:
            return [66, 134, 244]  # Dark blue
    else:
        if x % 2 == 0:
            return [66, 134, 244]  # Dark blue
        else:
            return [143, 155, 175]  # Light blue

# Main game loop for AI vs Human mode
if saki == 'ai':
    moves = []  # Store valid moves for selected piece
    enpassant = []  # Store en passant information
    promote = []  # Store promotion information
    promotion = False  # Flag for pawn promotion
    turn = 0  # Track whose turn it is (0 = White, 1 = Black)

    array = []  # Temporary array for move calculations
    quitgame = False

    # Main game loop
    while not quitgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame = True
                pygame.quit()
                quit()

            # Check for checkmate conditions
            if movex.checkw(chessBoard.gameTiles)[0] == 'checked' and len(moves) == 0:
                array = movex.movesifcheckedw(chessBoard.gameTiles)
                if len(array) == 0:
                    saki = 'end1'  # Black wins by checkmate
                    quitgame = True
                    break

            if movex.checkb(chessBoard.gameTiles)[0] == 'checked' and len(moves) == 0:
                array = movex.movesifcheckedb(chessBoard.gameTiles)
                if len(array) == 0:
                    saki = 'end2'  # White wins by checkmate
                    quitgame = True
                    break

            # Check for stalemate conditions
            if movex.checkb(chessBoard.gameTiles)[0] == 'notchecked' and turn % 2 == 1 and len(moves) == 0:
                check = False
                for x in range(8):
                    for y in range(8):
                        if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'Black' and turn % 2 == 1:
                            moves1 = chessBoard.gameTiles[y][x].pieceonTile.legalmoveb(chessBoard.gameTiles)
                            lx1 = movex.pinnedb(chessBoard.gameTiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    saki = 'end3'  # Stalemate
                    quitgame = True
                    break

            if movex.checkw(chessBoard.gameTiles)[0] == 'notchecked' and turn % 2 == 0 and len(moves) == 0:
                check = False
                for x in range(8):
                    for y in range(8):
                        if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'White' and turn % 2 == 0:
                            moves1 = chessBoard.gameTiles[y][x].pieceonTile.legalmoveb(chessBoard.gameTiles)
                            lx1 = movex.pinnedw(chessBoard.gameTiles, moves1, y, x)
                            if len(lx1) == 0:
                                continue
                            else:
                                check = True
                            if check == True:
                                break
                    if check == True:
                        break

                if check == False:
                    saki = 'end3'  # Stalemate
                    quitgame = True

            # AI's turn (Black)
            if not turn % 2 == 0 and promotion == False:
                turn = turn + 1
                sc = copy.deepcopy(chessBoard.gameTiles)
                y, x, fx, fy = ai.evaluate(sc)  # AI evaluates the board and chooses a move
                m = fy
                n = fx
                
                # Handle special moves for AI
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'K' or chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'R':
                    chessBoard.gameTiles[y][x].pieceonTile.moved = True

                # Castling for AI
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'K' and m == x + 2:
                    chessBoard.gameTiles[y][x+1].pieceonTile = chessBoard.gameTiles[y][x+3].pieceonTile
                    s = updateposition(y, x+1)
                    chessBoard.gameTiles[y][x+1].pieceonTile.position = s
                    chessBoard.gameTiles[y][x+3].pieceonTile = nullpiece()
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'K' and m == x - 2:
                    chessBoard.gameTiles[y][x-1].pieceonTile = chessBoard.gameTiles[y][0].pieceonTile
                    s = updateposition(y, x-1)
                    chessBoard.gameTiles[y][x-1].pieceonTile.position = s
                    chessBoard.gameTiles[y][0].pieceonTile = nullpiece()

                # En passant for AI
                if not len(enpassant) == 0:
                    chessBoard.gameTiles[enpassant[0]][enpassant[1]].pieceonTile.enpassant = False
                    enpassant = []
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P' and y + 1 == n and x + 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
                    chessBoard.gameTiles[y][x+1].pieceonTile = nullpiece()
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P' and y + 1 == n and x - 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
                    chessBoard.gameTiles[y][x-1].pieceonTile = nullpiece()

                # Pawn moves for AI
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P' and n == y + 2:
                    chessBoard.gameTiles[y][x].pieceonTile.enpassant = True
                    enpassant = [n, m]

                # Pawn promotion for AI
                if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P' and y + 1 == n and y == 6:
                    promotion = True

                # Execute AI move
                if promotion == False:
                    chessBoard.gameTiles[n][m].pieceonTile = chessBoard.gameTiles[y][x].pieceonTile
                    chessBoard.gameTiles[y][x].pieceonTile = nullpiece()
                    s = updateposition(n, m)
                    chessBoard.gameTiles[n][m].pieceonTile.position = s
                    allTiles.clear()
                    allpieces.clear()
                    chessBoard.printboard()
                    drawchesspieces()
                    moves = []

                # Handle pawn promotion for AI
                if promotion == True:
                    if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P':
                        chessBoard.gameTiles[y][x].pieceonTile = nullpiece()
                        chessBoard.gameTiles[n][m].pieceonTile = queen('Black', updateposition(n, m))
                        allTiles.clear()
                        allpieces.clear()
                        chessBoard.printboard()
                        drawchesspieces()
                        moves = []
                        promote = []
                        promotion = False

            # Handle human player's moves
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle moves when in check
                if movex.checkw(chessBoard.gameTiles)[0] == 'checked' and len(moves) == 0:
                    array = movex.movesifcheckedw(chessBoard.gameTiles)
                    coord = pygame.mouse.get_pos()
                    m = math.floor(coord[0]/100)
                    n = math.floor(coord[1]/100)
                    imgx = pygame.transform.scale(pygame.image.load("./chessart/red_square.png",), (100, 100))
                    mx = []
                    ma = []
                    for move in array:
                        if(move[1] == m and move[0] == n):
                            mx = [move[3]*100, move[2]*100]
                            ma = [move[2], move[3]]
                            moves.append(ma)
                            gamedisplay.blit(imgx, mx)
                            x = move[1]
                            y = move[0]
                    break

                # Handle pawn promotion
                if not len(promote) == 0:
                    coord = pygame.mouse.get_pos()
                    m = math.floor(coord[0]/100)
                    n = math.floor(coord[1]/100)
                    if chessBoard.gameTiles[promote[5][0]][promote[5][1]].pieceonTile.alliance == 'White':
                        for i in range(len(promote)):
                            if i == 4:
                                turn = turn - 1
                                break
                            if promote[i][0] == n and promote[i][1] == m:
                                if i == 0:
                                    chessBoard.gameTiles[promote[4][1]][promote[4][0]].pieceonTile = queen('White', updateposition(promote[4][1], promote[4][0]))
                                    chessBoard.gameTiles[promote[5][0]][promote[5][1]].pieceonTile = nullpiece()
                                    break
                                if i == 1:
                                    chessBoard.gameTiles[promote[4][1]][promote[4][0]].pieceonTile = rook('White', updateposition(promote[4][1], promote[4][0]))
                                    chessBoard.gameTiles[promote[5][0]][promote[5][1]].pieceonTile = nullpiece()
                                    break
                                if i == 2:
                                    chessBoard.gameTiles[promote[4][1]][promote[4][0]].pieceonTile = knight('White', updateposition(promote[4][1], promote[4][0]))
                                    chessBoard.gameTiles[promote[5][0]][promote[5][1]].pieceonTile = nullpiece()
                                    break
                                if i == 3:
                                    chessBoard.gameTiles[promote[4][1]][promote[4][0]].pieceonTile = bishop('White', updateposition(promote[4][1], promote[4][0]))
                                    chessBoard.gameTiles[promote[5][0]][promote[5][1]].pieceonTile = nullpiece()
                                    break

                    allTiles.clear()
                    allpieces.clear()
                    chessBoard.printboard()
                    drawchesspieces()
                    promote = []
                    promotion = False

                # Handle piece selection and movement
                if not len(moves) == 0:
                    coord = pygame.mouse.get_pos()
                    m = math.floor(coord[0]/100)
                    n = math.floor(coord[1]/100)
                    for move in moves:
                        if move[0] == n and move[1] == m:
                            turn = turn + 1
                            
                            # Handle special moves for human player
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'k' or chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'r':
                                chessBoard.gameTiles[y][x].pieceonTile.moved = True

                            # Castling for human player
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'k' and m == x + 2:
                                chessBoard.gameTiles[y][x+1].pieceonTile = chessBoard.gameTiles[y][x+3].pieceonTile
                                s = updateposition(y, x+1)
                                chessBoard.gameTiles[y][x+1].pieceonTile.position = s
                                chessBoard.gameTiles[y][x+3].pieceonTile = nullpiece()
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'k' and m == x - 2:
                                chessBoard.gameTiles[y][x-1].pieceonTile = chessBoard.gameTiles[y][0].pieceonTile
                                s = updateposition(y, x-1)
                                chessBoard.gameTiles[y][x-1].pieceonTile.position = s
                                chessBoard.gameTiles[y][0].pieceonTile = nullpiece()

                            # En passant for human player
                            if not len(enpassant) == 0:
                                chessBoard.gameTiles[enpassant[0]][enpassant[1]].pieceonTile.enpassant = False
                                enpassant = []

                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p' and y - 1 == n and x + 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
                                chessBoard.gameTiles[y][x+1].pieceonTile = nullpiece()
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p' and y - 1 == n and x - 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
                                chessBoard.gameTiles[y][x-1].pieceonTile = nullpiece()

                            # Pawn moves for human player
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p' and n == y - 2:
                                chessBoard.gameTiles[y][x].pieceonTile.enpassant = True
                                enpassant = [n, m]

                            # Pawn promotion for human player
                            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p' and y - 1 == n and y == 1:
                                promotion = True

                            # Execute human move
                            if promotion == False:
                                chessBoard.gameTiles[n][m].pieceonTile = chessBoard.gameTiles[y][x].pieceonTile
                                chessBoard.gameTiles[y][x].pieceonTile = nullpiece()
                                s = updateposition(n, m)
                                chessBoard.gameTiles[n][m].pieceonTile.position = s
                    if promotion == False:
                        allTiles.clear()
                        allpieces.clear()
                        chessBoard.printboard()
                        drawchesspieces()
                        moves = []

                    # Handle pawn promotion UI for human player
                    if promotion == True:
                        if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p' and x == 7 and y == 1:
                            pygame.draw.rect(gamedisplay, (0, 0, 0), [x*100-100, (y*100)+100, 200, 200])
                            imgx = pygame.transform.scale(pygame.image.load("./chessart/WQ.png",), (100, 100))
                            imgx1 = pygame.transform.scale(pygame.image.load("./chessart/WR.png",), (100, 100))
                            imgx2 = pygame.transform.scale(pygame.image.load("./chessart/WN.png",), (100, 100))
                            imgx3 = pygame.transform.scale(pygame.image.load("./chessart/WB.png",), (100, 100))
                            gamedisplay.blit(imgx, [x*100-100, (y*100)+200])
                            gamedisplay.blit(imgx1, [(x*100), (y*100)+200])
                            gamedisplay.blit(imgx2, [x*100-100, (y*100)+100])
                            gamedisplay.blit(imgx3, [(x*100), (y*100)+100])
                            promote = [[y+2, x-1], [y+2, x], [y+1, x], [y+1, x], [m, n], [y, x]]

                        elif chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p':
                            pygame.draw.rect(gamedisplay, (0, 0, 0), [x*100, (y*100)+100, 200, 200])
                            imgx = pygame.transform.scale(pygame.image.load("./chessart/WQ.png",), (100, 100))
                            imgx1 = pygame.transform.scale(pygame.image.load("./chessart/WR.png",), (100, 100))
                            imgx2 = pygame.transform.scale(pygame.image.load("./chessart/WN.png",), (100, 100))
                            imgx3 = pygame.transform.scale(pygame.image.load("./chessart/WB.png",), (100, 100))
                            gamedisplay.blit(imgx, [x*100, (y*100)+200])
                            gamedisplay.blit(imgx1, [(x*100)+100, (y*100)+200])
                            gamedisplay.blit(imgx2, [x*100, (y*100)+100])
                            gamedisplay.blit(imgx3, [(x*100)+100, (y*100)+100])
                            promote = [[y+2, x], [y+2, x+1], [y+1, x], [y+1, x+1], [m, n], [y, x]]

                else:
                    drawchesspieces()
                    coords = pygame.mouse.get_pos()
                    x = math.floor(coords[0]/100)
                    y = math.floor(coords[1]/100)
                    mx = []
                    
                    # Calculate valid moves for selected piece
                    if(chessBoard.gameTiles[y][x].pieceonTile.alliance == 'White'):
                        moves = chessBoard.gameTiles[y][x].pieceonTile.legalmoveb(chessBoard.gameTiles)
                        
                        # Handle special moves for king
                        if(chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'k'):
                            ax = movex.castlingw(chessBoard.gameTiles)
                            if not len(ax) == 0:
                                for l in ax:
                                    if l == 'ks':
                                        moves.append([7, 6])
                                    if l == 'qs':
                                        moves.append([7, 2])
                        
                        # Handle en passant for pawns
                        if(chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p'):
                            ay = movex.enpassantb(chessBoard.gameTiles, y, x)
                            if not len(ay) == 0:
                                if ay[1] == 'r':
                                    moves.append([y-1, x+1])
                                else:
                                    moves.append([y-1, x-1])

                    # Filter moves based on pins
                    if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'White':
                        lx = movex.pinnedw(chessBoard.gameTiles, moves, y, x)
                    moves = lx

                    # AI thinking message
                    if not turn % 2 == 0:
                        draw_status_message("AI is thinking...")
                        pygame.display.update()
                        # AI move logic here
                        draw_status_message("Your turn")

                    # Only allow moves for white pieces
                    if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'Black':
                        moves = []

                    # No moves for empty squares
                    if chessBoard.gameTiles[y][x].pieceonTile.tostring() == '-':
                        moves = []

                    # Highlight selected piece and valid moves
                    imgx = pygame.transform.scale(pygame.image.load("./chessart/red_square.png",), (100, 100))
                    for move in moves:
                        mx = [move[1]*100, move[0]*100]
                        gamedisplay.blit(imgx, mx)

        # Draw all pieces on the board
        for img in allpieces:
            gamedisplay.blit(img[0], img[1])

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

# Game over screen for Black win (checkmate)
if saki == 'end1':
    quitgame = False
    while not quitgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame = True
                pygame.quit()
                quit()

            gamedisplay.fill(BACKGROUND_COLOR)
            gamedisplay.blit(text3, textRect3)
            draw_status_message("Game Over - Black wins by checkmate!", (255, 0, 0))
            pygame.display.update()
            clock.tick(60)

# Game over screen for White win (checkmate)
if saki == 'end2':
    quitgame = False
    while not quitgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame = True
                pygame.quit()
                quit()

            gamedisplay.fill(BACKGROUND_COLOR)
            gamedisplay.blit(text4, textRect4)
            draw_status_message("Game Over - White wins by checkmate!", (255, 0, 0))
            pygame.display.update()
            clock.tick(60)

# Game over screen for Stalemate
if saki == 'end3':
    quitgame = False
    while not quitgame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame = True
                pygame.quit()
                quit()

            gamedisplay.fill(BACKGROUND_COLOR)
            gamedisplay.blit(text5, textRect5)
            draw_status_message("Game Over - Stalemate!", (255, 215, 0))  # Gold color for stalemate
            pygame.display.update()
            clock.tick(60)

def draw_valid_moves(moves):
    """
    Highlight valid moves for the selected piece.
    
    Args:
        moves (list): List of valid move coordinates
    """
    for move in moves:
        x, y = move[1] * 100, move[0] * 100
        s = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(s, VALID_MOVE_COLOR, s.get_rect())
        gamedisplay.blit(s, (x, y))

def draw_selected_piece(x, y):
    """
    Highlight the currently selected piece.
    
    Args:
        x, y (int): Board coordinates of the selected piece
    """
    s = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.rect(s, HIGHLIGHT_COLOR, s.get_rect())
    gamedisplay.blit(s, (x * 100, y * 100))

def handle_ai_move():
    """
    Handle the AI's move selection and execution.
    This function encapsulates the AI move logic for better organization.
    """
    turn = turn + 1
    sc = copy.deepcopy(chessBoard.gameTiles)
    y, x, fx, fy = ai.evaluate(sc)
    m = fy
    n = fx
    
    # Handle special moves
    if chessBoard.gameTiles[y][x].pieceonTile.tostring() in ['K', 'R']:
        chessBoard.gameTiles[y][x].pieceonTile.moved = True

    # Castling
    if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'K':
        if m == x + 2:  # Kingside
            chessBoard.gameTiles[y][x+1].pieceonTile = chessBoard.gameTiles[y][x+3].pieceonTile
            s = updateposition(y, x+1)
            chessBoard.gameTiles[y][x+1].pieceonTile.position = s
            chessBoard.gameTiles[y][x+3].pieceonTile = nullpiece()
        elif m == x - 2:  # Queenside
            chessBoard.gameTiles[y][x-1].pieceonTile = chessBoard.gameTiles[y][0].pieceonTile
            s = updateposition(y, x-1)
            chessBoard.gameTiles[y][x-1].pieceonTile.position = s
            chessBoard.gameTiles[y][0].pieceonTile = nullpiece()

    # En passant
    if not len(enpassant) == 0:
        chessBoard.gameTiles[enpassant[0]][enpassant[1]].pieceonTile.enpassant = False
        enpassant = []
    
    # Pawn moves
    if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'P':
        if y + 1 == n and x + 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
            chessBoard.gameTiles[y][x+1].pieceonTile = nullpiece()
        if y + 1 == n and x - 1 == m and chessBoard.gameTiles[n][m].pieceonTile.tostring() == '-':
            chessBoard.gameTiles[y][x-1].pieceonTile = nullpiece()
        if n == y + 2:
            chessBoard.gameTiles[y][x].pieceonTile.enpassant = True
            enpassant = [n, m]
        if y + 1 == n and y == 6:
            promotion = True

    # Make the move
    if not promotion:
        chessBoard.gameTiles[n][m].pieceonTile = chessBoard.gameTiles[y][x].pieceonTile
        chessBoard.gameTiles[y][x].pieceonTile = nullpiece()
        s = updateposition(n, m)
        chessBoard.gameTiles[n][m].pieceonTile.position = s
        allTiles.clear()
        allpieces.clear()
        chessBoard.printboard()
        drawchesspieces()
        moves = []
    else:
        chessBoard.gameTiles[y][x].pieceonTile = nullpiece()
        chessBoard.gameTiles[n][m].pieceonTile = queen('Black', updateposition(n, m))
        allTiles.clear()
        allpieces.clear()
        chessBoard.printboard()
        drawchesspieces()
        moves = []
        promote = []
        promotion = False

def handle_human_move(event):
    """
    Handle the human player's move selection and execution.
    
    Args:
        event: Pygame event object
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        coord = pygame.mouse.get_pos()
        x = math.floor(coord[0]/100)
        y = math.floor(coord[1]/100)
        
        if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'White':
            moves = chessBoard.gameTiles[y][x].pieceonTile.legalmoveb(chessBoard.gameTiles)
            
            # Handle special moves
            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'k':
                ax = movex.castlingw(chessBoard.gameTiles)
                if ax:
                    for l in ax:
                        if l == 'ks':
                            moves.append([7, 6])
                        if l == 'qs':
                            moves.append([7, 2])
            
            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == 'p':
                ay = movex.enpassantb(chessBoard.gameTiles, y, x)
                if ay:
                    if ay[1] == 'r':
                        moves.append([y-1, x+1])
                    else:
                        moves.append([y-1, x-1])
            
            moves = movex.pinnedw(chessBoard.gameTiles, moves, y, x)
            
            if not turn % 2 == 0:
                moves = []
            
            if chessBoard.gameTiles[y][x].pieceonTile.alliance == 'Black':
                moves = []
            
            if chessBoard.gameTiles[y][x].pieceonTile.tostring() == '-':
                moves = []
            
            draw_selected_piece(x, y)
            draw_valid_moves(moves)