import pandas as pd
import json

## setup
ward_totals = [
    {"ward": 29, "totals": {}}, 
    {"ward": 35, "totals": {}}, 
    {"ward": 36, "totals": {}}, 
    {"ward": 49, "totals": {}}
    ]
table_data = {
    "race": [],
    "income": [],
    "educ": []
}
SORT_ORDERS = {
    "race": {
        "White": 0, 
        "Black or African American": 1, 
        "Asian": 2, 
        "Hispanic or Latino/a": 3, 
        "Other": 4
    },
    "income": {
        "Less than $10,000": 0,
        "$10,000-$24,999": 1,
        "$25,000-$39,999": 2,
        "$40,000-$59,999": 3,
        "$60,000-$99,999": 4,
        "$100,000-$149,999": 5,
        "More than $150,000": 6
    },
    "educ": {
        "Less than high school": 0,
        "High school": 1,
        "Some college": 2,
        "Professional school": 3,
        "Bachelor's": 4,
        "Master's": 5,
        "Doctorate": 6
    }
}

# modifies object for given category in place
def append_entry(obj, ward, pop, part, demo):
    obj["Ward {} Pop Count".format(ward)] = pop
    obj["Ward {} Part Count".format(ward)] = part
    totals = [wt for wt in ward_totals if wt["ward"] == ward][0]["totals"]
    obj["Ward {} Pop Perc".format(ward)] = pop / totals[demo]["pop"]
    obj["Ward {} Part Perc".format(ward)] = part / totals[demo]["part"]

# computes total pop and part for given ward 
# (treating each demographic variable separately since these aren't similated jointly)
def compute_totals(ward, race_df, edu_df, income_df):
    curr_race_df = race_df[race_df["ward"] == ward]
    curr_edu_df = edu_df[edu_df["ward"] == ward]
    curr_income_df = income_df[income_df["ward"] == ward]
    return {
        "race": {
            "pop": curr_race_df["pop"].sum(),
            "part": curr_race_df["part"].sum()
        },
        "educ": {
            "pop": curr_edu_df["pop"].sum(),
            "part": curr_edu_df["part"].sum()
        },
        "income": {
            "pop": curr_income_df["pop"].sum(),
            "part": curr_income_df["part"].sum()
        }
    }

# format labels
def format_race(r):
    if (r == "black"):
        return "Black or African American"
    elif (r == "latino"):
        return "Hispanic or Latino/a"
    else:
        return r.capitalize()
    
def format_income(i):
    if (i.startswith("less")):
        return "Less than $10,000"
    elif (i.endswith("more")):
        return "More than $150,000"
    else:
        label =  i.replace(" ", "")
        idx = label.index("-")
        return "$" + label[:idx + 1] + "$" + label[idx + 1:]
    
# sort table entries by demographic categories
def sort_by(table, demo):
    table[demo].sort(key=lambda x: SORT_ORDERS[demo][x["category"]])


## main
# load count data
race_df = pd.read_csv("participation_simulation/race.csv")
edu_df = pd.read_csv("participation_simulation/educ.csv")
income_df = pd.read_csv("participation_simulation/income.csv")

# compute normalizing totals per ward
for wd in ward_totals:
    wd["totals"] = compute_totals(wd["ward"], race_df, edu_df, income_df)

# construct race table
race_categories = race_df["race"].unique()
for r in race_categories:
    curr_obj = {"category": format_race(r)}
    curr_df = race_df[race_df["race"] == r]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"], "race"), axis = 1)
    table_data["race"].append(curr_obj)

sort_by(table_data, "race")

# construct income table
income_categories = income_df["income_cohort"].unique()
for i in income_categories:
    curr_obj = {"category": format_income(i)}
    curr_df = income_df[income_df["income_cohort"] == i]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"], "income"), axis = 1)
    table_data["income"].append(curr_obj)

sort_by(table_data, "income")

# construct edu table
edu_categories = edu_df["education"].unique()
for e in edu_categories:
    curr_obj = {"category": e.capitalize()}
    curr_df = edu_df[edu_df["education"] == e]
    curr_df.apply(lambda row: append_entry(curr_obj, row["ward"], row["pop"], row["part"], "educ"), axis = 1)
    table_data["educ"].append(curr_obj)

sort_by(table_data, "educ")

# print(table_data)
with open("demo_table_data.json","w") as f:
    json.dump(table_data, f)
