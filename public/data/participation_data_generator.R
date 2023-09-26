library(tidyverse)

pivot_and_uncount = function(df, var_name, val_name) {
  long_df = df %>% 
    dplyr::select({{var_name}}, {{val_name}}) %>%
    pivot_longer(cols = c({{val_name}}), names_to = c("ward"), values_to = "count") %>%
    rowwise() %>%
    mutate(ward = as.numeric(substr(ward, 6, 7)))
  
  long_df$ward = long_df$ward[2]
  
  long_df = long_df %>% 
    group_by({{var_name}}, ward) %>%
    uncount(count)
}

sample_participants = function(long_df, prop) {
  sample <- long_df %>%
    sample_frac(prop) # some percent of ward participating
}


## education data
edu_df <- read_csv("./source/educ.csv")

# ward 29
ward29_edu = pivot_and_uncount(edu_df, education, ward_29_educ)
ward29_edu_sample = sample_participants(ward29_edu, 0.05)

# ward 35
ward35_edu = pivot_and_uncount(edu_df, education, ward_35_educ)
ward35_edu_sample = sample_participants(ward35_edu, 0.06)

# ward 36
ward36_edu = pivot_and_uncount(edu_df, education, ward_36_educ)
ward36_edu_sample = sample_participants(ward36_edu, 0.05)

# ward 49
ward49_edu = pivot_and_uncount(edu_df, education, ward_49_educ)
ward49_edu_sample = sample_participants(ward49_edu, 0.07)

# combine wards into one table
educ_sample = rbind(ward29_edu_sample, ward35_edu_sample, ward36_edu_sample, ward49_edu_sample)

educ_sample = educ_sample %>% # this is our sample
  group_by(education, ward) %>%
  summarise(
    count = n()
  )

educ <- rbind(ward29_edu, ward35_edu, ward36_edu, ward49_edu)

educ <- educ %>% 
  group_by(education, ward) %>%
  summarise(
    count = n()
  )

educ = educ %>% 
  left_join(educ_sample, by = c("education", "ward")) %>%
  rename(
    pop = count.x,
    part = count.y
  )

# output
write.csv(educ, "./participation_simulation/educ.csv", row.names = FALSE)


## income data
income_df <- read_csv("./source/income_cohort.csv")

# ward 29
ward29_income = pivot_and_uncount(income_df, income_cohort, ward_29_income)
ward29_income_sample = sample_participants(ward29_income, 0.05)

# ward 35
ward35_income = pivot_and_uncount(income_df, income_cohort, ward_35_income)
ward35_income_sample = sample_participants(ward35_income, 0.06)

# ward 36
ward36_income = pivot_and_uncount(income_df, income_cohort, ward_36_income)
ward36_income_sample = sample_participants(ward36_income, 0.05)

# ward 49
ward49_income = pivot_and_uncount(income_df, income_cohort, ward_49_income)
ward49_income_sample = sample_participants(ward49_income, 0.07)

# combine wards into one table
income_sample = rbind(ward29_income_sample, ward35_income_sample, ward36_income_sample, ward49_income_sample)

income_sample = income_sample %>% # this is our sample
  group_by(income_cohort, ward) %>%
  summarise(
    count = n()
  )

income <- rbind(ward29_income, ward35_income, ward36_income, ward49_income)

income <- income %>% 
  group_by(income_cohort, ward) %>%
  summarise(
    count = n()
  )

income = income %>% 
  left_join(income_sample, by = c("income_cohort", "ward")) %>%
  rename(
    pop = count.x,
    part = count.y
  )

# output
write.csv(income, "./participation_simulation/income.csv", row.names = FALSE)


## race data
race_df <- read_csv("./source/race.csv")

# ward 29
ward29_race = pivot_and_uncount(race_df, race, ward_29)
ward29_race_sample = sample_participants(ward29_race, 0.05)

# ward 35
ward35_race = pivot_and_uncount(race_df, race, ward_35)
ward35_race_sample = sample_participants(ward35_race, 0.06)

# ward 36
ward36_race = pivot_and_uncount(race_df, race, ward_36)
ward36_race_sample = sample_participants(ward36_race, 0.05)

# ward 49
ward49_race = pivot_and_uncount(race_df, race, ward_49)
ward49_race_sample = sample_participants(ward49_race, 0.07)

# combine wards into one table
race_sample = rbind(ward29_race_sample, ward35_race_sample, ward36_race_sample, ward49_race_sample)

race_sample = race_sample %>% # this is our sample
  group_by(race, ward) %>%
  summarise(
    count = n()
  )

race <- rbind(ward29_race, ward35_race, ward36_race, ward49_race)

race <- race %>% 
  group_by(race, ward) %>%
  summarise(
    count = n()
  )

race = race %>% 
  left_join(race_sample, by = c("race", "ward")) %>%
  rename(
    pop = count.x,
    part = count.y
  )

# output
write.csv(race, "./participation_simulation/race.csv", row.names = FALSE)
