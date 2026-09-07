import ast
import unittest
from pathlib import Path

class StaticAppTests(unittest.TestCase):
    def test_app_parses(self):
        ast.parse((Path(__file__).resolve().parents[1]/"src"/"app.py").read_text())

    def test_bind_address(self):
        text=(Path(__file__).resolve().parents[1]/"src"/"app.py").read_text()
        self.assertIn('HOST = "0.0.0.0"', text)
        self.assertIn('"/health"', text)

if __name__=="__main__":
    unittest.main()
