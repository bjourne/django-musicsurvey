from collections import defaultdict
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from musicsurvey import random_name
from musicsurvey.models import Clip, Duel, Round
from musicsurvey.settings import MUSICSURVEY_CLIPS_PER_SURVEY
from random import sample, randint

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

def index(request):
    clips_per_offset = defaultdict(list)
    for clip in Clip.objects.all():
        clips_per_offset[clip.offset].append(clip)
    offsets = sample(list(clips_per_offset.keys()),
                     MUSICSURVEY_CLIPS_PER_SURVEY)
    pairs = []
    for offset in offsets:
        pair = sample(clips_per_offset[offset], 2)
        pairs.append(pair)
    context = {'pairs' : pairs}
    return render(request, 'musicsurvey/index.html', context)
