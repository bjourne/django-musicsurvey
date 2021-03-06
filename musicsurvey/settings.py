from django.conf import settings

MUSICSURVEY_CLIPS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_CLIPS_PER_SURVEY', 5)
