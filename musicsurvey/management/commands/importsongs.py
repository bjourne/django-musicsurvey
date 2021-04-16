from django.conf import settings as dj_settings
from django.core.management.base import BaseCommand, CommandError
from musicsurvey import random_name
from musicsurvey import settings as ms_settings
from musicsurvey.models import *
from pathlib import Path
from shutil import copy, rmtree

def ensure_clip(stdout, src, clips_dir):
    parts = src.stem.split('__')
    offset = parts[0]
    gen_type = parts[1]
    if Clip.objects.filter(offset = offset, gen_type = gen_type).exists():
        return
    name = random_name()
    clip = Clip(name = name, offset = offset, gen_type = gen_type)
    clip.save()
    dst = clips_dir / ('%s.%s' % (name, ms_settings.MUSICSURVEY_FILE_TYPE))
    copy(str(src), str(dst))
    stdout.write('Importing %30s -> %10s.' % (src.stem, dst.stem))

class Command(BaseCommand):
    help = 'Import clips from a directory'

    def add_arguments(self, parser):
        parser.add_argument('import-dir', type = str)
        parser.add_argument(
            '--delete-existing', action = 'store_true',
            help = 'Delete existing clips before importing')

    def handle(self, *args, **opts):
        import_dir = Path(opts['import-dir'])

        clips_dir = [p for (prefix, p) in dj_settings.STATICFILES_DIRS
                     if prefix == 'musicsurvey']
        if not clips_dir:
            err = ('STATICFILES_DIRS must contains a directory '
                   'for storing clips.')
            raise ValueError(err)
        clips_dir = clips_dir[0]
        if opts['delete_existing']:
            Clip.objects.all().delete()
            Round.objects.all().delete()
            rmtree(clips_dir)
        clips_dir.mkdir(exist_ok = True, parents = True)
        glob = '*.%s' % ms_settings.MUSICSURVEY_FILE_TYPE
        songs = list(import_dir.glob(glob))
        self.stdout.write('%d clips found.' % len(songs))
        for song in songs:
            ensure_clip(self.stdout, song, clips_dir)
