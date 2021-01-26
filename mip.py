from mip import *

print("hello")


GPh = 0.18
disutility = 0.1
t = 3  # appliance.t
E = 0.8  # storage.E
IE = 3 # storage.IE
SD = 0.01 # storage.sd
P1 = 1.800  # household.p
MinC = 2.56 # min storage
MaxC = 6.4 # max storage
SP = 1
RQ = [0.1 for _ in range(24)]  # stockage.RQ
beta = 17 # appliance.beta
Lmax = 6000

m = Model(sense=MINIMIZE,solver_name=CBC)

GE = [ m.add_var(name='GE'+str(i),ub=Lmax,lb=0) for i in range(1,25)]
S = [ m.add_var(name='S'+str(i),var_type=BINARY) for i in range(1,25)]
IC = [ m.add_var(name='IC'+str(i),var_type=BINARY) for i in range(1,25)]
BE = [ m.add_var(name='BE'+str(i)) for i in range(1,25)]
RE = [ m.add_var(name='RE'+str(i),ub=RQ[i-1]) for i in range(1,25) ]
SE = [ m.add_var(name='SE'+str(i),ub=MaxC,lb=MinC) for i in range(1,25)]
tau = m.add_var(name='Tau',ub=beta)

for h in range(0,24):

    m+= (S[h]*P1 + IC[h]*SP == GE[h] + BE[h] + RE[h])

m+= SE[0] == IE*SD + IC[0]*SP*E-BE[0]
for h in range(1,24):
    m+= SE[h] == SE[h-1]*SD + IE*SD + IC[0]*SP*E-BE[0]

m+= xsum(S[h] for h in range(24)) == t
#Contrainte 11
for h in range(24):
    m+= (h+1)*S[h] <= tau
print("hi")
#%%
m.objective = xsum(GPh * GE[h] for h in range(24)) + disutility*tau
#%%
m.max_gap = 0.01
status = m.optimize(max_seconds=30)
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in m.vars:
        print('{} : {}'.format(v.name, v.x))