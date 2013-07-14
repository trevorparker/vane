import vane
import unittest

class TestFetch(unittest.TestCase):
    def test_owm_good_fetch(self):
        loc = 'New York, NY'
        w = vane.fetch_weather(loc)
        self.assertTrue('temperature' in w['current'])
        self.assertTrue('summary' in w['current'])

    def test_owm_bad_fetch(self):
        with self.assertRaises(Exception):
            loc = 'Somewhere, On, Mars'
            w = vane.fetch_weather(loc)

    def test_wund_good_fetch(self):
        api_key = os.environ['WUND_API']
        loc = 'New York, NY'
        w = vane.fetch_weather(location=loc, provider='wund', api_key=api_key)
        self.assertTrue('temperature' in w['current'])
        self.assertTrue('summary' in w['current'])

    def test_wund_bad_fetch(self):
        api_key = os.environ['WUND_API']
        with self.assertRaises(Exception):
            loc = '0'
            w = vane.fetch_weather(
                location=loc, provider='wund', api_key=api_key)

if __name__ == '__main__':
    unittest.main()
