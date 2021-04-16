from django.conf import settings

# Number of pairs each survey respondent has to rate.
MUSICSURVEY_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_PAIRS_PER_SURVEY', 2)

# Number of pairs per survey that contain one random clip. Used for
# control.
MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY', 0)

# Number of pairs per survey that contains a human-composed clip.
MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY', 1)

# The clips' file type
MUSICSURVEY_FILE_TYPE = \
    getattr(settings, 'MUSICSURVEY_FILE_TYPE', 'mid')

# Human-readable names of the composers
MUSICSURVEY_COMPOSER_NAMES = \
    getattr(settings, 'MUSICSURVEY_COMPOSER_NAMES', {})

# Whether both composers submit the same composition in
# duels. Generally preferable if the number of clips is large.
MUSICSURVEY_SAME_COMPOSITIONS = \
    getattr(settings, 'MUSICSURVEY_SAME_COMPOSITIONS', True)
