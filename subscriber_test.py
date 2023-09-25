import unittest
from mqsubscriber import convert_to_radians

class TestSubscriber(unittest.TestCase):

    def test_convert_to_radians(self):
        # Test if conversion to radians works correctly for various input values
        test_cases = [
            {'lat': 45.0, 'long': -90.0, 'expected': {'lat_rad': 0.7854, 'long_rad': -1.5708}},
            {'lat': 0.0, 'long': 0.0, 'expected': {'lat_rad': 0.0, 'long_rad': 0.0}},
            {'lat': -90.0, 'long': 180.0, 'expected': {'lat_rad': -1.5708, 'long_rad': 3.1416}},
        ]

        for case in test_cases:
            converted_data = convert_to_radians(case)
            self.assertAlmostEqual(converted_data['lat_rad'], case['expected']['lat_rad'], delta=0.0001)
            self.assertAlmostEqual(converted_data['long_rad'], case['expected']['long_rad'], delta=0.0001)
            

if __name__ == '__main__':
    unittest.main()