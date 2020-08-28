from datetime import timedelta

class Constants:
    DEFAULT_IN_A_ROW_REQUIRED = 2
    MAX_IN_A_ROW_REQUIRED = 4
    ADDED_DURATION = timedelta(seconds=30)
    MIN_UC_IN_PROGRESS_CNT = 3
    MAX_UC_IN_PROGRESS_CNT = 10
    LEARN_PROB = 1 / 3
