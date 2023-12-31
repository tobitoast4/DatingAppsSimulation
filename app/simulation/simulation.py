import sys
import random
import time
import datetime
import math  # do not remove (this is used for eval() )
from simulation.person import *


def like_current_profile_random(probability_rate):
    number = random.randint(0, 99)
    return number < probability_rate


class Simulation:
    def __init__(self, amount_men, amount_women, amount_women_seen_by_one_man, amount_men_seen_by_one_woman,
                 max_amount_of_likes_of_one_man, max_amount_of_likes_of_one_woman, formula_for_men_attractiveness,
                 formula_for_women_attractiveness):
        """Creates a new instance of Simulation.

        Args:
            amount_men:                         The amount of men there will be in the simulation.
            amount_women:                       The amount of women there will be in the simulation.
            amount_women_seen_by_one_man:       The amount of women a man will see in the simulation.
                                                E.g.: If set to 100, one man can swipe 100 profiles left or right.
            amount_men_seen_by_one_woman:       The amount of men a woman will see in the simulation.
            max_amount_of_likes_of_one_man:     The maximum amount of like one man has.
                                                If set to None, he will have unlimited likes.
            max_amount_of_likes_of_one_woman:   The maximum amount of like one woman has.
                                                If set to None, she will have unlimited likes.
            formula_for_men_attractiveness:     The formula to determine the attractiveness for men. The attractiveness
                                                for each single man will follow this formula. Should be parsed already.
                                                -> Means x^6.14 should already be written in pythonic way (as x**6.14).
                                                -> See ./utils.py -> parse_equation()
            formula_for_women_attractiveness:   The formula to determine the attractiveness for women.
        """
        self.amount_men = amount_men
        self.amount_women = amount_women
        self.amount_women_seen_by_one_man = amount_women_seen_by_one_man
        self.amount_men_seen_by_one_woman = amount_men_seen_by_one_woman
        self.max_amount_of_likes_of_one_man = max_amount_of_likes_of_one_man
        self.max_amount_of_likes_of_one_woman = max_amount_of_likes_of_one_woman
        self.formula_for_men_attractivity = formula_for_men_attractiveness
        self.formula_for_women_attractivity = formula_for_women_attractiveness
        # progress_to_reach is set to (AMOUNT_MEN + AMOUNT_WOMEN) * 3 as all users will be iterated 3 times:
        # once for creating, once every user will swipe and once for calculating the matches
        self.progress = Progress((self.amount_men + self.amount_women) * 3)
        self.list_of_men = []
        self.list_of_women = []

        self.timestamp_started = datetime.datetime.now()
        self.timestamp_finished = None
        self.latest_error = None

    def get_random_sample_of_users_by_sex(self, sex):
        """Gets a random sample of users of one sex. The size of the sample depends on
           self.amount_men_seen_by_one_woman / self.amount_women_seen_by_one_man.
        """
        if sex == SEX_MALE:
            return random.sample(self.list_of_men, self.amount_men_seen_by_one_woman)
        elif sex == SEX_FEMALE:
            return random.sample(self.list_of_women, self.amount_women_seen_by_one_man)
        else:
            raise ValueError

    def get_users_by_sex(self, sex):
        """Gets all the users of one sex in the simulation.
        """
        if sex == SEX_MALE:
            return self.list_of_men
        elif sex == SEX_FEMALE:
            return self.list_of_women
        else:
            raise ValueError

    def run_like_process_for_sex(self, sex):
        """Runs the like process for all users of one sex by iterating all these users and
           letting each of them swipe through the given amount of profiles.
        """
        opposite_sex = get_opposite_sex(sex)
        for current_user in self.get_users_by_sex(sex):
            self.progress.increase_progress()
            subset_of_other_users = self.get_random_sample_of_users_by_sex(opposite_sex)
            for current_profile in subset_of_other_users:
                like_probability = current_profile.attractiveness
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

    def get_users_by_ids(self, user_ids):
        """Gets all users by id.

        Args:
            user_ids: A set of user ids. All users with their id within this set will be returned.
        """
        filtered_users = []
        users = [user.to_dict() for user in self.list_of_men + self.list_of_women]
        for user in users:
            if user[DICT_KEY_OBJECT_ID] in user_ids:
                filtered_users.append(user)
        return filtered_users

    def run_sim(self, time_sleep):
        """Runs the simulation. That includes creating all male and female users with their attractiveness level,
           swiping the profiles and calculating the matches. In between the status of the progress of the simulation
           will also be updated.

        Args:
            time_sleep: Can be used to show the progress bar for a short amount of time.

        Raises:
            SyntaxError / Exception.
        """
        try:
            self.progress.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_1
            time.sleep(time_sleep)
            step_size = 1/self.amount_men
            for i in range(self.amount_men):
                current_x = f"({step_size} * (i+1))"
                formula = self.formula_for_men_attractivity.replace("x", current_x)
                attractiveness = float(eval(formula)) * 100
                self.list_of_men.append(User(SEX_MALE, attractiveness, self.max_amount_of_likes_of_one_man))
                self.progress.increase_progress()

            step_size = 1/self.amount_women
            for i in range(self.amount_women):
                current_x = f"({step_size} * (i+1))"
                formula = self.formula_for_women_attractivity.replace("x", current_x)
                attractiveness = float(eval(formula)) * 100
                self.list_of_women.append(User(SEX_FEMALE, attractiveness, self.max_amount_of_likes_of_one_woman))
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
            self.timestamp_finished = datetime.datetime.now()
        except SyntaxError:
            self.latest_error = f"{sys.exc_info()[1].args[0]} in <br><br>" \
                                f"{sys.exc_info()[1].args[1][3]} <br><br> " \
                                f"This character might cause the error: " \
                                f"{sys.exc_info()[1].args[1][3][(sys.exc_info()[1].args[1][2])-1]}"
        except Exception as e:
            self.latest_error = str(e)


PROGRESS_STATE_TEXT_STATUS_0 = "Simulation not started"
PROGRESS_STATE_TEXT_STATUS_1 = "Starting simulation ..."
PROGRESS_STATE_TEXT_STATUS_2 = "Men are swiping ..."
PROGRESS_STATE_TEXT_STATUS_3 = "Women are swiping ..."
PROGRESS_STATE_TEXT_STATUS_4 = "Calculating matches ..."
PROGRESS_STATE_TEXT_STATUS_5 = "Simulation succeeded"


class Progress:
    def __init__(self, progress_to_reach):
        """Creates a new instance of Progress.

        Args:
            progress_to_reach:    Amount of processing cycles to be done. Simple example:
                                  Download of files from website. Downloading a file could be seen as one processing
                                  cycle. self.progress_to_reach should be set to this amount of files. After a
                                  processing cycle is done, current_progress should be increased.
        """
        self.progress_to_reach = progress_to_reach
        self.current_progress = 0
        self.current_progress_status_text = PROGRESS_STATE_TEXT_STATUS_0  # the initial text

    def increase_progress(self):
        self.current_progress += 1

    def current_progress_in_percent(self):
        return round(self.current_progress / self.progress_to_reach * 100)
