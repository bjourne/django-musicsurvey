from django.conf import settings

# Number of pairs each survey respondent has to rate.
MUSICSURVEY_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_CLIPS_PER_SURVEY', 6)

# Number of pairs per survey that contain one random clip. Used for
# control.
MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_RANDOM_CLIPS_PER_SURVEY', 0)

# Number of pairs per survey that contains a human-composed clip.
MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY', 3)
