class CannotAutoGenerate(Exception):
    pass


class QuestionExists(CannotAutoGenerate):
    def __init__(self, msg='question with same type already exists',
                 *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


MAX_MC_CHOICE_NUM = 10
MIN_MC_CHOICE_NUM = 5
MAX_RANDOM_CHOICE_NUM = 20
