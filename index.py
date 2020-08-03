from pulp import *
from random import seed
from random import randint

# --- model data ---

# set R of r routes
routes = ["r1","r2","r3","r4"]

# cost of alternative, high alternative only used if bus route infeasible
cost_alternative = 1000

# number of potential nodes
num_nodes = 15

# a num_node x num_node sized matrix, the OD passenger demand matrix
passenger_demand = []

# populate passenger_demand
seed(1)
for i in range(num_nodes):
    row = []
    for j in range(num_nodes):
        if i == j:
            row.append(0)
        else:
            row.append(randint(0,99))
    passenger_demand.append(row)


arc_cost = []


# --- decision variables ---

# if segment ij belongs to route r
x_ijr = LpVariable("x_ijr", 0, 1)

# if demand od traverses segment ij on route r
p_ijr_od = LpVariable("p_ijr_od", 0, 1) 

# if od stops at node i for transfer 
t_i_od = LpVariable("t_i_od", 0, 1)

# if demand od uses the bus system
m_od = LpVariable("m_od", 0, 1)


# --- objective functions ---
max_demand = LpProblem("maxDemand", LpMaximize)