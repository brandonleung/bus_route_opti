from pulp import *
from random import seed
from random import randint
seed(1)

# --- model data ---

events = { #            food pounds, dollars, meals yield, annual min, annual max
    "food_drive":       [300,0,231,500,2000],
    "church_drive_1":   [128000,8897,143045,1,9],
    "church_drive_2":   [0,826,4125,1,3],
    "media_1":          [20000,100000,515400,1,3],
    "media_2":          [8000,750,9910,1,2],
    "auction_1":        [0,58721,293605,1,3],
    "auction_2":        [0,1200,6000,1,3], 
    "auction_3":        [0,5000,25000,1,1],
    "auction_4":        [0,4500,22500,1,12], 
    "dinner_blues":     [0,15000,75000,1,1], 
    "dinner_jazz":      [0,22618,113090,1,3], 
    "concert_1":        [2500,0,1925,1,3], 
    "concert_2":        [600,2548,13202,1,4], 
    "concert_3":        [2042,12015,61647,1,3], 
    "zoo":              [3000,400,4310,1,18], 
    "5k_1":             [0,18000,90000,1,2], 
    "5k_2":             [0,13000,65000,1,3],
    "5k_3":             [0,3384,16920,1,6], 
    "golf_1":           [0,10000,50000,1,3], 
    "golf_2":           [0,4005,20025,1,1], 
    "company_1":        [0,3723,18615,1,8], 
    "company_2":        [125,300,1596,1,36], 
    "retail":           [0,1500,7500,1,3], 
    "matching_gift":    [0,20000,100000,1,3], 
    "sales_1":          [0,200000,1000000,1,10], 
    "sales_2":          [0,4586,22928,1,6],
    "food_1":           [0,3000,15000,1,2], 
    "food_2":           [0,5000,25000,1,1], 
    "social_media_1":   [0,26000,130000,1,1], 
    "social_media_2":   [0,1500,7500,1,1], 
    "social_media_3":   [0,14700,73500,1,12], 
    "pledge_1":         [0,5085,25425,1,12], 
    "pledge_2":         [0,82000,410000,1,2], 
    "pledge_3":         [0,65000,325000,1,1]
}

resources = { 
    "staff":        [14, 21600],
    "volunteers":   [10, 30000],
    "ceo":          [78, 400],
    "marketing":    [29, 1000],
    "IS":           [48, 500],
    "events":       [19, 5400],
    "donor_mgmt":   [19, 800],
    "board_members":[10, 1200],
    "ext_equipment":[40, 3600],
    "int_equipment":[40, 4500],
    "supplies":     [1, 100000],
    "storage":      [2, 200000],
    "meals":        [5, 25000]
}

(pounds, dollars, meals, mins, maxs) = splitDict(events)
(unit_resource_cost, resource_available) = splitDict(resources)

# generate resources
# (event,resource), cost
resource_cost = {}
for e in events:
    for r_key,r_value in resources.items():
        if (e is not "food_drive" and e is not "media_1"):
            k = e + "," + r_key
            resource_cost[k] = randint(0, 0.02*r_value[1])

# add known resources
food_drive = [3,5,0,0,0,1,0,0,1,1,10,57,0]
media_1 = [138,0,0,16,25,14,25,25,6,14,667,220,3800,400]

for i,r in enumerate(resources.keys()):
    resource_cost["food_drive,"+r] = food_drive[i]
    resource_cost["media_1,"+r] = media_1[i]

# --- decision variables ---
x = LpVariable.dicts("event", events, 0, None, LpInteger)
y = LpVariable.dicts("additional_resource", resources, 0, None, LpInteger)

# --- objective function ---
prob = LpProblem("MaximizeMeals", LpMaximize)
prob += lpSum([x[e]*((10/13)*pounds[e] + 5*dollars[e]) for e in events.keys()]) - lpSum(5*[y[r]*unit_resource_cost[r] for r in resources.keys()]), "Sum_of_Demand_Served"

# --- constraints ---
for r in resources.keys():
    # resource capacity
    prob += lpSum([x[e]*resource_cost[e + "," + r] for e in events.keys()]) <= resource_available[r] + y[r], "Sum_of_Resources_%s_Used"%r

for e in events.keys():
    # min number of event
    prob += x[e] >= mins[e], "Min_%s_Event"%e
    # max number of event
    prob += x[e] <= maxs[e], "Max_%s_Event"%e
    
# distribution budget
prob += (0.2/1.3)*lpSum([x[e]*pounds[e] for e in events.keys()]) <= lpSum([x[e]*dollars[e] for e in events.keys()]), "Distribution_Budget"

# --- results ---
prob.solve()

print(LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print(value(prob.objective))
