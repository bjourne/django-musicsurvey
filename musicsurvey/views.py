from collections import defaultdict
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
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
        winner = Clip.objects.get(name = winner)
        loser = Clip.objects.get(name = loser)
        duel = Duel(winner = winner, loser = loser, round = round)
        duel.save()
    return HttpResponseRedirect(reverse('thanks', args=[round.name]))

# Not awesome code, but it ensure that no offset repeats and that the
# number of random clips is limited.
def index(request):

    # Clips grouped by offsets in random order.
    clips_per_offset = defaultdict(list)
    for clip in Clip.objects.all():
        clips_per_offset[clip.offset].append(clip)
    clips_per_offset = list(clips_per_offset.items())
    for offset, clips in clips_per_offset:
        shuffle(clips)
    shuffle(clips_per_offset)

    n_total_pairs = settings.MUSICSURVEY_PAIRS_PER_SURVEY
    n_random_pairs = settings.MUSICSURVEY_RANDOM_PAIRS_PER_SURVEY
    n_non_random_pairs = n_total_pairs - n_random_pairs
    random_pairs = []
    non_random_pairs = []
    for offset, clips in clips_per_offset:
        random_clips = [c for c in clips if 'random' in c.gen_type]
        non_random_clips = [c for c in clips if not 'random' in c.gen_type]
        if (random_clips
            and non_random_clips
            and len(random_pairs) < n_random_pairs):
            random_pairs.append([random_clips[0], non_random_clips[0]])
        elif (len(non_random_clips) > 1
              and len(non_random_pairs) < n_non_random_pairs):
            non_random_pairs.append(sample(non_random_clips, 2))
    pairs = random_pairs + non_random_pairs
    assert len(pairs) == n_total_pairs
    assert len(random_pairs) == n_random_pairs
    assert len(non_random_pairs) == n_non_random_pairs
    for pair in pairs:
        shuffle(pair)
    shuffle(pairs)
    context = {'pairs' : pairs}
    return render(request, 'musicsurvey/index.html', context)
