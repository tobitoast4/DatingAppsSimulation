from person import *


def get_users_in_groups(list_of_users):
    list_length = len(list_of_users)
    list_of_men_data = [man.to_dict() for man in list_of_users]
    list_of_users_data_sorted = sorted(list_of_men_data, key=lambda user: user[DICT_KEY_AMOUNT_LIKES_RECEIVED])
    granularity = 10

    amount_of_users_in_group = len(list_of_users_data_sorted) / granularity

    groups = []
    for g in range(granularity):
        min_index = round(g * amount_of_users_in_group)
        max_index = round((g + 1) * amount_of_users_in_group)
        current_group_amount_total = 0
        for index in range(min_index, max_index):
            current_group_amount_total += list_of_users_data_sorted[index][DICT_KEY_AMOUNT_LIKES_RECEIVED]
        groups.append({
            "group_name": f"{round(min_index / list_length * 100)} - {round(max_index / list_length * 100)}",
            "average_amount": current_group_amount_total / (max_index - min_index),
        })
    return groups
