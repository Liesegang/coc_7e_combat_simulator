import ply.lex as lex
import ply.yacc as yacc
import random

class DiceParser:
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
            ("right", "UMINUS"),
            ("nonassoc", "LPAREN", "RPAREN"),
        )
        self.lexer = lex.lex(module=self)
        self.parser = yacc.yacc(module=self)

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
    t_ignore = " \t"

    def t_DICE(self, t):
        r"\d+[Dd]\d+"
        nums = t.value.lower().split("d")
        rolls = [random.randint(1, int(nums[1])) for _ in range(int(nums[0]))]
        t.value = sum(rolls)
        self.dice_rolls.append({"roll": t.value, "details": rolls})
        return t

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
        | expression MOD expression"""
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

    def p_expression_exponent(self, p):
        "expression : expression EXPONENT expression"
        p[0] = p[1] ** p[3]  # 指数演算を実装

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
        p[0] = self.current_parameters.get(key, 0)  # Use current parameters

    def p_error(self, p):
        if p:
            print(f"Syntax error at {p.value!r}")
        else:
            print("Syntax error at EOF")

    def parse(self, expression, parameters=None):
        self.current_parameters = parameters if parameters is not None else {}
        self.dice_rolls = []
        result = self.parser.parse(expression)
        return result, self.dice_rolls
