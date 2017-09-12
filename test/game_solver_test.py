import unittest
from board import Board
from game_solver import *


class gameSolverTest(unittest.TestCase):
    '''
        Tests for game solver
    '''

    def setUp(self):
        '''
        Set up test environment
        '''
        self.board = Board([12, 12, 2])

    def test_game_solver(self):
        '''
        Test game solver solves the game
        '''
        self.assertTrue(solve_game(self.board, auto=False))

    def test_combine(self):
        '''
        Test combining two sets work properly
        '''
        comb_1 = [(1,4), (2, 3)]
        comb_2 = [(2,3), (3, 4)]
        new_comb = combine(comb_1, comb_2)
        self.assertEquals(new_comb, [(1, 4), (2, 3), (3, 4)])

    def test_intersection(self):
        '''
        Test intersecting two sets work properly
        :return:
        '''
        blank_squares_1 = [(1, 3), (2, 4), (5, 6)]
        blank_squares_2 = [(2, 5), (1, 3), (2, 4)]
        intersection = get_intersection(blank_squares_1, blank_squares_2)
        self.assertEquals(intersection, [(1, 3), (2, 4)])

    def test_cartesian_product(self):
        '''
        Test doing Cartesian product to two sets and discarding contradicted results work properly
        '''
        possible_combinations_1 = [[(1, 0), (2, 0)], [(1, 0), (3, 0)], [(1, 0), (4, 0)], [(2, 0), (3, 0)], [(2, 0), (4, 0)], [(3, 0), (4, 0)]]
        possible_combinations_2 = [[(3, 0)], [(4, 0)], [(5, 0)]]
        product = cartesian_product_no_contradiction(possible_combinations_1, possible_combinations_2, [(3, 0), (4, 0)])
        self.assertEquals(product, [[(1, 0), (2, 0), (5, 0)], [(1, 0), (3, 0)], [(1, 0), (4, 0)], [(2, 0), (3, 0)], [(2, 0), (4, 0)]])

    def test_find_safer_operation_from_new_combination(self):
        '''
        Test find_safer_operation_from_new_combination returns minimum probability and safest square
        '''
        combined_set = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
        new_combinations = [[(1, 0), (2, 0), (5, 0)], [(1, 0), (3, 0)], [(1, 0), (4, 0)], [(2, 0), (3, 0)], [(2, 0), (4, 0)]]
        probability, safest_square = find_safer_operation_from_new_combination(combined_set, new_combinations)
        self.assertEquals(probability, 1 / 5)
        self.assertEquals(safest_square, (5, 0))
