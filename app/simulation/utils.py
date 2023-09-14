import pandas as pd
from simulation.person import DICT_KEY_OBJECT_ID


def get_distribution(sim, dict_key, granularity):
    groups_men = pd.DataFrame(get_users_in_groups(sim.list_of_men, dict_key, granularity))
    groups_men = groups_men.rename(columns={'average_amount': 'men'})
    groups_men = groups_men.rename(columns={'user_ids': 'user_ids_of_men'})
    groups_women = pd.DataFrame(get_users_in_groups(sim.list_of_women, dict_key, granularity))
    groups_women = groups_women.rename(columns={'average_amount': 'women'})
    groups_women = groups_women.rename(columns={'user_ids': 'user_ids_of_women'})
    groups_women = groups_women.drop(['group_name'], axis=1)  # the column group_name is only needed once
    return pd.concat([groups_men, groups_women], axis=1, join="inner")


def get_users_in_groups(list_of_users, dict_key, granularity):
    list_length = len(list_of_users)
    list_of_men_data = [user.to_dict() for user in list_of_users]
    list_of_users_data_sorted = sorted(list_of_men_data, key=lambda user: user[dict_key])

    amount_of_users_in_group = len(list_of_users_data_sorted) / granularity

    groups = []
    for g in range(granularity):
        min_index = round(g * amount_of_users_in_group)
        max_index = round((g + 1) * amount_of_users_in_group)
        current_group_amount_total = 0
        user_ids = []
        for index in range(min_index, max_index):
            user = list_of_users_data_sorted[index]
            current_group_amount_total += user[dict_key]
            user_ids.append(user[DICT_KEY_OBJECT_ID])
        groups.append({
            "group_name": f"{round(min_index / list_length * 100)} - {round(max_index / list_length * 100)}",
            "average_amount": current_group_amount_total / (max_index - min_index),
            "user_ids": user_ids
        })
    return groups


def parse_equation(equation):
    equation = equation.replace("^", "**")
    equation = equation.replace("sin", "math.sin")
    equation = equation.replace("cos", "math.cos")
    equation = equation.replace("tan", "math.tan")
    equation = equation.replace("asin", "math.asin")
    equation = equation.replace("acos", "math.acos")
    equation = equation.replace("atan", "math.atan")
    equation = equation.replace("sqrt", "math.sqrt")
    equation = equation.replace("PI", "math.pi")   # allow
    equation = equation.replace("Pi", "math.pi")   # all
    equation = equation.replace("pi", "math.pi")   # three
    equation = equation.replace("e", "math.e")
    equation = equation.replace("log2", "math.log2")
    equation = equation.replace("abs", "math.fabs")
    return equation
