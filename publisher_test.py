import unittest
from mqpublisher import generate_random_lat_lon, main

class TestPublisher(unittest.TestCase):

    def test_generate_random_lat_lon(self):
        # Test if latitude and longitude values are within valid ranges n times
        for _ in range(100):
            latlong = generate_random_lat_lon()
            self.assertTrue(-90 <= latlong['lat'] <= 90)
            self.assertTrue(-180 <= latlong['long'] <= 180)

    def test_main_function(self):
        # Test if the main function runs without errors
        try:
            main(testing=True)
        except Exception as e:
            self.fail(f"Main function raised an exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()