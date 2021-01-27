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
    """
     Input : use households and appliances ans stockages
     Output : CkTrade and DS
    :return:
    """


    ctot = 1

    GPh = 0.18
    disutility = 0.1
    t = 3  # appliance.t
    E = 0.8  # storage.E
    IE = 3 # storage.IE
    SD = 0.01 # storage.sd
    P1 = 1800  # household.p
    MinC = 2.56 # min storage
    MaxC = 6.4 # max storage
    SP = [MaxC-IE - i*0.1 for i in range(24)]  # stockage.sp
    RQ = [0.1 for _ in range(24)]  # stockage.RQ
    beta = 17 # appliance.beta
    Lmax = 6000


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
    for offset in range(24):
        l[offset, offset + x_index["GE"]] = -1  # -GEh
        l[offset, offset + x_index["S"]] = P1  # P1 * Sh
        l[offset, offset + x_index["IC"]] = SP[offset]  # SP * ICh
        l[offset, offset + x_index["BE"]] = -1  # -BEh
        l[offset, offset + x_index["RE"]] = -1  # -REh
        b[offset] = 0

    # Contrainte 8 : h [1, 24] -> S1 + .. + S24 = t
    l[24, x_index["S"]:x_index["IC"]] = 1
    b[24] = t

    # Contrainte 4 :
    l[25, x_index["SE"]] = 1
    l[25, x_index["IC"]] = - E * SP[0]
    l[25, x_index["BE"]] = 1
    b[25] = IE * SD
    for offset in range(1, 24):
        l[25 + offset, x_index["SE"] + offset] = 1
        l[25 + offset, x_index["SE"] + offset - 1] = -SD
        l[25, x_index["IC"] + offset] = - E * SP[offset]
        l[25, x_index["BE"] + offset] = 1
        b[25 + offset] = IE * SD

    lin = np.zeros((48, 145))
    bin = np.zeros(48)
#TODO Refaire la contrainte 11 & 15

    # Contrainte 11
    for offset in range(24):
        lin[offset, offset + x_index['S']] = offset + 1
        lin[offset, -1] = -1
        bin[offset] = 0

    #Contstrain 15
    for offset in range(24):
        lin[offset,offset] = 1
        bin[offset] = Lmax



     # "bounds"
    bounds = [(None, None) for _ in range(145)]
    # bounds = np.array(bounds)
    # Bounds SE:

    for offset in range(24):
        bounds[offset + x_index["SE"]] = (MinC, MaxC)

    # Bound RE
    for offset in range(24):
        bounds[offset + x_index["RE"]] = (None, RQ[offset])

    # Bound Tau
    bounds[-1] = (None, beta)

    # linprog
    res = linprog(c, A_eq=l, b_eq=b, A_ub=lin, b_ub=bin, bounds=bounds, options={"disp": True})
    print(res)

    return res

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
