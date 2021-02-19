# x=BooleanVar(True)
# print('x: ', x)
from pyomo.environ import *
from pyomo.gdp import Disjunct, Disjunction
x=RangeSet(3)
# print('x: ', x)

# print('x: ', x[1])

y=(['PV','grid'])
print(y)

print( y['PV'])
