# see https://www.youtube.com/watch?v=x3lypVnJ0HM&t=371s&ab_channel=MemeableData
from simulation import *
from utils import *
import plotly.express as px
import pandas as pd

AMOUNT_SIMULATIONS = 1


average_amount_of_likes_male = 0
average_amount_of_likes_female = 0
average_amount_of_matches_male = 0
average_amount_of_matches_female = 0

simulations = []
for i in range(AMOUNT_SIMULATIONS):
    print(i)
    sim = Simulation(500, 500, 100, 100)
    sim.run_sim()
    simulations.append(sim)

    average_amount_of_likes_male += sim.get_average_number_of_likes_received_by_sex(SEX_MALE)
    average_amount_of_likes_female += sim.get_average_number_of_likes_received_by_sex(SEX_FEMALE)
    average_amount_of_matches_male += sim.get_average_number_of_matches_by_sex(SEX_MALE)
    average_amount_of_matches_female += sim.get_average_number_of_matches_by_sex(SEX_FEMALE)

average_amount_of_likes_male = average_amount_of_likes_male / AMOUNT_SIMULATIONS
average_amount_of_likes_female = average_amount_of_likes_female / AMOUNT_SIMULATIONS
average_amount_of_matches_male = average_amount_of_matches_male / AMOUNT_SIMULATIONS
average_amount_of_matches_female = average_amount_of_matches_female / AMOUNT_SIMULATIONS


print("")
print(f"Average amount of likes (male): {average_amount_of_likes_male}")
print(f"Average amount of likes (female): {average_amount_of_likes_female}")
print("")
print(f"Average amount of matches (male): {average_amount_of_matches_male}")
print(f"Average amount of matches (female): {average_amount_of_matches_female}")

sim0 = simulations[0]


groups_men = pd.DataFrame(get_users_in_groups(sim0.list_of_men))
groups_men = groups_men.rename(columns={'average_amount': 'average_amount_men'})
groups_women = pd.DataFrame(get_users_in_groups(sim0.list_of_women))
groups_women = groups_women.rename(columns={'average_amount': 'average_amount_women'})

df = pd.concat([groups_men, groups_women["average_amount_women"]], axis=1, join="inner")

print(df)
# fig = px.bar(df, x="group_name", y=["average_amount_men", "average_amount_women"], barmode='group', title='x')
# fig.show()
