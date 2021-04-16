# django-musicsurvey

django-musicsurvey is a Django app for creating simple musical
preference surveys.

## Design

The idea behind django-musicsurvey is to rank a relatively small group
of composers based on what they compose. The composers can be humans,
computer algorithms, or whatever. Each composer outputs a number of
clips - short musical performances. Humans then judge random pairs of
clips and they select the clip they prefer. One can think of the
composers "battling" each other. The composer that wins the most is
the best one.

You can find a demo of django-musicsurvey here,
https://modmusicgen.com/, where it is used to rate generative music
models.

## Configuration

To use django-musicsurvey on your site, add the following to
`settings.py`:

* Add `'musicsurvey.apps.MusicSurveyConfig'` to `INSTALLED_APPS`.
* Add a path to `STATICFILES_DIRS` for storing user-accesible clips. For
  example, if the clips are stored in /some/path/, set
  `STATICFILES_DIRS` to:
  ```
  STATICFILES_DIRS = [ ('musicsurvey', "/some/path") ]
  ```
  This directory should initially be empty.
* Configure `MUSICSURVEY_FILE_TYPE` based on the type of your clips;
  "mp3" for MP3, "mid" for MIDI and so on:
  ```
  MUSICSURVEY_FILE_TYPE = 'mp3'
  ```
* Configure `MUSICSURVEY_COMPOSER_NAMES` so that it maps between
  composer names in filenames and "human-reable names" (see section
  Clip Import below):
  ```
  MUSICSURVEY_COMPOSER_NAMES = {
    'student1' : 'Student 1',
    'student2' : 'Student 2',
    'john' : 'John Williams',
    ...
  }
  ```

Add the following to `urls.py`:

* `path('musicsurvey/', include('musicsurvey.urls'))` (or
    whichever root path you prefer) to `urlpatterns`.

Then initialize the database with

    python manage.py makemigrations musicsurvey
    python manage.py migrate

## Clip Import

Your clip collection must be stored in a single directory and the
names of all clips must adhere to the following format:

    <composition>__<composer>__<misc>.<filetype>

"Composition" should contain information about what the composition
is, "composer" about what composed it, misc can be any useful data and
"filetype" should match `MUSICSURVEY_FILE_TYPE`. For example, the
names of clips of renditions of classical music could have the
following names:

    bach-bmw974__student1__jan4.mp3
    bach-bmw974__student2__feb3.mp3
    mozart-no21__student1__jan4.mp3
    mozart-no21__john__dec22.mp3
    ...

Note that these names should match what you configured in
`MUSICSURVEY_COMPOSER_NAMES`.

Import clips from this directory using:

    python manage.py importsongs collection --delete-existing

`--delete-existing` is optional and purges the database before import.
