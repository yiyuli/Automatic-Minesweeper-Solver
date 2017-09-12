class Square(object):
    '''
    Square object represents a square in the board.
    It holds coordinates of row and column, and whether the square is no bomb, not flaged, not cleared, not bomed, not checked.
    '''

    FLAG = 'f'
    CLEAR = 'c'
    BLANK = ' '
    BOMB = 'b'
    WRONG = 'w'

    def __init__(self, row, col, board):
        '''
        Constructor for a square, originally marked as no bomb, not flaged, not cleared, not bomed, not checked.
        :param row: row of the square
        :param col: column of the square
        :param board: board the square is in
        '''
        self.row = row
        self.col = col
        self.board = board
        self.is_bomb = False
        self.flagged = False
        self.cleared = False
        self.bombed = False
        self.checked = False

    def display(self):
        '''
        Return the character representing the status of the square.
        The status includes square is clicked and bombed, square is cleared, square is flagged, and original square.
        :return: character representing the status of the square
        '''
        if self.bombed:
            return Square.BOMB
        elif self.cleared:
            if not self.nearby_bombs() == 0:
                return str(self.nearby_bombs())
            else:
                return Square.CLEAR
        elif self.flagged:
            return Square.FLAG
        else:
            return Square.BLANK

    def final_display(self):
        '''
        Return the character representing the status of the square after the game ended
        :return: character representing the status of the square
        '''
        if self.flagged and not self.is_bomb:
            return Square.WRONG
        elif not self.flagged and self.is_bomb:
            return Square.BOMB
        elif self.cleared:
            if not self.nearby_bombs() == 0:
                return str(self.nearby_bombs())
            else:
                return Square.CLEAR
        elif self.flagged and self.is_bomb:
            return Square.FLAG
        else:
            return Square.BLANK


    def nearby_bombs(self):
        '''
        Return how many bombs the neighbors of current square have in total.
        :return: number of bombs the neighbors of current square have in total
        '''
        nearby_bombs = 0
        nearby_squares = self.nearby_squares()
        for row, col in nearby_squares:
            if self.board.squares[row][col].is_bomb:
                nearby_bombs += 1
        return nearby_bombs

    def nearby_flags(self):
        '''
        Return how many flags the neighbors of current square have in total.
        :return: number of flags the neighbors of current square have in total
        '''
        nearby_flags = 0
        nearby_squares = self.nearby_squares()
        for row, col in nearby_squares:
            if self.board.squares[row][col].flagged:
                nearby_flags += 1
        return nearby_flags

    def nearby_cleared(self):
        '''
        Return how many cleared squares the neighbors of current square have in total.
        :return: number of cleared squares the neighbors of current square have in total
        '''
        nearby_cleared = 0
        nearby_squares = self.nearby_squares()
        for row, col in nearby_squares:
            if self.board.squares[row][col].flagged:
                nearby_cleared += 1
        return nearby_cleared

    def nearby_squares(self):
        '''
        Return all possible coordinates of neighbors of current square.
        :return: all possible coordinates of neighbors of current square
        '''
        nearby_squares = []
        if self.row == 0:
            self.deal_with_top_squares(nearby_squares)
        elif self.row == self.board.height - 1:
            self.deal_with_bottom_squares(nearby_squares)
        else:
            self.deal_with_middle_squares(nearby_squares)
        return nearby_squares



    def deal_with_middle_squares(self, nearby_squares):
        '''
        Return all possible coordinates of neighbors of current square which is in the middle.
        :param nearby_squares: list holding all coordinates
        :return: all possible coordinates of neighbors of current square which is in the middle.
        '''
        if self.col == 0:
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row - 1, self.col + 1))
            nearby_squares.append((self.row + 1, self.col + 1))
        elif self.col == self.board.width - 1:
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row - 1, self.col - 1))
            nearby_squares.append((self.row + 1, self.col - 1))
        else:
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row - 1, self.col - 1))
            nearby_squares.append((self.row - 1, self.col + 1))
            nearby_squares.append((self.row + 1, self.col - 1))
            nearby_squares.append((self.row + 1, self.col + 1))

    def deal_with_bottom_squares(self, nearby_squares):
        '''
        all possible coordinates of neighbors of current square which is in the bottom.
        :param nearby_squares: list holding all coordinates
        :return: all possible coordinates of neighbors of current square which is in the bottom
        '''
        if self.col == 0:
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row - 1, self.col + 1))
        elif self.col == self.board.width - 1:
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row - 1, self.col - 1))
        else:
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row - 1, self.col))
            nearby_squares.append((self.row - 1, self.col + 1))
            nearby_squares.append((self.row - 1, self.col - 1))

    def deal_with_top_squares(self, nearby_squares):
        '''
        Return: all possible coordinates of neighbors of current square which is in the top.
        :param nearby_squares: list holding all coordinates
        :return: all possible coordinates of neighbors of current square which is in the top
        '''
        if self.col == 0:
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row + 1, self.col + 1))
        elif self.col == self.board.width - 1:
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row + 1, self.col - 1))
        else:
            nearby_squares.append((self.row, self.col + 1))
            nearby_squares.append((self.row, self.col - 1))
            nearby_squares.append((self.row + 1, self.col))
            nearby_squares.append((self.row + 1, self.col + 1))
            nearby_squares.append((self.row + 1, self.col - 1))

    def flag(self):
        '''
        Flag a square if it is not flagged, Unflag it if it is flagged.
        '''
        res = 0
        if not self.cleared:
            if self.flagged:
                res = 1
            else:
                res = -1
            self.flagged = not self.flagged
        return res

    def bomb(self):
        '''
        Mark current square to be bombed, which means clicked and there is a bomb.
        '''
        self.bombed = True
