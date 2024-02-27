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
            ("(2+3)*4", 20),
            ("2+3*4", 14),
            ("(2+3)*4-5/5", 19),
        ]
        for expr, expected in tests:
            with self.subTest(expr=expr):
                result, _ = self.parser.parse(expr)
                self.assertEqual(result, expected)

    def test_dice_rolls(self):
        expr = "1d6"
        _, rolls = self.parser.parse(expr)
        self.assertTrue(all(1 <= roll <= 6 for roll in rolls[0]["details"]))

    def test_parameter_substitution(self):
        expr = "2*{multiplier}"
        parameters = {"multiplier": 5}
        result, _ = self.parser.parse(expr, parameters)
        self.assertEqual(result, 10)

    def test_multiple_dice_rolls(self):
        expr = "2d6+3d4"
        _, rolls = self.parser.parse(expr)
        self.assertEqual(len(rolls), 2)
        self.assertTrue(all(1 <= roll <= 6 for roll in rolls[0]["details"]))
        self.assertTrue(all(1 <= roll <= 4 for roll in rolls[1]["details"]))

    def test_invalid_expression(self):
        with self.assertRaises(Exception):
            try:
                self.parser.parse("2*/5")
            except Exception as e:
                pass
                return
            self.fail("Expected exception not raised")

    def test_negative_numbers(self):
        parser = DiceParser()
        self.assertEqual(parser.parse("3+-5")[0], -2)
        self.assertEqual(parser.parse("-3+5")[0], 2)

    def test_dice_roll_fixed_value(self):
        with patch('random.randint', side_effect=[3, 4]):
            parser = DiceParser()
            result, rolls = parser.parse("2d6")

            self.assertEqual(result, 7)

            self.assertEqual(len(rolls), 1)
            self.assertEqual(len(rolls[0]["details"]), 2)

            self.assertEqual(rolls[0]["details"][0], 3)
            self.assertEqual(rolls[0]["details"][1], 4)

    def test_dice_lowercase(self):
        with patch('random.randint', return_value=3):
            parser = DiceParser()
            result, rolls = parser.parse("1d6")
            self.assertEqual(result, 3)
            self.assertEqual(len(rolls), 1)
            self.assertEqual(rolls[0]["roll"], 3)
            self.assertEqual(rolls[0]["details"][0], 3)

    def test_dice_multiple_rolls(self):
        with patch('random.randint', side_effect=[2, 1, 5, 3, 6]):
            parser = DiceParser()
            result, rolls = parser.parse("2d4+3d6")

            expected_total = (2 + 1) + (5 + 3 + 6)
            self.assertEqual(result, expected_total)

            self.assertEqual(len(rolls), 2)

            self.assertEqual(rolls[0]["details"], [2, 1])
            self.assertEqual(rolls[1]["details"], [5, 3, 6])

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

        self.assertEqual(rolls[0]["details"], [4, 3, 5])

    def test_exponent_operation(self):
        parser = DiceParser()
        self.assertEqual(parser.parse("2^3")[0], 8)
        self.assertEqual(parser.parse("2^(1+2)")[0], 8)
        self.assertEqual(parser.parse("(2^2)^2")[0], 16)

if __name__ == '__main__':
    unittest.main()