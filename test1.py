from sympy import symbols, And, Or, Not, Implies, simplify, satisfiable, pretty
import random
p, q, r = symbols('p q r')
test = ~(p & q & r) & (q | (p & r))
print(pretty(simplify(test)))