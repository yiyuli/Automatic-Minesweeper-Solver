import unittest
from board import Board

class SquareTest(unittest.TestCase):
    '''
    Tests for Square object
    '''
    def setUp(self):
        '''
            Set up test environment
        '''
        self.board = Board([10,10,2])

    def test_display(self):
        '''
        Test whether display will return proper character representing its status
        '''
        square = self.square = self.board.squares[3][3]
        self.assertEquals(square.display(), ' ')
        self.square.flag()
        self.assertEquals(square.display(), 'f')
        self.square.bomb()
        self.assertEquals(square.display(), 'b')

    def test_nearby_squares(self):
        '''
        Test whether nearby_squares will return neighbors of current square correctly
        '''
        nearby_squares = self.board.squares[3][3].nearby_squares()
        self.assertEquals(nearby_squares, [(3, 4), (3, 2), (2, 3), (4, 3), (2, 2), (2, 4), (4, 2), (4, 4)])
        nearby_squares = self.board.squares[0][0].nearby_squares()
        self.assertEquals(nearby_squares, [(1, 0), (0, 1), (1, 1)])
        nearby_squares = self.board.squares[2][0].nearby_squares()
        self.assertEquals(nearby_squares, [(1, 0), (3, 0), (2, 1), (1, 1), (3, 1)])