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
            ('NUMBER',   r'\d+(\.\d*)?'),       # Integer or decimal number
            ('ASSIGN',   r'='),                 # Assignment operator
            ('DICE',     r'd'),                 # Dice 'd'
            ('EXCLAM',   r'!+'),                # Explosions
            ('COND',     r'[KkLlHhMmDdCcVvUuRr#TtPpSs]'),  # Conditions
            ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),  # Identifiers
            ('OP',       r'[+\-*/]'),           # Arithmetic operators
            ('LPAREN',   r'\('),                # Left parenthesis
            ('RPAREN',   r'\)'),                # Right parenthesis
            ('COMMA',    r','),                 # Comma
            ('LBRACE',   r'\{'),                # Left brace
            ('RBRACE',   r'\}'),                # Right brace
            ('COMPARE',  r'[<>!=]{1,2}'),       # Comparison operators
            ('STRING',   r'\".*?\"|\'.*?\''),   # String literals
            ('NEWLINE',  r'\n'),                # Line endings
            ('SKIP',     r'[ \t]+'),            # Skip over spaces and tabs
            ('MISMATCH', r'.'),                 # Any other character
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
        result = self.parse_term()
        while self.current_token[0] == 'OP' and self.current_token[1] in ('+', '-'):
            op = self.current_token[1]
            self.next_token()
            right = self.parse_term()
            if op == '+':
                result += right
            elif op == '-':
                result -= right
        return result

    def parse_term(self):
        result = self.parse_factor()
        while self.current_token[0] == 'OP' and self.current_token[1] in ('*', '/'):
            op = self.current_token[1]
            self.next_token()
            right = self.parse_factor()
            if op == '*':
                result *= right
            elif op == '/':
                result /= right
        return result

    def parse_factor(self):
        token_type, token_value = self.current_token

        if token_type == 'NUMBER':
            num = int(token_value)
            self.next_token()
            if self.current_token[0] == 'DICE':
                self.next_token()
                sides = self.parse_sides()
                conditions = self.parse_conditions()
                rolls = [self.roll_die(sides) for _ in range(num)]
                rolls = self.apply_conditions(rolls, conditions, sides)
                total = sum(rolls)
                return total
            else:
                return num
        elif token_type == 'DICE':
            self.next_token()
            num = 1
            sides = self.parse_sides()
            conditions = self.parse_conditions()
            rolls = [self.roll_die(sides) for _ in range(num)]
            rolls = self.apply_conditions(rolls, conditions, sides)
            total = sum(rolls)
            return total
        elif token_type == 'LPAREN':
            self.next_token()
            expr = self.parse_expression()
            self.expect('RPAREN')
            return expr
        elif token_type == 'ID':
            var_name = token_value
            self.next_token()
            if self.current_token[0] == 'ASSIGN':
                self.next_token()
                value = self.parse_expression()
                self.variables[var_name] = value
                return value
            else:
                return self.variables.get(var_name, 0)
        else:
            raise SyntaxError('Unexpected token %s' % token_type)

    def parse_sides(self):
        token_type, token_value = self.current_token
        if token_type == 'NUMBER':
            sides = int(token_value)
            self.next_token()
            return sides
        elif token_type == 'ID':
            # Handle custom dice types if needed
            sides = token_value
            self.next_token()
            return sides
        else:
            raise SyntaxError('Expected number or identifier after "d"')

    def parse_conditions(self):
        conditions = []
        while self.current_token[0] in ('COND', 'EXCLAM'):
            cond = self.current_token[1]
            self.next_token()
            params = None
            if self.current_token[0] == 'LBRACE':
                params = self.parse_brace_content()
            else:
                if self.current_token[0] == 'NUMBER':
                    params = self.current_token[1]
                    self.next_token()
            conditions.append((cond, params))
        return conditions

    def parse_brace_content(self):
        self.expect('LBRACE')
        content = ''
        brace_count = 1
        while brace_count > 0:
            token_type, token_value = self.current_token
            if token_type == 'LBRACE':
                brace_count += 1
                content += token_value
                self.next_token()
            elif token_type == 'RBRACE':
                brace_count -= 1
                if brace_count == 0:
                    self.next_token()
                    break
                else:
                    content += token_value
                    self.next_token()
            else:
                content += token_value
                self.next_token()
        return content

    def roll_die(self, sides):
        if isinstance(sides, int):
            return self.random.randint(1, sides)
        else:
            # Placeholder for custom dice logic
            return 0

    def apply_conditions(self, rolls, conditions, sides):
        for cond, params in conditions:
            cond = cond.upper()
            if cond == 'K':  # Keep Highest
                num_keep = int(params) if params else 1
                rolls = sorted(rolls, reverse=True)[:num_keep]
            elif cond == 'KL':  # Keep Lowest
                num_keep = int(params) if params else 1
                rolls = sorted(rolls)[:num_keep]
            elif cond == 'D':  # Drop Lowest
                num_drop = int(params) if params else 1
                rolls = sorted(rolls)[num_drop:]
            elif cond == 'DH':  # Drop Highest
                num_drop = int(params) if params else 1
                rolls = sorted(rolls, reverse=True)[num_drop:]
            elif cond == '!':  # Explode
                rolls = self.handle_explode(rolls, sides, params)
            elif cond == 'R':  # Reroll
                reroll_values = self.parse_condition_params(params)
                for i in range(len(rolls)):
                    while rolls[i] in reroll_values:
                        rolls[i] = self.roll_die(sides)
            # Implement other conditions as needed
        return rolls

    def parse_condition_params(self, params):
        if not params:
            return [1]  # Default to rerolling ones
        return [int(p.strip()) for p in params.split(',')]

    def handle_explode(self, rolls, sides, params):
        new_rolls = []
        explode_value = sides  # Default explode value is the max side
        if params:
            explode_value = int(params)
        for roll in rolls:
            total = roll
            while roll == explode_value:
                roll = self.roll_die(sides)
                total += roll
            new_rolls.append(total)
        return new_rolls

# Example usage:
if __name__ == '__main__':
    roller = DiceRoller()
    notation = '4d6K3 + 2'
    result = roller.roll(notation)
    print('Result:', result)

    # Roll 5d10, keep highest 3
    result = roller.roll('5d10K3')
    print('Result:', result)

    # Roll 4d6, reroll ones
    result = roller.roll('4d6R{1}')
    print('Result:', result)

    # Roll 3d6, explode on 6
    result = roller.roll('3d6!')
    print('Result:', result)
