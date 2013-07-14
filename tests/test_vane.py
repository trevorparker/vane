import vane
import unittest

class TestFetch(unittest.TestCase):
    def setUp(self):
        pass

    def test_good_fetch(self):
        self.loc = 'New York, NY'
        self.w = vane.fetch_weather(self.loc)
        self.assertTrue('temperature' in self.w['current'])
        self.assertTrue('summary' in self.w['current'])

    def test_bad_fetch(self):
        with self.assertRaises(Exception):
            self.loc = 'Somewhere, On, Mars'
            self.w = vane.fetch_weather(self.loc)

if __name__ == '__main__':
    unittest.main()
