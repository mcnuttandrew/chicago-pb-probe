import pandas as pd
import json

## setup
ward_totals = [
    {"ward": 29}, 
    {"ward": 35}, 
    {"ward": 36}, 
    {"ward": 49}
    ]
table_data = {
    "race": [],
    "income": [],
    "educ": []
}

# modifies object for given category in place
def append_entry(obj, ward, pop, part):
    obj["Ward {} Pop Count".format(ward)] = pop
    obj["Ward {} Part Count".format(ward)] = part
    totals = [wt for wt in ward_totals if wt["ward"] == ward][0]
    obj["Ward {} Pop Perc".format(ward)] = pop / totals["pop"]
    obj["Ward {} Part Perc".format(ward)] = part / totals["part"]

# computes total pop and part for given ward
def compute_totals(ward, df0, df1, df2):
    curr_df0 = df0[df0["ward"] == ward]
    curr_df1 = df1[df1["ward"] == ward]
    curr_df2 = df2[df2["ward"] == ward]
    max_pop_total = max(curr_df0["pop"].sum(), curr_df1["pop"].sum(), curr_df2["pop"].sum())
    max_part_total = max(curr_df0["part"].sum(), curr_df1["part"].sum(), curr_df2["part"].sum())
    return (max_pop_total, max_part_total)
    


## main
# load count data
race_df = pd.read_csv("participation_simulation/race.csv")
edu_df = pd.read_csv("participation_simulation/educ.csv")
income_df = pd.read_csv("participation_simulation/income.csv")

# compute normalizing totals per ward
for wd in ward_totals:
    totals = compute_totals(wd["ward"], race_df, edu_df, income_df)
    wd["pop"], wd["part"] = totals

# construct race table
race_categories = race_df["race"].unique()
for r in race_categories:
    curr_obj = {"category": r.capitalize()}
    curr_df = race_df[race_df["race"] == r]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"]), axis = 1)
    table_data["race"].append(curr_obj)

# construct income table
income_categories = income_df["income_cohort"].unique()
for i in income_categories:
    curr_obj = {"category": i}
    curr_df = income_df[income_df["income_cohort"] == i]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"]), axis = 1)
    table_data["income"].append(curr_obj)

# construct edu table
edu_categories = edu_df["education"].unique()
for e in edu_categories:
    curr_obj = {"category": e.capitalize()}
    curr_df = edu_df[edu_df["education"] == e]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"]), axis = 1)
    table_data["educ"].append(curr_obj)

# print(table_data)
with open("demo_table_data.json","w") as f:
    json.dump(table_data, f)
