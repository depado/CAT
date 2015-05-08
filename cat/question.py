#!/usr/bin/env python3
# coding: utf-8

import re

from .script import Script
from .pattern import parse

__all__ = ['Question', 'UnknownQuery']


class UnknownQuery(SyntaxError):
    pass


class Question:
    """
    A question asked to the user and execute a script
    depending on the answer.
    """

    def __init__(self, text: str, scripts: list=()):
        """
        :param text:    str object representing the
                        question text/prompt.
        :param scripts: list of Script objects that are
                        executed or not depending on the
                        question's answer given.
        """

        self.text = text
        self.scripts = list(scripts)

    def ask(self):
        """
        Ask the user the question and execute the detected
        script. Return the result of that script.

        :return: The return value of the detected script
        """

        answer = input(self.text)

        for script in self.scripts:
            m = script.pattern.match(answer)

            if m is not None:
                return script.execute(m)

        raise UnknownQuery('Unmatched answer {!r}'.format(answer))

    def script(self, expr: str, *flags):
        """
        Instantiate a new script.

        :param keywords: The regular expression to which
                         the script will react.
        :return: the function as-is
        """

        if isinstance(expr, str):
            expr = re.compile(parse(expr), *flags)

        def _decorator_wrapper(fn: callable):
            script = Script(fn, expr, [self])
            self.scripts.append(script)
            return script

        return _decorator_wrapper