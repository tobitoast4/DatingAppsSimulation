MAX_AMOUNT_OF_USERS_PER_SEX = 1000000
MIN_AMOUNT_OF_USERS_PER_SEX = 1
MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE = 0
MIN_AMOUNT_OF_LIKES = 0


def check_inputs_for_errors(amount_of_men, amount_of_women, amount_of_women_a_man_will_see, amount_of_men_a_woman_will_see, max_amount_of_likes_for_men, max_amount_of_likes_for_women):
    errors = []
    if amount_of_men is None or amount_of_men > MAX_AMOUNT_OF_USERS_PER_SEX or amount_of_men < MIN_AMOUNT_OF_USERS_PER_SEX:
        errors.append(f"The amount of men in the simulation must be between {MIN_AMOUNT_OF_USERS_PER_SEX} and {MAX_AMOUNT_OF_USERS_PER_SEX}.")
    else:
        if amount_of_men_a_woman_will_see is None or amount_of_men_a_woman_will_see > amount_of_men or amount_of_men_a_woman_will_see < MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE:
            errors.append(f"The amount of men a woman will see in the simulation must be between {MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE} and your input {amount_of_men}.")
    if amount_of_women is None or amount_of_women > MAX_AMOUNT_OF_USERS_PER_SEX or amount_of_women < MIN_AMOUNT_OF_USERS_PER_SEX:
        errors.append(f"The amount of women in the simulation must be between {MIN_AMOUNT_OF_USERS_PER_SEX} and {MAX_AMOUNT_OF_USERS_PER_SEX}.")
    else:
        if amount_of_women_a_man_will_see is None or amount_of_women_a_man_will_see > amount_of_women or amount_of_women_a_man_will_see < MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE:
            errors.append(f"The amount of women a man will see in the simulation must be between {MIN_AMOUNT_OF_OTHER_USERS_ONE_USER_WILL_SEE} and your input {amount_of_women}.")
    if max_amount_of_likes_for_men is not None and max_amount_of_likes_for_men < 0:
        errors.append("The maximum amount of likes for men can not be negative. Leave emtpy for unlimited likes.")
    if max_amount_of_likes_for_women is not None and max_amount_of_likes_for_women < 0:
        errors.append("The maximum amount of likes for women can not be negative. Leave emtpy for unlimited likes.")
    return "<br>".join(errors)
