#!/usr/bin/env python3
"""
Test runner for Tic-Tac-Chess project
Run with: python3 run_tests.py [options]
"""
import unittest
import sys

if __name__ == "__main__":
    # Discover and run all tests
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="*_test.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with proper code
    sys.exit(0 if result.wasSuccessful() else 1)
