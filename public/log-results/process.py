import json
import pandas as pd

USERS = [
    ("p01", "p01"), 
    ("p02", "p02"), 
    ("p03", "p03"), 
    ("p04", "p04"), 
    ("p05", "p05"), 
    ("a01", "p06"), 
    ("a02", "p07"), 
    ("a03", "p08"), 
    ("a04", "p09"), 
    ("a05", "p10"), 
    ("a06", "p11"), 
    ("a07", "p12"), 
    ("a08", "p13")
]
PROJECT_COSTS = {
    "Street Resurfacing": 475000, 
    "Bike Lanes": 75000, 
    "School Improvements": 500000, 
    "Picnic Tables": 35700,
    "Street Lights": 115000,
    "Food Pantry": 2500, 
    "Street Murals": 75000,
    "Curb Cuts": 40000
}


with open("data.json") as f:
    data = json.load(f)

df_list = []
for u, pid in USERS:
    # get user dictionary
    user_data = [d for d in data if d["userId"] == u][0]
    # create data frame columns
    user = []
    project = []
    rank = []
    pre_allocations = []
    post_allocations = []
    cost = []
    for i, p in enumerate(user_data["sortOrder"]):
        user.append(pid)
        project.append(p)
        rank.append(i + 1)
        if user_data["allocations"][p] > 0:
            pre_allocations.append(round(user_data["allocations"][p]))
        else: 
            pre_allocations.append(0)
        if user_data["postCheckAllocations"][p] > 0:
            post_allocations.append(round(user_data["postCheckAllocations"][p]))
        else:
            post_allocations.append(0)
        cost.append(PROJECT_COSTS[p])

    d = {
        "user": user, 
        "project": project, 
        "sort_rank": rank, 
        "pre_rank": [sorted(pre_allocations, reverse=True).index(x) + 1 for x in pre_allocations],
        "post_rank": [sorted(post_allocations, reverse=True).index(x) + 1 for x in post_allocations],
        "pre_allocations": pre_allocations, 
        "post_allocations": post_allocations,
        "cost": cost
    }
    user_df = pd.DataFrame(data = d)

    df_list.append(user_df)

out = pd.concat(df_list)

print(out.head())

out.to_csv('processed_data.csv', index=False)