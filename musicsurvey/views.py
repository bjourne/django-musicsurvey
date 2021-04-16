from collections import defaultdict
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from musicsurvey import random_name, settings
from musicsurvey.models import Clip, Duel, Round
from random import choice, sample, shuffle, randint

def thanks(request, round_name):
    round = get_object_or_404(Round, name = round_name)
    duels = round.duel_set.all()
    context = {'duels' : duels}
    return render(request, 'musicsurvey/thanks.html', context)

def submit(request):
    pairs = [v.split('-') for (k, v)
             in request.POST.items() if k[:3] == 'sel']
    elapsed_s = request.POST['elapsed_s']
    ip = request.META['REMOTE_ADDR']
    round = Round(ip = ip, elapsed_s = elapsed_s, name = random_name())
    round.save()
    for winner, loser in pairs:
        winner = Clip.objects.get(random_name = winner)
        loser = Clip.objects.get(random_name = loser)
        duel = Duel(winner = winner, loser = loser, round = round)
        duel.save()
    return HttpResponseRedirect(reverse('thanks', args=[round.name]))

# Not awesome code, but it ensure that no composition repeats and that
# the number of random clips is limited.
def sample_pairs_same_compositions():
    clips_per_composition = defaultdict(list)
    for clip in Clip.objects.all():
        clips_per_composition[clip.composition].append(clip)
    clips_per_composition = list(clips_per_composition.items())
    for composition, clips in clips_per_composition:
        shuffle(clips)
    shuffle(clips_per_composition)

    random_pairs = []
    human_pairs = []
    other_pairs = []

    n_total_pairs = settings.MUSICSURVEY_PAIRS_PER_SURVEY
    n_random_pairs = settings.MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY
    n_human_pairs = settings.MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY

    n_compositions = len(clips_per_composition)
    if n_compositions < n_total_pairs:
        err = ('Only %d compositions found, %d is required. Use the '
               '"importsongs" command to import a clip collection.'
               % (n_compositions, n_total_pairs))
        raise ImproperlyConfigured(err)

    for composition, clips in clips_per_composition:
        random_clips = [c for c in clips if 'random' in c.composer]
        human_clips = [c for c in clips if 'original' in c.composer]
        other_clips = [c for c in clips
                       if (not 'random' in c.composer
                           and not 'original' in c.composer)]
        if (random_clips
            and other_clips
            and len(random_pairs) < n_random_pairs):
            random_pairs.append([random_clips[0], other_clips[0]])
        elif (human_clips
            and other_clips
            and len(human_pairs) < n_human_pairs):
            human_pairs.append([human_clips[0], other_clips[0]])
        elif len(other_clips) >= 2:
            other_pairs.append([other_clips[0], other_clips[1]])
        if (len(random_pairs) + len(human_pairs) + len(other_pairs)
            == n_total_pairs):
            break
    pairs = random_pairs + human_pairs + other_pairs
    assert len(pairs) == n_total_pairs
    assert len(random_pairs) == n_random_pairs
    assert len(human_pairs) == n_human_pairs
    return pairs

def sample_pairs():
    clips = list(Clip.objects.all())

    random_clips = [c for c in clips if 'random' in c.composer]
    human_clips = [c for c in clips if 'original' in c.composer]
    other_clips = [c for c in clips
                   if (not 'random' in c.composer
                       and not 'original' in c.composer)]

    n_human_pairs = settings.MUSICSURVEY_HUMAN_PAIRS_PER_SURVEY
    n_random_pairs = settings.MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY
    n_other_pairs = settings.MUSICSURVEY_PAIRS_PER_SURVEY \
        - n_human_pairs - n_random_pairs

    pairs = []
    for _ in range(n_human_pairs):
        clip1 = choice(human_clips)
        human_clips.remove(clip1)
        clip2 = choice(other_clips)
        other_clips.remove(clip2)
        pairs.append([clip1, clip2])
    for _ in range(n_random_pairs):
        clip1 = choice(random_clips)
        random_clips.remove(clip1)
        clip2 = choice(other_clips)
        other_clips.remove(clip2)
        pairs.append([clip1, clip2])
    for _ in range(n_other_pairs):
        clip1 = choice(other_clips)
        other_clips.remove(clip1)
        while True:
            clip2 = choice(other_clips)
            if clip2.composer != clip1.composer:
                other_clips.remove(clip2)
                break
        pairs.append([clip1, clip2])

    assert len(pairs) == n_human_pairs + n_random_pairs + n_other_pairs
    return pairs

def index(request):
    if settings.MUSICSURVEY_SAME_COMPOSITIONS:
        pairs = sample_pairs_same_compositions()
    else:
        pairs = sample_pairs()
    for pair in pairs:
        shuffle(pair)
    shuffle(pairs)
    context = {'pairs' : pairs}
    return render(request, 'musicsurvey/index.html', context)
