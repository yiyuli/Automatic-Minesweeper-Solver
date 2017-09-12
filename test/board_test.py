import unittest
from board import Board

class BoardTest(unittest.TestCase):
    '''
    Tests for Board object
    '''
    def setUp(self):
        '''
        Set up test environment
        '''
        self.board = Board([10,10,2])

    def test_detect_game_state_goon(self):
        '''
        Test whether the game will return go on state properly
        '''
        game_state = self.board.detect_game_state()
        self.assertEquals(game_state, Board.GOON)

    def test_detect_game_state_lose(self):
        '''
            Test whether the game will return lose state properly
        '''
        self.board.squares[2][2].bomb()
        game_state = self.board.detect_game_state()
        self.assertEquals(game_state, Board.LOSE)

    def test_detect_game_state_win(self):
        '''
            Test whether the game will return win state properly
        '''
        for row in range(self.board.height):
            for col in range(self.board.width):
                if not self.board.squares[row][col].is_bomb:
                    self.board.squares[row][col].cleared = True
        game_state = self.board.detect_game_state()
        self.assertEquals(game_state, Board.WIN)

    def test_update_flag_command(self):
        '''
            Test if the board is updated correctly if receiving a flag command
        '''
        self.board.update('f', 3, 3)
        self.assertTrue(self.board.squares[3][3].flagged)
        self.board.update('f', 3, 3)
        self.assertFalse(self.board.squares[3][3].flagged)

    def test_update_click_command(self):
        '''
            Test if the board is updated correctly if receiving a click command
        '''
        for row in range(self.board.height):
            for col in range(self.board.width):
                self.board.squares[row][col].is_bomb = False
        self.board.squares[0][0].is_bomb = True
        self.board.squares[4][3].is_bomb = True
        self.board.update('c', 5, 5)
        for row in range(self.board.height):
            for col in range(self.board.width):
                if (row == 0 and col == 0) or (row == 4 and col == 3):
                    self.assertFalse(self.board.squares[row][col].cleared)
                else:
                    self.assertTrue(self.board.squares[row][col].cleared)