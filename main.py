# import Classes
from Classes.EnergySuplier import EnergySuplier
from Classes.Household import Household
from Classes.Microgrid import Microgrid
# import solver
from scipy.optimize import linprog


# simplex optimizer :https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
"""
minimize:

c @ x

such that:

A_ub @ x <= b_ub
A_eq @ x == b_eq
lb <= x <= ub

"""

print("Hello World.")


# TO DO: Implementer les classes
# TO DO: Trouver un solveur de symplex et implementer les variables
# TO DO: Explorer les datas
# TO DO: Implementer un data feeder
# TO DO: Debbug and run the algorithm
# TO DO: Display results -> classe résultats

"""Data"""
K = 4   # Number of households
h = 1   # Step
hl = 60  # length
H = [i for i in range(0, hl, h)]  # time distribution

"""Classes instantiation"""

# Generator :
generator = EnergySuplier([])
# Microgrid :
microgrid = Microgrid()
# Households :
list_households = []
for k in range(K):
    list_households.append(Household())
    pass

"""Algorithm ECO-TRADE"""

# Module 1
def module1():
    # Input : use households and appliances ans stockages
    # Output : CkTrade and DS
    ctot = 1

    return ctot

# Module 2
def module2():
    # Input : use households and appliances ans stockages
    # Output : Microgrid energy price (MP)

    return 0

# Module 3
def module3():
    # Input : use households and appliances ans stockages
    # Output : solution and ME

    return 1, []


# ECO-TRADE Algorithm

epsilon_count, epsilon_max, Cpre = 0, 0, 0
Ccur, epsilon_cur, epsilon = 1, 0, 0.7
for household in list_households:
    Cpre += module1()
print("Cost at initialization :", Cpre)
while epsilon_count <= epsilon_max:
    module2()
    Ccur, x = module3()

    epsilon_cur = abs((Cpre - Ccur)/Cpre)
    if epsilon_cur <= epsilon:
        epsilon_count += 1
    else:
        epsilon_count = 0
    Cpre = Ccur

# final solution :
print("Solution :", x)
