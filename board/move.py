from pieces.nullpiece import nullpiece
from pieces.pawn import pawn
from pieces.rook import rook
from pieces.king import king


class move:
    """Represents a chess move from one position to another"""

    def __init__(self, start, end, board):
        """
        Initialize a move
        Args:
            start (int): Starting position index
            end (int): Ending position index
            board: The chess board
        """
        self.start = start  # Store starting position
        self.end = end  # Store ending position
        self.board = board  # Store reference to board
        self.pieceMoved = board.gameTiles[start//8][start%8].getpiece()  # Get piece being moved
        self.pieceCaptured = board.gameTiles[end//8][end%8].getpiece()  # Get piece being captured (if any)
        self.moveID = start * 100 + end  # Create unique move ID

    def __eq__(self, other):
        """
        Compare two moves for equality
        Args:
            other: Another move to compare with
        Returns:
            bool: True if moves are equal, False otherwise
        """
        if isinstance(other, move):  # Check if other is a move
            return self.moveID == other.moveID  # Compare move IDs
        return False  # Return False if other is not a move

    def getChessNotation(self):
        """
        Get chess notation for this move (e.g., "e2 to e4")
        Returns:
            str: Chess notation string
        """
        # Convert position indices to chess notation
        return self.getRankFile(self.start) + " to " + self.getRankFile(self.end)

    def getRankFile(self, pos):
        """
        Convert position index to chess notation
        Args:
            pos (int): Position index
        Returns:
            str: Chess notation (e.g., "e4")
        """
        # Convert position to rank and file
        rank = str(8 - (pos//8))  # Calculate rank (1-8)
        file = chr(97 + (pos%8))  # Calculate file (a-h)
        return file + rank  # Return chess notation

    def execute(self):
        """
        Execute this move on the board
        Returns:
            board: Updated board state
        """
        # Create new board state
        newBoard = board()
        newBoard.gameTiles = self.board.gameTiles.copy()
        
        # Move piece to new position
        newBoard.gameTiles[self.end//8][self.end%8] = Tile(self.end, self.pieceMoved)
        newBoard.gameTiles[self.start//8][self.start%8] = Tile(self.start, nullpiece())
        
        return newBoard  # Return updated board

    def isvalid(self):
        """
        Check if this move is valid
        Returns:
            bool: True if move is valid, False otherwise
        """
        # Check if move is within board bounds
        if self.end < 0 or self.end > 63:
            return False
            
        # Check if piece is being moved
        if self.pieceMoved is None:
            return False
            
        # Check if destination has piece of same color
        if self.pieceCaptured is not None and self.pieceCaptured.color == self.pieceMoved.color:
            return False
            
        # Check if move is legal for piece type
        if not self.pieceMoved.validMove(self.end, self.board):
            return False
            
        return True  # Move is valid

    def isCheck(self):
        """
        Check if this move puts opponent in check
        Returns:
            bool: True if move puts opponent in check, False otherwise
        """
        # Execute move on temporary board
        tempBoard = self.execute()
        
        # Find opponent's king
        kingPos = -1
        for i in range(64):
            piece = tempBoard.gameTiles[i//8][i%8].getpiece()
            if isinstance(piece, king) and piece.color != self.pieceMoved.color:
                kingPos = i
                break
                
        # Check if king is in check
        if kingPos != -1:
            return self.pieceMoved.validMove(kingPos, tempBoard)
            
        return False  # King not found or not in check

    def isCheckmate(self):
        """
        Check if this move results in checkmate
        Returns:
            bool: True if move results in checkmate, False otherwise
        """
        # Execute move on temporary board
        tempBoard = self.execute()
        
        # Find opponent's king
        kingPos = -1
        for i in range(64):
            piece = tempBoard.gameTiles[i//8][i%8].getpiece()
            if isinstance(piece, king) and piece.color != self.pieceMoved.color:
                kingPos = i
                break
                
        # Check if king is in checkmate
        if kingPos != -1:
            # Check if king has any legal moves
            king = tempBoard.gameTiles[kingPos//8][kingPos%8].getpiece()
            return king.isCheckmate(tempBoard)
            
        return False  # King not found or not in checkmate

    def checkb(self,gametiles):
        x=0
        y=0
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()=='K'):
                    x=m
                    y=k
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.alliance=='White'):
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    for move in moves:
                        if(move[0]==x and move[1]==y):
                            return["checked",[m,k]]
        return["notchecked"]

    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def movesifcheckedb(self,gametiles):
        movi=[]
        piece=None
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.alliance=='Black'):
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    for move in moves:
                        x=move[0]
                        y=move[1]
                        piece=gametiles[x][y].pieceonTile
                        gametiles[x][y].pieceonTile=gametiles[m][k].pieceonTile
                        gametiles[m][k].pieceonTile=nullpiece()
                        s=self.updateposition(x,y)
                        gametiles[x][y].pieceonTile.position=s
                        if(self.checkb(gametiles)[0]=='notchecked'):
                            movi.append([m,k,x,y])
                            gametiles[m][k].pieceonTile=gametiles[x][y].pieceonTile
                            gametiles[x][y].pieceonTile=piece
                            s=self.updateposition(m,k)
                            gametiles[m][k].pieceonTile.position=s
                        else:
                            gametiles[m][k].pieceonTile=gametiles[x][y].pieceonTile
                            gametiles[x][y].pieceonTile=piece
                            s=self.updateposition(m,k)
                            gametiles[m][k].pieceonTile.position=s


        return movi

    def checkw(self,gametiles):
        x=0
        y=0
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()=='k'):
                    x=m
                    y=k
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.alliance=='Black'):
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    if moves==None:
                        print(m)
                        print(k)
                    for move in moves:
                        if(move[0]==x and move[1]==y):
                            return["checked",[m,k]]
        return["notchecked"]

    def movesifcheckedw(self,gametiles):
        movi=[]
        piece=None
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.alliance=='White'):
                    moves=gametiles[m][k].pieceonTile.legalmoveb(gametiles)
                    for move in moves:
                        x=move[0]
                        y=move[1]
                        piece=gametiles[x][y].pieceonTile
                        gametiles[x][y].pieceonTile=gametiles[m][k].pieceonTile
                        gametiles[m][k].pieceonTile=nullpiece()
                        s=self.updateposition(x,y)
                        gametiles[x][y].pieceonTile.position=s
                        if(self.checkw(gametiles)[0]=='notchecked'):
                            movi.append([m,k,x,y])
                            gametiles[m][k].pieceonTile=gametiles[x][y].pieceonTile
                            gametiles[x][y].pieceonTile=piece
                            s=self.updateposition(m,k)
                            gametiles[m][k].pieceonTile.position=s
                        else:
                            gametiles[m][k].pieceonTile=gametiles[x][y].pieceonTile
                            gametiles[x][y].pieceonTile=piece
                            s=self.updateposition(m,k)
                            gametiles[m][k].pieceonTile.position=s


        return movi

    def castlingb(self,gametiles):
        array=[]
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()=='K'):
                    if(gametiles[m][k].pieceonTile.moved==False):
                        if(gametiles[m][k+3].pieceonTile.tostring()=='R'):
                            if(gametiles[m][k+3].pieceonTile.moved==False):
                                if(gametiles[m][k+1].pieceonTile.tostring()=='-'):
                                    if(gametiles[m][k+2].pieceonTile.tostring()=='-'):
                                        array.append('ks')
                        if(gametiles[m][0].pieceonTile.tostring()=='R'):
                            if(gametiles[m][0].pieceonTile.moved==False):
                                if(gametiles[m][3].pieceonTile.tostring()=='-'):
                                    if(gametiles[m][2].pieceonTile.tostring()=='-'):
                                        if(gametiles[m][1].pieceonTile.tostring()=='-'):
                                            array.append('qs')
                    return array
    def castlingw(self,gametiles):
        array=[]
        for m in range(8):
            for k in range(8):
                if(gametiles[m][k].pieceonTile.tostring()=='k'):
                    if(gametiles[m][k].pieceonTile.moved==False):
                        if(gametiles[m][k+3].pieceonTile.tostring()=='r'):
                            if(gametiles[m][k+3].pieceonTile.moved==False):
                                if(gametiles[m][k+1].pieceonTile.tostring()=='-'):
                                    if(gametiles[m][k+2].pieceonTile.tostring()=='-'):
                                        array.append('ks')
                        if(gametiles[m][0].pieceonTile.tostring()=='r'):
                            if(gametiles[m][0].pieceonTile.moved==False):
                                if(gametiles[m][3].pieceonTile.tostring()=='-'):
                                    if(gametiles[m][2].pieceonTile.tostring()=='-'):
                                        if(gametiles[m][1].pieceonTile.tostring()=='-'):
                                            array.append('qs')
                    return array



    def enpassantb(self,gametiles,y,x):

        if(gametiles[y][x].pieceonTile.tostring()=='P' and y==4):
            if(x+1<8 and gametiles[y][x+1].pieceonTile.tostring()=='p' and gametiles[y][x+1].pieceonTile.enpassant==True):
                return[[y,x],'r']
            if(x-1>=0 and gametiles[y][x-1].pieceonTile.tostring()=='p' and gametiles[y][x-1].pieceonTile.enpassant==True):
                return[[y,x],'l']

        if(gametiles[y][x].pieceonTile.tostring()=='p' and y==3):
            if(x+1<8 and gametiles[y][x+1].pieceonTile.tostring()=='P' and gametiles[y][x+1].pieceonTile.enpassant==True):
                return[[y,x],'r']
            if(x-1>=0 and gametiles[y][x-1].pieceonTile.tostring()=='P' and gametiles[y][x-1].pieceonTile.enpassant==True):
                return[[y,x],'l']

        return []


    def pinnedb(self,gametiles,moves,y,x):
        movi=[]
        piece1=None
        for move in moves:
            m=move[0]
            k=move[1]
            piece1=gametiles[m][k].pieceonTile
            gametiles[m][k].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            if(self.checkb(gametiles)[0]=='notchecked'):
                movi.append(move)
            gametiles[y][x].pieceonTile=gametiles[m][k].pieceonTile
            gametiles[m][k].pieceonTile=piece1

        return movi

    def pinnedw(self,gametiles,moves,y,x):
        movi=[]
        piece1=None
        for move in moves:
            m=move[0]
            k=move[1]
            piece1=gametiles[m][k].pieceonTile
            gametiles[m][k].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            if(self.checkw(gametiles)[0]=='notchecked'):
                movi.append(move)
            gametiles[y][x].pieceonTile=gametiles[m][k].pieceonTile
            gametiles[m][k].pieceonTile=piece1

        return movi























































