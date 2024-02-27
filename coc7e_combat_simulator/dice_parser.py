from enum import Enum
from typing import Tuple
import ply.lex as lex
import ply.yacc as yacc
import random

import logging

logger = logging.getLogger(__name__)


class RollDetails:
    def __init__(self, roll: int, details: list[int]):
        self.roll = roll
        self.details = details

    def __repr__(self) -> str:
        return f"Roll: {self.roll}, Details: {self.details}"


class DiceParser:
    class Mode(Enum):
        ROLL = 1
        EXPECTED = 2
        MAXIMUM = 3
        MINIMUM = 4

    def __init__(self):
        self.dice_rolls = []
        self.tokens = (
            "NUMBER",
            "DICE",
            "PLUS",
            "MINUS",
            "TIMES",
            "DIVIDE",
            "MOD",
            "EXPONENT",
            "UMINUS",
            "LPAREN",
            "RPAREN",
            "PARAMETER",
        )
        self.precedence = (
            ("right", "EXPONENT"),
            ("left", "PLUS", "MINUS"),
            ("left", "TIMES", "DIVIDE", "MOD"),
            ("left", "DICE"),
            ("right", "UMINUS"),
            ("nonassoc", "LPAREN", "RPAREN"),
        )
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)
        self.mode = self.Mode.ROLL

    # Lexer rules
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"\/"
    t_MOD = r"%"
    t_EXPONENT = r"\^"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_PARAMETER = r"\{[a-zA-Z_][a-zA-Z0-9_]*\}"
    t_DICE = r"[dD]"
    t_ignore = " \t"

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    # Parser rules
    def p_expression_binop(self, p):
        """expression : expression PLUS expression
        | expression MINUS expression
        | expression TIMES expression
        | expression DIVIDE expression
        | expression MOD expression
        | expression DICE expression"""
        if p[2] == "+":
            p[0] = p[1] + p[3]
        elif p[2] == "-":
            p[0] = p[1] - p[3]
        elif p[2] == "*":
            p[0] = p[1] * p[3]
        elif p[2] == "/":
            p[0] = p[1] / p[3]
        elif p[2] == "%":
            p[0] = p[1] % p[3]
        elif p[2].lower() == "d":
            dice_faces = p[3]
            dice_count = p[1]
            if self.mode == self.Mode.ROLL:
                rolls = [random.randint(1, dice_faces) for _ in range(dice_count)]
                p[0] = sum(rolls)
                self.dice_rolls.append(RollDetails(p[0], rolls))
                logger.info(f"Rolling {p[1]}D{p[3]} with {rolls}")
            elif self.mode == self.Mode.EXPECTED:
                # 期待値 = (最小値 + 最大値) / 2 * 個数
                expected_value = (1 + dice_faces) / 2 * dice_count
                p[0] = expected_value
                logger.info(f"Expected value of {p[1]}D{p[3]} is {p[0]}")
            elif self.mode == self.Mode.MAXIMUM:
                p[0] = dice_faces * dice_count
                logger.info(f"Maximum value of {p[1]}D{p[3]} is {p[0]}")
            elif self.mode == self.Mode.MINIMUM:
                p[0] = dice_count
                logger.info(f"Minimum value of {p[1]}D{p[3]} is {p[0]}")

    def p_expression_exponent(self, p):
        "expression : expression EXPONENT expression"
        p[0] = p[1] ** p[3]

    def p_expression_uminus(self, p):
        "expression : MINUS expression %prec UMINUS"
        p[0] = -p[2]

    def p_expression_group(self, p):
        "expression : LPAREN expression RPAREN"
        p[0] = p[2]

    def p_expression_dice(self, p):
        "expression : DICE"
        p[0] = p[1]

    def p_expression_number(self, p):
        "expression : NUMBER"
        p[0] = p[1]

    def p_expression_parameter(self, p):
        "expression : PARAMETER"
        key = p[1][1:-1]
        p[0] = self.current_parameters.get(key, 0)

    def p_error(self, p):
        if p:
            print(f"Syntax error at {p.value!r}")
        else:
            print("Syntax error at EOF")

    def parse(
        self, expression: str, parameters=None
    ) -> Tuple[float, list[RollDetails]]:
        logger.info(f"Parsing {expression} with parameters {parameters}")
        self.current_parameters = parameters if parameters is not None else {}
        self.dice_rolls = []
        self.mode = self.Mode.ROLL
        result = self.parser.parse(expression)
        return result, self.dice_rolls

    def expected(self, expression: str, parameters=None) -> float:
        logger.info(
            f"Calculating expected value of {expression} with parameters {parameters}"
        )
        self.current_parameters = parameters if parameters is not None else {}
        self.dice_rolls = []
        self.mode = self.Mode.EXPECTED
        result = self.parser.parse(expression)
        return result

    def maximum(self, expression: str, parameters=None) -> float:
        logger.info(
            f"Calculating maximum value of {expression} with parameters {parameters}"
        )
        self.current_parameters = parameters if parameters is not None else {}
        self.dice_rolls = []
        self.mode = self.Mode.MAXIMUM
        result = self.parser.parse(expression)
        return result

    def minimum(self, expression: str, parameters=None) -> float:
        logger.info(
            f"Calculating minimum value of {expression} with parameters {parameters}"
        )
        self.current_parameters = parameters if parameters is not None else {}
        self.dice_rolls = []
        self.mode = self.Mode.MINIMUM
        result = self.parser.parse(expression)
        return result
