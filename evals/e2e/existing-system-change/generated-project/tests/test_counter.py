import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from counter_service.counter import increment, reset, decrement

class CounterTests(unittest.TestCase):
    def test_increment_baseline(self):
        self.assertEqual(6, increment(5))

    def test_reset_baseline(self):
        self.assertEqual(0, reset())

    def test_decrement_change(self):
        self.assertEqual(4, decrement(5))

if __name__ == "__main__":
    unittest.main()
