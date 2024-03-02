#test_calculator

import unittest
from calculator import Double, Even

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.double_instance = Double()
        self.even_instance = Even()

    def test_twox(self):
        self.assertEqual(self.double_instance.twox(2), 4)
        self.assertEqual(self.double_instance.twox(3), 6)

    def test_isEven(self):
        self.assertTrue(self.even_instance.isEven(2))
        self.assertFalse(self.even_instance.isEven(3))

if __name__ == '__main__':
    unittest.main()
