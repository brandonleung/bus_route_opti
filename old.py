from pulp import *
from random import seed
from random import randint
from random import uniform
seed(1)

# --- model data ---

# set R of r routes
routes = ["r1","r2","r3"]

# cost of alternative, high alternative only used if bus route infeasible
cost_alternative = 1000

# number of potential nodes
nodes = [1,2,3,4,5,6,7,8,9,10]

# combination of segments, for segments that don't match
segments = [(i,j) for i in nodes for j in nodes if i < j ]
segment_costs = {}
# generate the distance/cost of traversing that segment
for s in segments:
    segment_costs[s] = round(uniform(1.5,9), 2)

# a num_node x num_node sized matrix, the OD passenger demand matrix
passenger_demand = {}
for i in nodes:
    row = {}
    for j in nodes:
        if i == j:
            row[j] = 0
        else:
            row[j] = randint(0,99)
    passenger_demand[i] = row

# --- decision variables ---
m_od = LpVariable.dicts("m_od", (nodes, nodes), 0, None, LpInteger)

# --- maximizing demand objective function 1 ---
# max_demand = LpProblem("MaxCustomerDemand", LpMaximize)
# max_demand += lpSum([m_od[i][j]*passenger_demand[i][j] for (i,j) in segments]), "Sum_of_Demand_Served"

# max_demand.solve()
# print(LpStatus[max_demand.status])
# print(value(max_demand.objective))
