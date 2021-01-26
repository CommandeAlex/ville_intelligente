# import Classes
from Classes.EnergySuplier import EnergySuplier
from Classes.Household import Household
from Classes.Microgrid import Microgrid
import numpy as np
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
    # TODO :
    # Construire les matrices A, b, c et bounds
    # A = (?,?) de zéros
    # Ligne par ligne => remplissage (DUR)
    # x size = 6h+1 -> 169
    GPh = 1
    disutility = 0.1
    c = np.zeros(145)
    # x = [GE1 .. GE24, S1 .. S24, IC1 .. IC24, BE1 .. BE24, RE1 .. RE24, SE1 .. SE24, Tau]
    x_index = {"GE": 0, "S": 24, "IC": 48, "BE": 72, "RE": 96, "SE": 120}

    # Fonction de cout
    c[:25] = GPh
    c[-1] = disutility

    # Matrice de contraintes
    b = np.zeros(50)

    # Contrainte 3 : h [1,24] Lh = -> -1 GEh + P1*Sh + SP * ICh - BEh - REh = (0)
    l = np.zeros((50, 145))
    P1 = 0  # household.p
    SP = 0  # stockage.sp
    for offset in range(24):
        l[offset, offset + x_index["GE"]] = -1  # -GEh
        l[offset, offset + x_index["S"]] = P1  # P1 * Sh
        l[offset, offset + x_index["IC"]] = SP  # SP * ICh
        l[offset, offset + x_index["BE"]] = -1  # -BEh
        l[offset, offset + x_index["RE"]] = -1  # -REh
        b[offset] = 0

    # Contrainte 8 : h [1, 24] -> S1 + .. + S24 = t
    t = 1 # appliance.t
    l[24, x_index["S"]:x_index["IC"]] = 1
    b[24] = t

    # Contrainte 4 :
    E = 1  # storage.E
    IE = 1 # storage.IE
    SD = 0.01 # storage.sd
    l[25, x_index["SE"]] = 1
    l[25, x_index["IC"]] = - E * SP
    l[25, x_index["BE"]] = 1
    b[25] = IE * SD
    for offset in range(1, 24):
        l[25 + offset, x_index["SE"] + offset] = 1
        l[25 + offset, x_index["SE"] + offset - 1] = -SD
        l[25, x_index["IC"] + offset] = - E * SP
        l[25, x_index["BE"] + offset] = 1
        b[25 + offset] = IE * SD

    lin = np.zeros((24, 145))
    bin = np.zeros(24)

    # Contrainte 11
    for offset in range(24):
        lin[offset, offset] = 1
        lin[offset, -1] = -1
        bin[offset] = 0

     # "bounds"
    bounds = [(None, None) for _ in range(145)]
    # bounds = np.array(bounds)
    # Bounds SE:
    MinC = 10 # min storage
    MaxC = 100 # max storage
    for offset in range(24):
        bounds[offset + x_index["SE"]] = (MinC, MaxC)

    # Bound RE
    RQ = [w for w in range(24)]  # stockage.RQ
    for offset in range(24):
        bounds[offset + x_index["RE"]] = (None, RQ[offset])

    # Bound Tau
    beta = 1 # appliance.beta
    bounds[-1] = (None, beta)

    print('Matrice l ?', l)
    print('Matrice bounds ?', bounds)


    # linprog
    res = linprog(c, A_eq=l.tolist(), b_eq=b.tolist(), A_ub=lin.tolist(), b_ub=bin.tolist() , bounds=bounds, options={"disp": True})
    print(res)
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
# for household in list_households:
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
