#!/usr/bin/env python3
# coding: utf-8

import re
from enum import Enum
from collections import namedtuple

__all__ = ['lex', 'parse']

Token = namedtuple('Token', ['type', 'match'])


class TokenEnum(Enum):
    def __init__(self, pattern):
        self.pattern = re.compile(pattern)


class DefaultContextToken(TokenEnum):
    LBRACE = r'{'
    OTHER = '.'


class RegexDefinitionContextToken(TokenEnum):
    RBRACE = r'}'
    IDENT = r'[A-Za-z_]\w*(?=:)'
    COLON = ':'


class RegexContextToken(TokenEnum):
    LBRACE, RBRACE = r'{', r'}'
    REGEXCHAR = '.'


class State(Enum):
    def __init__(self, token_set):
        self.token_set = token_set

    DEFAULT = DefaultContextToken
    REGEX_DEF = RegexDefinitionContextToken
    REGEX = RegexContextToken


def lex(s: str) -> list:
    atoms = []
    braces_opened = 0
    state = State.DEFAULT

    while s:
        if state == State.DEFAULT:
            for t in state.token_set:
                m = t.pattern.match(s)

                if m is not None:
                    s = s[m.end():]

                    if t == state.token_set.LBRACE:
                        state = State.REGEX_DEF
                        break

                    token = Token(t, m)
                    atoms.append(token)
                    break

        elif state == State.REGEX_DEF:
            for t in state.token_set:
                m = t.pattern.match(s)

                if m is not None:
                    s = s[m.end():]

                    if t == state.token_set.COLON:
                        state = State.REGEX

                    token = Token(t, m)
                    atoms.append(token)
                    break

        elif state == State.REGEX:
            for t in state.token_set:
                m = t.pattern.match(s)

                if m is not None:
                    s = s[m.end():]

                    if t == state.token_set.LBRACE:
                        braces_opened += 1
                        t = RegexContextToken.REGEXCHAR

                    elif t == state.token_set.RBRACE:
                        if not braces_opened:
                            state = State.DEFAULT
                            break
                        else:
                            braces_opened -= 1
                            t = RegexContextToken.REGEXCHAR

                    token = Token(t, m)
                    atoms.append(token)
                    break

    if state != State.DEFAULT:
        raise SyntaxError("Unbalanced braces")

    return atoms


def parse(s: str):
    tokens = lex(s)
    pattern = ''

    while tokens:
        try:
            literal = ''
            while tokens[0].type == DefaultContextToken.OTHER:
                literal += tokens.pop(0).match.group(0)
            pattern += re.escape(literal)

            if tokens[0].type == RegexDefinitionContextToken.IDENT and\
               tokens[1].type == RegexDefinitionContextToken.COLON:

                groupname = tokens.pop(0).match.group(0)
                tokens.pop(0)

                regex = ''
                while tokens[0].type == RegexContextToken.REGEXCHAR:
                    regex += tokens.pop(0).match.group(0)
                    if not tokens:
                        break
                pattern += '(?P<{name}>{regex})'.format(name=groupname, regex=regex)

        except IndexError:
            break

    return re.compile(pattern)