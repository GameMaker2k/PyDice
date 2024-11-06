#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2016-2021 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2016-2021 Joshua Przyborowski - https://github.com/JoshuaPrzyborowski

    $FileInfo: pydice.py - Last Update: 1/4/2021 Ver. 0.3.4 RC 1 - Author: joshuatp $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
import re
import random

__program_name__ = "PyDice-Roll"
__project__ = __program_name__
__project_url__ = "https://github.com/JoshuaPrzyborowski/PyDice"
__version_info__ = (0, 3, 4, "RC 1", 1)
__version_date_info__ = (2024, 10, 22, "RC 1", 1)
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[
    1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2)
if(__version_info__[4] != None):
    __version_date_plusrc__ = __version_date__ + \
        "-"+str(__version_date_info__[4])
if(__version_info__[4] == None):
    __version_date_plusrc__ = __version_date__
if(__version_info__[3] != None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(
        __version_info__[2])+" "+str(__version_info__[3])
if(__version_info__[3] == None):
    __version__ = str(
        __version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])


from __future__ import division, print_function
import re
import random

class DiceRoller:
    def __init__(self, seed=None):
        self.random = random.Random(seed)
        self.variables = {}
        self.user_values = {}

    def roll(self, expression):
        self.tokens = self.tokenize(expression)
        self.current_token = None
        self.next_token()
        result = self.parse_expression()
        return result

    def tokenize(self, expression):
        token_specification = [
            ('NUMBER',   r'\d+(\.\d*)?'),   # Integer or decimal number
            ('ASSIGN',   r'='),             # Assignment operator
            ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
            ('OP',       r'[+\-*/]'),       # Arithmetic operators
            ('DICE',     r'd'),             # Dice 'd'
            ('LPAREN',   r'\('),            # Left parenthesis
            ('RPAREN',   r'\)'),            # Right parenthesis
            ('COMMA',    r','),             # Comma
            ('EXCLAM',   r'!+'),            # Explosions
            ('COND',     r'[KkLlHhMmDdCcVvUuRr#TtPpSs]'), # Conditions
            ('LBRACE',   r'\{'),            # Left brace
            ('RBRACE',   r'\}'),            # Right brace
            ('COMPARE',  r'[<>!=]{1,2}'),   # Comparison operators
            ('STRING',   r'\".*?\"|\'.*?\''), # String literals
            ('NEWLINE',  r'\n'),            # Line endings
            ('SKIP',     r'[ \t]+'),        # Skip over spaces and tabs
            ('MISMATCH', r'.'),             # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line = expression
        pos = 0
        tokens = []
        match = get_token(line)
        while match is not None:
            typ = match.lastgroup
            if typ != 'SKIP' and typ != 'NEWLINE':
                val = match.group(typ)
                tokens.append((typ, val))
            pos = match.end()
            match = get_token(line, pos)
        return tokens

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = ('EOF', '')

    def expect(self, token_type):
        if self.current_token[0] == token_type:
            val = self.current_token[1]
            self.next_token()
            return val
        else:
            raise SyntaxError('Expected %s but got %s' % (token_type, self.current_token[0]))

    def parse_expression(self):
        if self.current_token[0] == 'ID' and self.lookahead()[0] == 'ASSIGN':
            var_name = self.expect('ID')
            self.expect('ASSIGN')
            value = self.parse_expression()
            self.variables[var_name] = value
            return value
        else:
            return self.parse_term()

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token[0] in ('OP',):
            op = self.expect('OP')
            right = self.parse_factor()
            node = self.evaluate_op(node, op, right)
        return node

    def parse_factor(self):
        token_type, token_value = self.current_token
        if token_type == 'NUMBER':
            self.next_token()
            return float(token_value)
        elif token_type == 'ID':
            self.next_token()
            # Check for function call
            if self.current_token[0] == 'LPAREN':
                args = self.parse_arguments()
                return self.evaluate_function(token_value, args)
            else:
                return self.variables.get(token_value, self.user_values.get(token_value, 0))
        elif token_type == 'DICE':
            return self.parse_dice()
        elif token_type == 'LPAREN':
            self.next_token()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError('Unexpected token %s' % token_type)

    def parse_dice(self):
        num_dice = 1
        if self.tokens and self.tokens[0][0] == 'NUMBER':
            num_dice = int(self.expect('NUMBER'))
        self.expect('DICE')
        if self.current_token[0] == 'ID' or self.current_token[0] == 'NUMBER':
            sides = self.expect(self.current_token[0])
            if sides.isdigit():
                sides = int(sides)
            else:
                # Custom die type (e.g., 'proficiency')
                sides = sides  # Handle custom dice separately
        else:
            raise SyntaxError('Expected die sides')
        # Handle roll conditions
        conditions = self.parse_conditions()
        rolls = []
        for _ in range(num_dice):
            roll = self.roll_die(sides)
            rolls.append(roll)
        # Apply conditions
        rolls = self.apply_conditions(rolls, conditions, sides)
        total = sum(rolls)
        return total

    def parse_conditions(self):
        conditions = []
        while self.current_token[0] in ('COND', 'EXCLAM'):
            cond = self.expect(self.current_token[0])
            params = None
            if self.current_token[0] == 'LBRACE':
                params = self.parse_brace_content()
            conditions.append((cond, params))
        return conditions

    def parse_brace_content(self):
        self.expect('LBRACE')
        content = ''
        while self.current_token[0] != 'RBRACE':
            content += self.current_token[1]
            self.next_token()
        self.expect('RBRACE')
        return content

    def parse_arguments(self):
        args = []
        self.expect('LPAREN')
        while self.current_token[0] != 'RPAREN':
            args.append(self.parse_expression())
            if self.current_token[0] == 'COMMA':
                self.next_token()
        self.expect('RPAREN')
        return args

    def evaluate_op(self, left, op, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        else:
            raise SyntaxError('Unknown operator %s' % op)

    def evaluate_function(self, name, args):
        functions = {
            'round': round,
            'min': min,
            'max': max,
            'clamp': lambda x, min_val, max_val: max(min(x, max_val), min_val),
            'rnd': lambda a, b: self.random.randint(int(a), int(b)),
            # Add more functions as needed
        }
        if name in functions:
            return functions[name](*args)
        else:
            raise NameError('Unknown function %s' % name)

    def roll_die(self, sides):
        if isinstance(sides, int):
            return self.random.randint(1, sides)
        else:
            # Handle custom dice
            return 0  # Placeholder

    def apply_conditions(self, rolls, conditions, sides):
        # Implement conditions like 'K', 'KL', '!', 'R', etc.
        # For brevity, only 'K' (keep highest) is implemented here
        for cond, params in conditions:
            if cond.upper() == 'K':
                num_keep = int(params) if params else len(rolls) - 1
                rolls = sorted(rolls, reverse=True)[:num_keep]
            # Implement other conditions as needed
        return rolls

    def lookahead(self):
        if self.tokens:
            return self.tokens[0]
        else:
            return ('EOF', '')

def apply_conditions(self, rolls, conditions, sides):
    for cond, params in conditions:
        if cond.upper() == 'K':
            num_keep = int(params) if params else len(rolls) - 1
            rolls = sorted(rolls, reverse=True)[:num_keep]
        elif cond.upper() == 'R':
            reroll_values = self.parse_condition_params(params)
            for i in range(len(rolls)):
                while rolls[i] in reroll_values:
                    rolls[i] = self.roll_die(sides)
        # Add more conditions here
    return rolls

def parse_condition_params(self, params):
    if not params:
        return [1]  # Default to rerolling ones
    # Parse params into a list of values or conditions
    # Implement parsing logic based on your needs
    return [int(p.strip()) for p in params.split(',')]

# Example usage:
if __name__ == '__main__':
    roller = DiceRoller()
    notation = '4d6K3 + 2'
    result = roller.roll(notation)
    print('Result:', result)

    roller = DiceRoller()

    # Roll 5d10, keep highest 3
    result = roller.roll('5d10K3')
    print('Result:', result)

    # Roll 4d6, reroll ones
    result = roller.roll('4d6R{1}')
    print('Result:', result)

    # Roll 3d6, explode on 6
    result = roller.roll('3d6!')
    print('Result:', result)

