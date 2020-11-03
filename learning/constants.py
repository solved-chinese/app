from datetime import timedelta

# algorithm constants
MAX_INTERVAL_SECONDS = 120
DEFAULT_IN_A_ROW_REQUIRED = 2 # overridden by each ability
MAX_IN_A_ROW_REQUIRED = 2 # overridden by each ability
ADDED_DURATION = timedelta(seconds=30)
MIN_SC_IN_PROGRESS_CNT = 3
MAX_SC_IN_PROGRESS_CNT = 8
LEARN_PROB = 0.3
MAX_RANDOM_CHOICES = 20