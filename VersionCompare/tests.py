import unittest

from VersionCompare import versionComparer

class TestVersionComparator(unittest.TestCase):
    def test_equal_version_same_length(self):
        self.assertEqual(versionComparer('1.2.1', '1.2.1'), 0)

    def test_equal_version_same_length_all_zero(self):
        self.assertEqual(versionComparer('0.0.0', '0.0.0'), 0)

    def test_equal_version_special_versions_length_all_zero(self):
        self.assertEqual(versionComparer('0.0.0a', '0.0.0a'), 0)

    def test_greater_version_same_length(self):
        self.assertGreater(versionComparer('1.2.3', '1.2.1'), 0)

    def test_greater_version_bigger_versions(self):
        self.assertGreater(versionComparer('1.2.1.0.2', '1.2.1.0.1'), 0)
        
    def test_greater_version_different_length(self):
        self.assertGreater(versionComparer('1.2.13', '1.2.1.0.1'), 0)

    def test_less_version_same_length(self):
        self.assertLess(versionComparer('5.5.1', '5.5.3'), 0)

    def test_less_version_bigger_versions(self):
        self.assertLess(versionComparer('1.1.1.0.1', '1.2.1.0.1'), 0)
        
    def test_less_version_different_length(self):
        self.assertLess(versionComparer('1.2.1', '1.2.12.0.1'), 0)

    def test_less_version_special_versions_mixed(self):
        self.assertLess(versionComparer('1  .0.0.0. 0', ' 5',), 0)

    def test_less_version_mixed_length(self):
        self.assertLess(versionComparer('5.5.1.0.b', '5.5.3'), 0)


if __name__ == '__main__':
    unittest.main()