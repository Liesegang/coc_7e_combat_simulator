import unittest
from coc7e_combat_simulator.dice_parser import DiceParser
from unittest.mock import patch
import random

class TestDiceParser(unittest.TestCase):
    def setUp(self):
        self.parser = DiceParser()

    def test_simple_arithmetic(self):
        tests = [
            ("3+2", 5),
            ("10-2", 8),
            ("5*3", 15),
            ("20/4", 5),
            ("7%2", 1),
            ("2^3", 8),
            ("2^(1+2)", 8),
            ("(2^2)^2", 16),
            ("(2+3)*4", 20),
            ("2+3*4", 14),
            ("(2+3)*4-5/5", 19),
        ]
        for expr, expected in tests:
            with self.subTest(expr=expr):
                result, rolls = self.parser.parse(expr)
                self.assertEqual(result, expected)
                self.assertEqual(len(rolls), 0)

                result = self.parser.expected(expr)
                self.assertEqual(result, expected)

                result = self.parser.maximum(expr)
                self.assertEqual(result, expected)

                result = self.parser.minimum(expr)
                self.assertEqual(result, expected)

    def test_dice_rolls(self):
        expr = "1000d6"
        _, rolls = self.parser.parse(expr)
        self.assertTrue(all(1 <= roll <= 6 for roll in rolls[0].details))

    def test_parameter_substitution(self):
        expr = "2*{multiplier}"
        parameters = {"multiplier": 5}
        result, _ = self.parser.parse(expr, parameters)
        self.assertEqual(result, 10)

    def test_invalid_expression(self):
        with self.assertRaises(Exception):
            try:
                self.parser.parse("2*/5")
            except Exception as e:
                pass
                return
            self.fail("Expected exception not raised")

    def test_negative_numbers(self):
        self.assertEqual(self.parser.parse("3+-5")[0], -2)
        self.assertEqual(self.parser.parse("-3+5")[0], 2)

    @patch('random.randint')
    def test_dice_roll_fixed_value(self, mock_randint):
        mock_randint.side_effect=[3, 4]
        result, rolls = self.parser.parse("2d6")

        self.assertEqual(result, 7)
        self.assertEqual(rolls[0].roll, 7)
        self.assertEqual(rolls[0].details, [3, 4])

    @patch('random.randint')
    def test_dice_lowercase(self, mock_randint):
        mock_randint.return_value=3
        parser = DiceParser()
        result, rolls = parser.parse("1d6")
        self.assertEqual(result, 3)
        self.assertEqual(rolls[0].roll, 3)
        self.assertEqual(rolls[0].details[0], 3)

    @patch('random.randint')
    def test_multiple_dice_rolls(self, mock_randint):
        mock_randint.side_effect=[2, 1, 5, 3, 6]
        result, rolls = self.parser.parse("2d4+3d6")

        self.assertEqual(result, sum([2, 1, 5, 3, 6]))
        self.assertEqual(rolls[0].details, [2, 1])
        self.assertEqual(rolls[1].details, [5, 3, 6])

    @patch('random.randint')
    def test_complex_expression(self, mock_randint):
        mock_randint.side_effect = [4, 3, 5]

        parser = DiceParser()
        expression = "(3D6+2)*5-10/{HP}"
        parameters = {'HP': 2}

        result, rolls = parser.parse(expression, parameters)

        self.assertTrue(result is not None)
        self.assertTrue(len(rolls) > 0)

        expected_rolls_result = sum([4, 3, 5])
        expected_total = ((expected_rolls_result + 2) * 5) - (10 / parameters['HP'])
        self.assertEqual(result, expected_total)

        self.assertEqual(rolls[0].details, [4, 3, 5])

    def test_expected_maximum_minimum_values(self):
        expr = "3d6"
        expected = self.parser.expected(expr)
        maximum = self.parser.maximum(expr)
        minimum = self.parser.minimum(expr)
        self.assertAlmostEqual(expected, (1 + 6) / 2 * 3)
        self.assertEqual(minimum, 3)
        self.assertEqual(maximum, 18)

    def test_expected_value(self):
        tests = [
            ("1d6", 3.5),
            ("2d6", 7.0),
            ("1d20", 10.5),
            ("3d4+2", 9.5),
            ("4d6-1", 13.0),
            ("2d10+3d3", 17.0),
        ]
        for expr, expected_value in tests:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(self.parser.expected(expr), expected_value, places=2)

    def test_minimum_value(self):
        tests = [
            ("1d6", 1),
            ("2d6", 2),
            ("1d20", 1),
            ("3d4+2", 5),
            ("4d6-1", 3),
            ("2d10+3d3", 5),
        ]
        for expr, min_value in tests:
            with self.subTest(expr=expr):
                self.assertEqual(self.parser.minimum(expr), min_value)

    def test_maximum_value(self):
        tests = [
            ("1d6", 6),
            ("2d6", 12),
            ("1d20", 20),
            ("3d4+2", 14),
            ("4d6-1", 23),
            ("2d10+3d3", 29),
        ]
        for expr, max_value in tests:
            with self.subTest(expr=expr):
                self.assertEqual(self.parser.maximum(expr), max_value)

if __name__ == '__main__':
    unittest.main()