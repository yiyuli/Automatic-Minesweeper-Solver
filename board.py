import random
from square import Square

class Board(object):
    '''
    Board object represents board for game.
    It holds width * height squares, and is responsible to update itself by commands and detect game state.
    '''
    WIN = 2
    LOSE = 1
    GOON = 0

    CLICK = 'c'
    FLAG = 'f'
    DOUBLE = 'd'

    def __init__(self, size):
        '''
        Constructor for Board object, initialize height * width 2D lists. Then randomly assign mines.
        '''
        self.width = size[0]
        self.height = size[1]
        self.bombs = size[2]
        self.remainings = self.bombs
        self.started = False
        self.squares = [[object() for row in range(self.width)] for col in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                self.squares[row][col] = Square(row, col, self)
        k = 0
        while k < self.bombs:
            new_bomb_row = random.randrange(0, self.height)
            new_bomb_col = random.randrange(0, self.width)
            if not self.squares[new_bomb_row][new_bomb_col].is_bomb:
                self.squares[new_bomb_row][new_bomb_col].is_bomb = True
                k += 1

    def update(self, op, row, col):
        '''
        Update board by commands.
        :param op: operation of the command. Either 'f' or 'c' or 'd'
        :param row: row of the square that is operated on
        :param col: column of the square that is operated on
        '''
        if op == Board.FLAG:
            self.remainings += self.squares[row][col].flag()
        elif op == Board.DOUBLE:
            nearby_bombs = self.squares[row][col].nearby_bombs()
            nearby_flags = self.squares[row][col].nearby_flags()
            if self.squares[row][col].cleared and not nearby_bombs == 0 and nearby_bombs == nearby_flags:
                self.check_nearby_squares(self.squares[row][col].nearby_squares())
        elif op == Board.CLICK:
            if not self.started and self.squares[row][col].is_bomb:
                self.relocate_bomb(row, col)
            self.started = True
            if not self.squares[row][col].is_bomb:
                self.spread_cleared_check(row, col)
            else:
                self.squares[row][col].bombed = True

    def relocate_bomb(self, row, col):
        '''
        Relocate bomb in position (row, col)
        :param row: row
        :param col: column
        '''
        find_non_bomb_square = False
        while not find_non_bomb_square:
            new_bomb_row = random.randrange(0, self.height)
            new_bomb_col = random.randrange(0, self.width)
            if not self.squares[new_bomb_row][new_bomb_col].is_bomb:
                self.squares[new_bomb_row][new_bomb_col].is_bomb = True
                find_non_bomb_square = True
        self.squares[row][col].is_bomb = False

    def spread_cleared_check(self, row, col):
        '''
        Recursively check squares is cleared.
        If all of neighbor of current square are not bomb, mark it as cleared and recursively check all neighbors.
        If not, just mark it as cleared.
        :param row: row of current square
        :param col: column of current square
        '''
        self.squares[row][col].cleared = True
        if self.squares[row][col].nearby_bombs() == 0:
            self.squares[row][col].checked = True
            nearby_squares = self.squares[row][col].nearby_squares()
            for r, c in nearby_squares:
                if not self.squares[r][c].checked:
                    self.spread_cleared_check(r, c)

    def check_nearby_squares(self, nearby_squares):
        '''
        check nearby squares if nearby square is not flagged
        :param nearby_squares: nearby_squares
        '''
        for r, c in nearby_squares:
            if not self.squares[r][c].flagged:
                self.update(Board.CLICK, r, c)

    def print(self):
        '''
        Print the board.
        '''
        print (' ', end=" ")
        for col in range(self.width):
            print (col, end=" ")
        print("")

        for row in range(self.height):
            print (row, end=" ")
            for col in range(self.width):
                print(self.squares[row][col].display(), end=" ")
            print("")

    def detect_game_state(self):
        '''
        Detect current game_state. If there is a square that is bombed, the game ended as lose.
        If there are non-bomb square that can be clicked on, the game ended as win.
        Otherwise, the game continues.
        '''
        game_state = Board.WIN
        for row in range(self.height):
            for col in range(self.width):
                if self.squares[row][col].bombed:
                    return Board.LOSE
                if not self.squares[row][col].is_bomb and not self.squares[row][col].cleared:
                    game_state = Board.GOON
        return game_state

    def test_mode(self):
        '''
        Set the board to test mode, which is designed to be a fixed configuration
        '''
        for row in range(self.height):
            for col in range(self.width):
                self.squares[row][col].is_bomb = False
        self.squares[0][1].is_bomb = True
        self.squares[0][2].is_bomb = True
        self.squares[1][2].is_bomb = True
        self.squares[2][1].is_bomb = True
        self.squares[2][0].is_bomb = True

