import unittest
from proxy import main

class TestProxy(unittest.TestCase):

    def test_main_function(self):
        # Test if the main function runs without errors
        try:
            main(testing=True)
        except Exception as e:
            self.fail(f"Main function raised an exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()





