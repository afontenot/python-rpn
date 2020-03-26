# python-rpn

RPN is a proof-of-concept interpreter for entering Python commands
in a simple reverse-Polish style. The interpreter has the following
meta-commands to control the program's state:
 * help: display this text
 * stack: print the entire stack for debugging
 * clear: delete the entire stack
 * undo: restore the previous stack
 * exec: run the following Python command in the current namespace

RPN supports the following operations on the stack:
 * n collect: pop n elements of the stack and append them as a list
 * dup: duplicate the top element on the stack
 * n dups: duplicate the top n elements on the stack

Python built-in functions (and functions from math) are supported, and
given a number of (popped) arguments from the stack equal to the number
of arguments accepted by the function. Obviously this won't work as expected
for some functions, so that's one limitation of this proof-of-concept.

Any other text is assumed to be an RPN expression. For example:
 * 1 2 3: add the numbers 1 2 3 to the stack
 * 1 2 +: add 3 to the stack
 * 1 2 3 3 collect sum print: add [1, 2, 3] to the stack and print 6

Note that python built-ins like sum and print are available, along with the
 built-in operators and functions from math, by default.
