import unittest
from rank import Rank

class RankTest(unittest.TestCase):
    '''
    Test for rank object
    '''
    def test_update(self):
        '''
        Test whether the rank will update properly
        '''
        rank = Rank()
        rank.update('time: 50')
        rank.update('time: 30')
        self.assertEquals(rank.first, 30)
        self.assertEquals(rank.second, 50)
        self.assertEquals(rank.third, 'No record')