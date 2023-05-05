from django import template
from django.conf import settings
from musicsurvey import settings as ms_settings

register = template.Library()

@register.filter(name = 'humanize_model')
def humanize_model(s):
    v = ms_settings.MUSICSURVEY_COMPOSER_NAMES[s]
    if isinstance(v, tuple) and len(v) == 2:
        return v[0]
    return 'clip composed by %s' % v

@register.filter(name = 'clips_static_url')
def clips_static_url(clip):
    fmt = '%smusicsurvey/%s.%s'
    return fmt % (settings.STATIC_URL, clip.random_name,
                  ms_settings.MUSICSURVEY_FILE_TYPE)
