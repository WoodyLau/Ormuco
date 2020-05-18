import unittest
from OverlappingLines import isOverlap

class testIsOverlap(unittest.TestCase):
    def test_not_overlapping1(self):
        self.assertFalse(isOverlap(1,3,4,5))
    def test_not_overlapping2(self):
        self.assertFalse(isOverlap(1,3,3,5))
    def test_not_overlapping3(self):
        self.assertFalse(isOverlap(3,1,5,4))
    def test_not_overlapping4(self):
        self.assertFalse(isOverlap(5,4,1,3))
    def test_overlapping_slightly1(self):
        self.assertTrue(isOverlap(1,4,3,5))
    def test_overlapping_slightly2(self):
        self.assertTrue(isOverlap(1,3.5,3,5))
    def test_overlapping_slightly3(self):
        self.assertTrue(isOverlap(4,1,5,3))
    def test_overlapping_slightly4(self):
        self.assertTrue(isOverlap(5,3,1,4))
    def test_overlapping_completely1(self):
        self.assertTrue(isOverlap(1,5,3,4))
    def test_overlapping_completely2(self):
        self.assertTrue(isOverlap(1,5,3,5))
    def test_overlapping_completely3(self):
        self.assertTrue(isOverlap(5,1,4,3))
    def test_overlapping_completely4(self):
        self.assertTrue(isOverlap(5,1,3,4))
    def test_negative_not_overlapping(self):
        self.assertFalse(isOverlap(-1,-3,-4,-5))
    def test_negative_overlapping_slightly1(self):
        self.assertTrue(isOverlap(-1,-4,-3,-5))
    def test_negative_overlapping_completely1(self):
        self.assertTrue(isOverlap(-1,-5,-3,-4))
     
        
if __name__ == '__main__':
    unittest.main()