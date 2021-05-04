import os
import queue
import unittest
from request.requester import Requester 
from request.util.util import Util

class RequestTest(unittest.TestCase):
    """ contains unit tests """

    def __init__(self, *args, **kwargs):
        super(RequestTest, self).__init__(*args, **kwargs)
        
        self.requester = Requester('*', '*')
        self.word = 'debilitate'

        self.response = self.requester.get_translation(self.word, 'en', 'de')

        print(self.response)
   
    def test_word(self):
        self.assertNotEqual(self.response, None)

    

if __name__ == '__main__':
    unittest.main()
