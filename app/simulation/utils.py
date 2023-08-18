from app.simulation.person import *
import pandas as pd


def get_distribution_amount_likes_received(sim):
    return get_distribution(sim, DICT_KEY_AMOUNT_LIKES_RECEIVED)


def get_distribution_amount_matches(sim):
    return get_distribution(sim, DICT_KEY_AMOUNT_MATCHES)


def get_distribution(sim, dict_key):
    groups_men = pd.DataFrame(get_users_in_groups(sim.list_of_men, dict_key))
    groups_men = groups_men.rename(columns={'average_amount': 'men'})
    groups_women = pd.DataFrame(get_users_in_groups(sim.list_of_women, dict_key))
    groups_women = groups_women.rename(columns={'average_amount': 'women'})
    return pd.concat([groups_men, groups_women["women"]], axis=1, join="inner")


def get_users_in_groups(list_of_users, dict_key):
    list_length = len(list_of_users)
    list_of_men_data = [man.to_dict() for man in list_of_users]
    list_of_users_data_sorted = sorted(list_of_men_data, key=lambda user: user[dict_key])
    granularity = 10

    amount_of_users_in_group = len(list_of_users_data_sorted) / granularity

    groups = []
    for g in range(granularity):
        min_index = round(g * amount_of_users_in_group)
        max_index = round((g + 1) * amount_of_users_in_group)
        current_group_amount_total = 0
        for index in range(min_index, max_index):
            current_group_amount_total += list_of_users_data_sorted[index][dict_key]
        groups.append({
            "group_name": f"{round(min_index / list_length * 100)} - {round(max_index / list_length * 100)}",
            "average_amount": current_group_amount_total / (max_index - min_index),
        })
    return groups
