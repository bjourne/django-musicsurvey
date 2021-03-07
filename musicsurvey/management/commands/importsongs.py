from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from musicsurvey import random_name
from musicsurvey.models import *
from pathlib import Path
from shutil import copy

def ensure_clip(stdout, src, clips_dir):
    parts = src.stem.split('-')
    offset = '%s-%s' % (parts[0], parts[1])
    gen_type = '%s-%s' % (parts[2], parts[3])
    if Clip.objects.filter(offset = offset, gen_type = gen_type).exists():
        return
    name = random_name()
    clip = Clip(name = name, offset = offset, gen_type = gen_type)
    clip.save()
    dst = clips_dir / ('%s.mp3' % name)
    copy(str(src), str(dst))
    stdout.write('Importing %s as %s.' % (src.stem, dst.stem))

class Command(BaseCommand):
    help = 'Import clips from a directory'

    def add_arguments(self, parser):
        parser.add_argument('import-dir', type = str)
        parser.add_argument(
            '--delete-existing', action = 'store_true',
            help = 'Delete existing clips before importing')

    def handle(self, *args, **opts):
        import_dir = Path(opts['import-dir'])

        clips_dir = settings.STATIC_ROOT / 'musicsurvey' / 'clips'
        clips_dir.mkdir(exist_ok = True, parents = True)
        if opts['delete_existing']:
            Clip.objects.all().delete()
            Round.objects.all().delete()

        for song in import_dir.glob('*.mp3'):
            ensure_clip(self.stdout, song, clips_dir)
