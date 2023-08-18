import random
import time
from app.simulation.person import *


def like_current_profile_random(probability_rate):
    number = random.randint(0, 99)
    return number < probability_rate


class Simulation:
    def __init__(self, amount_men, amount_women, amount_men_seen_by_one_woman, amount_women_seen_by_one_man):
        self.amount_men = amount_men
        self.amount_women = amount_women
        self.amount_men_seen_by_one_woman = amount_men_seen_by_one_woman
        self.amount_women_seen_by_one_man = amount_women_seen_by_one_man
        # progress_to_reach is set to (AMOUNT_MEN + AMOUNT_WOMEN) * 3 as all users will be iterated 3 times:
        # once for creating, once every user will swipe and once for calculating the matches
        self.progress = Progress((self.amount_men + self.amount_women) * 3)
        self.list_of_men = []
        self.list_of_women = []

    def get_random_sample_of_users_by_sex(self, sex):
        if sex == SEX_MALE:
            return random.sample(self.list_of_men, self.amount_men_seen_by_one_woman)
        elif sex == SEX_FEMALE:
            return random.sample(self.list_of_women, self.amount_women_seen_by_one_man)
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
            self.progress.increase_progress()
            subset_of_other_users = self.get_random_sample_of_users_by_sex(opposite_sex)
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

    def get_median_number_of_likes_received_by_sex(self, sex):
        users = self.get_users_by_sex(sex)
        users_sorted = sorted(users, key=lambda user: len(user.likes_received))
        median_user = users_sorted[len(users_sorted) // 2]
        return len(median_user.likes_received)

    def get_average_number_of_matches_by_sex(self, sex):
        users = self.get_users_by_sex(sex)
        amount_matches_total_for_sex = 0
        for user in users:
            amount_matches_total_for_sex = amount_matches_total_for_sex + user.amount_matches
        return amount_matches_total_for_sex / len(users)

    def get_median_number_of_matches_by_sex(self, sex):
        users = self.get_users_by_sex(sex)
        users_sorted = sorted(users, key=lambda user: user.amount_matches)
        median_user = users_sorted[len(users_sorted) // 2]
        return median_user.amount_matches

    def run_sim(self, time_sleep):
        """
        :param time_sleep: Can be used to show the progress bar for a short amount of time.
        """
        self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_1
        time.sleep(time_sleep)
        step_size = 1/self.amount_men
        for i in range(self.amount_men):
            attractivity = ((step_size * (i+1)) ** 6.14) * 100
            # print(f"A: {attractivity}")
            # print(f"B: ", end="")
            # print(eval(f"(({step_size} * (i+1)) ** 6.14) * 100"))
            # print()
            attractivity = 25
            self.list_of_men.append(User(SEX_MALE, attractivity))
            self.progress.increase_progress()

        step_size = 1/self.amount_women
        for i in range(self.amount_women):
            attractivity = ((step_size * (i+1)) ** 1.17) * 100
            attractivity = 25
            self.list_of_women.append(User(SEX_FEMALE, attractivity))
            self.progress.increase_progress()

        self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_2
        self.run_like_process_for_sex(SEX_MALE)
        self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_3
        self.run_like_process_for_sex(SEX_FEMALE)

        self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_4
        for user in self.list_of_men + self.list_of_women:
            user.calculate_amount_of_matches()
            self.progress.increase_progress()
        self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_5


PROGRESS_STATE_TEXT_STATUS_0 = "Simulation not started"
PROGRESS_STATE_TEXT_STATUS_1 = "Starting simulation ..."
PROGRESS_STATE_TEXT_STATUS_2 = "Men are swiping ..."
PROGRESS_STATE_TEXT_STATUS_3 = "Women are swiping ..."
PROGRESS_STATE_TEXT_STATUS_4 = "Calculating matches ..."
PROGRESS_STATE_TEXT_STATUS_5 = "Simulation succeeded"


class Progress:
    def __init__(self, progress_to_reach):
        """
        progress_to_reach: Amount of processing cycles to be done. Simple example:
                          Download of files from website. Downloading a file could be seen as one processing
                          cycle. self.progress_to_reach should be set to this amount of files. After a
                          processing cycle is done, current_progress should be increased.
        """
        self.progress_to_reach = progress_to_reach
        self.current_progress = 0
        self.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_0

    def increase_progress(self):
        self.current_progress += 1

    def current_progress_in_percent(self):
        return round(self.current_progress / self.progress_to_reach * 100)
