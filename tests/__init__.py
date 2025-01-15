# tests/__init__.py
import unittest

def run_all_tests():
    """
    Discover and run all tests in the "tests" folder.
    """
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == "__main__":
    run_all_tests()
