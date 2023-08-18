SEX_MALE = 1
SEX_FEMALE = 2

DICT_KEY_OBJECT_ID = "object_id"
DICT_KEY_SEX = "sex"
DICT_KEY_AMOUNT_LIKES_GIVEN = "amount_likes_given"
DICT_KEY_AMOUNT_LIKES_RECEIVED = "amount_likes_received"
DICT_KEY_AMOUNT_MATCHES = "amount_matches"


def get_opposite_sex(sex):
    if sex == SEX_MALE:
        return SEX_FEMALE
    elif sex == SEX_FEMALE:
        return SEX_MALE
    else:
        raise ValueError


class User:
    def __init__(self, sex, attractivity):
        self.sex = sex
        self.attractivity = attractivity
        self.likes_given = []
        self.likes_received = []
        self.amount_matches = 0

    def like_profile(self, user):
        self.likes_given.append(user)
        user.likes_received.append(self)

    def calculate_amount_of_matches(self):
        for user_liked in self.likes_given:
            for user_like_received in self.likes_received:
                if user_liked == user_like_received:
                    self.amount_matches += 1

    def to_dict(self):
        return {
            DICT_KEY_OBJECT_ID: id(self),
            DICT_KEY_SEX: self.sex,
            DICT_KEY_AMOUNT_LIKES_GIVEN: len(self.likes_given),
            DICT_KEY_AMOUNT_LIKES_RECEIVED: len(self.likes_received),
            DICT_KEY_AMOUNT_MATCHES: self.amount_matches
        }

    def print(self):
        print(f"User (sex: {self.sex}; likes given: {len(self.likes_given)}; likes received: {len(self.likes_received)}; self: {self})")
