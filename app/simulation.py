import random
from person import *

AMOUNT_MEN = 200
AMOUNT_WOMEN = 100


def like_current_profile_random(probability_rate):
    number = random.randint(0, 99)
    return number < probability_rate


class Simulation:
    def __init__(self):
        self.list_of_men = []
        step_size = 1/AMOUNT_MEN
        for i in range(AMOUNT_MEN):
            attractivity = ((step_size * (i+1)) ** 6.14) * 100
            print(f"A: {attractivity}")
            print(f"B: ", end="")
            print(eval(f"(({step_size} * (i+1)) ** 6.14) * 100"))
            print()
            self.list_of_men.append(User(SEX_MALE, attractivity))

        self.list_of_women = []
        step_size = 1/AMOUNT_WOMEN
        for i in range(AMOUNT_WOMEN):
            attractivity = ((step_size * (i+1)) ** 1.17) * 100
            self.list_of_women.append(User(SEX_FEMALE, attractivity))

    def get_random_list_of_100_users_by_sex(self, sex):
        if sex == SEX_MALE:
            return random.sample(self.list_of_men, 100)
        elif sex == SEX_FEMALE:
            return random.sample(self.list_of_women, 100)
        else:
            raise ValueError

    def get_users_by_sex(self, sex):
        if sex == SEX_MALE:
            return self.list_of_men
        elif sex == SEX_FEMALE:
            return self.list_of_women
        else:
            raise ValueError

    def run_like_process_for_sex(self, sex):
        opposite_sex = get_opposite_sex(sex)
        for current_user in self.get_users_by_sex(sex):
            subset_of_other_users = self.get_random_list_of_100_users_by_sex(opposite_sex)
            for current_profile in subset_of_other_users:
                like_probability = current_profile.attractivity
                # like_probability = 14
                # if sex == SEX_MALE:
                #     like_probability = 46
                if like_current_profile_random(like_probability):
                    current_user.like_profile(current_profile)

    def get_average_number_of_likes_received_by_sex(self, sex):
        users = self.get_users_by_sex(sex)
        amount_likes_total_for_sex = 0
        for user in users:
            amount_likes_total_for_sex = amount_likes_total_for_sex + len(user.likes_received)
        return amount_likes_total_for_sex / len(users)

    def get_average_number_of_matches_by_sex(self, sex):
        users = self.get_users_by_sex(sex)
        amount_matches_total_for_sex = 0
        for user in users:
            amount_matches_total_for_sex = amount_matches_total_for_sex + user.amount_matches
        return amount_matches_total_for_sex / len(users)

    def run_sim(self):
        self.run_like_process_for_sex(SEX_MALE)
        self.run_like_process_for_sex(SEX_FEMALE)

        for user in self.list_of_men + self.list_of_women:
            user.calculate_amount_of_matches()
