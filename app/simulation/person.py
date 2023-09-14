SEX_MALE = 1
SEX_FEMALE = 2

DICT_KEY_OBJECT_ID = "object_id"
DICT_KEY_SEX = "sex"
DICT_KEY_ATTRACTIVENESS = "attractiveness"
DICT_KEY_AMOUNT_LIKES_GIVEN = "amount_likes_given"
DICT_KEY_AMOUNT_LIKES_RECEIVED = "amount_likes_received"
DICT_KEY_AMOUNT_MATCHES = "amount_matches"


def get_opposite_sex(sex):
    """Gets the opposite sex.
       If male (1) is given, female is returned (2). If female (2) is given, male (1) is returned.
    """
    if sex == SEX_MALE:
        return SEX_FEMALE
    elif sex == SEX_FEMALE:
        return SEX_MALE
    else:
        raise ValueError


class User:
    def __init__(self, sex, attractiveness, max_amount_of_likes):
        """Creates a new instance of User. This class represents a user / profile in a dating app.

        Args:
            sex:                    The sex of the user.
            attractiveness:         The attractiveness. Should be a value from 0 tp 100.
            max_amount_of_likes:    The amount of profiles this user can like.
                                    If None, they have endless likes.
        """
        self.sex = sex
        self.attractiveness = attractiveness
        self.amount_of_likes_available = max_amount_of_likes
        self.likes_given = []       # this will contain references to other users that have been liked
        self.likes_received = []    # this will contain references to other users that gave this one a like
        self.amount_matches = 0

    def like_profile(self, user):
        # if self.amount_of_likes_available is None, the user has unlimited likes
        # otherwise check if there are some likes left
        if self.amount_of_likes_available is None or self.amount_of_likes_available > 0:
            self.likes_given.append(user)
            user.likes_received.append(self)
            if self.amount_of_likes_available is not None:
                self.amount_of_likes_available -= 1

    def calculate_amount_of_matches(self):
        for user_liked in self.likes_given:
            for user_like_received in self.likes_received:
                if user_liked == user_like_received:
                    self.amount_matches += 1

    def to_dict(self):
        """Returns this user in a dictionary. Can be used for creating a dataframe.
        """
        return {
            DICT_KEY_OBJECT_ID: id(self),
            DICT_KEY_SEX: self.sex,
            DICT_KEY_ATTRACTIVENESS: round(self.attractiveness, 4),
            DICT_KEY_AMOUNT_LIKES_GIVEN: len(self.likes_given),
            DICT_KEY_AMOUNT_LIKES_RECEIVED: len(self.likes_received),
            DICT_KEY_AMOUNT_MATCHES: self.amount_matches
        }
