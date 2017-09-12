class Rank(object):
    '''
    Rank object storing top three records
    '''
    def __init__(self):
        '''
        Constructor for Rank object
        '''
        self.first = 'No record'
        self.second = 'No record'
        self.third = 'No record'

    def update(self, time):
        '''
        Update rank by new finishing time
        :param time: new finishing time
        '''
        time = int(time.split(' ')[1])
        if self.first == 'No record' or time < self.first:
            self.third = self. second
            self.second = self.first
            self.first = time
        elif self.second == 'No record' or time < self.second:
            self.third = self.second
            self.second = time
        elif self.third == 'No record' or time < self.third:
            self.third = time