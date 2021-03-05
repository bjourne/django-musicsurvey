from django.conf import settings

MUSICSURVEY_CLIP_ROOT = \
    getattr(settings, 'MUSICSURVEY_CLIP_ROOT', '/tmp/serve-dir')
MUSICSURVEY_CLIPS_PER_SURVEY = \
    getattr(settings, 'MUSICSURVEY_CLIPS_PER_SURVEY', 5)
