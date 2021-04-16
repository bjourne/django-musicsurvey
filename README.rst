============
Music Survey
============

Music Survey is a Django app for creating simple musical preference
surveys. To add it to your site,

* Add `'musicsurvey.apps.MusicSurveyConfig'` to `INSTALLED_APPS` in
  `settings.py`.
* Add `path('musicsurvey/', include('musicsurvey.urls'))` (or
  whichever root path you prefer) to `urlpatterns` in `urls.py`.
* Run `python manage.py migrate`

* Configure `STATICFILES_DIRS` in `settings.py` to the path where
  clips should be stored. It needs to use the prefix
  "musicsurvey". For example, if the clips are to be stored in
  /some/path/, set `STATICFILES_DIRS` to:
  ```
  STATICFILES_DIRS = [
    ('musicsurvey', BASE_DIR / "clips")
  ]
  ```
