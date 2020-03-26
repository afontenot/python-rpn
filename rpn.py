#!/usr/bin/env python3
import readline
import sys
import types
from inspect import _empty, signature
from math import *

built_in_ops_1 = ['~', 'not']
built_in_ops_2 = ['+', 'in', '/', '//', '&', '^', '|', '**', 'is', '<<', '%', '*',
                  '@', '>>', '-', '<', '<=', '==', '!=', '>=', '>'] # what about 'is not'?

help_text = ("RPN is a proof-of-concept interpreter for entering Python commands\n"
             "in a simple reverse-Polish style. The interpreter has the following\n"
             "meta-commands to control the program's state:\n"
             " * help: display this text\n"
             " * stack: print the entire stack for debugging\n"
             " * clear: delete the entire stack\n"
             " * undo: restore the previous stack\n"
             " * exec: run the following Python command in the current namespace\n\n"
             ""
             "RPN supports the following operations on the stack:\n"
             " * n collect: pop n elements of the stack and append them as a list\n"
             " * dup: duplicate the top element on the stack\n"
             " * n dups: duplicate the top n elements on the stack\n\n"
             ""
             "Python built-in functions (and functions from math) are supported, and\n"
             "given a number of (popped) arguments from the stack equal to the number\n"
             "of arguments accepted by the function. Obviously this won't work as expected\n"
             "for some functions, so that's one limitation of this proof-of-concept.\n\n"
             ""
             "Any other text is assumed to be an RPN expression. For example:\n"
             " * 1 2 3: add the numbers 1 2 3 to the stack\n"
             " * 1 2 +: add 3 to the stack\n"
             " * 1 2 3 3 collect sum print: add [1, 2, 3] to the stack and print 6\n\n"
             ""
             "Note that python built-ins like sum and print are available, along with the\n"
             " built-in operators and functions from math, by default.")


class RPN:
    def __init__(self):
        self.prev_stack = []
        self.stack = []
        self.rpn_actions = {"collect": lambda x: [[self.stack.pop() for _ in range(x)]],
                            "dup": lambda x: [x, x],
                            "dups": lambda x: [self.stack.pop() for _ in range(x)]}

    def __parse__(self, val):
        if val in built_in_ops_1 or val in built_in_ops_2 or val in self.rpn_actions:
            return val
        try:
            return eval(val)
        except NameError:
            print("fail: could not parse", val)
            return ""

    # count number of *required* arguments for a function
    # returns ValueError for built-ins with no signature, like print
    def __countargs__(self, function):
        params = signature(function).parameters.values()
        return sum(x.default is _empty for x in params)

    def eval(self, expr):
        self.prev_stack = self.stack
        words = [self.__parse__(word) for word in expr.split()]
        for word in words:
            if word in self.rpn_actions:
                top = self.stack.pop()
                result = self.rpn_actions[word](top)
                if result is None:
                    self.stack.append(top)
                else:
                    self.stack.extend(result)
            elif isinstance(word, types.BuiltinFunctionType):
                try:
                    num_args = self.__countargs__(word)
                except ValueError: # fail open for e.g. print
                    num_args = 1
                args = [self.stack.pop() for _ in range(num_args)]
                result = word(*args)
                if result is None:
                    for arg in args[::-1]:
                        self.stack.append(arg)
                else:
                    self.stack.append(result)
            elif word in built_in_ops_1:
                top = self.stack.pop()
                result = eval(f"{word} {top}")
                if result is None:
                    self.stack.append(top)
                else:
                    self.stack.append(result)
            elif word in built_in_ops_2:
                top_1 = self.stack.pop()
                top_2 = self.stack.pop()
                result = eval(f"{top_2} {word} {top_1}")
                if result is None:
                    self.stack.append(top_2)
                    self.stack.append(top_1)
                else:
                    self.stack.append(result)
            else:
                if word != "":
                    self.stack.append(word)

    def __str__(self):
        return str(self.stack)

    def clear(self):
        self.prev_stack = self.stack
        self.stack = []

    def undo(self):
        self.stack = self.prev_stack


if __name__ == '__main__':
    rpn = RPN()
    
    def repl(val):
        if val == "stack" or val == "debug":
            print(rpn)
        elif val == "clear":
            rpn.clear()
        elif val == "undo":
            rpn.undo()
        elif val == "help":
            print(help_text)
        elif val.split()[0] == "exec":
            exec(' '.join(val.split()[1:]))
        else:
            try:
                rpn.eval(val)
            except Exception as ex:
                print("fail:", ex)
   
    inputtext = ">>> "
    if sys.stdin.isatty():
        print("RPN python interpreter 0.1.0\nTry help for commands.\n")
    else:
        inputtext = ""
    while True:
        try:
            inp = input(inputtext)
        except (EOFError, SystemError):
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        repl(inp)
