from collections import defaultdict
from django.conf import settings as settings
from django.core.management.base import BaseCommand, CommandError
from matplotlib.patches import Patch
from musicsurvey.models import *
from termtables import to_string

import matplotlib.pyplot as plt
import numpy as np

def print_term_table(row_fmt, rows, header, alignment):
    def format_col(fmt, col):
        if callable(fmt):
            return fmt(col)
        return fmt % col
    rows = [[format_col(*e) for e in zip(row_fmt, row)] for row in rows]
    s = to_string(rows,
                  header = header,
                  padding = (0, 0, 0, 0),
                  alignment = alignment,
                  style = "            -- ")
    m = len(s.splitlines()[1]) - 2
    print(' ' + '=' * m)
    print(s)
    print(' ' + '=' * m)

def plot_overall_win_ratios(rows, names, png_name):
    # First plot overall
    fig, ax = plt.subplots(figsize = (12, 4))

    y_pos = np.arange(len(names)) * 0.2

    wins = rows[-1][1:]
    ax.barh(y_pos, wins, align = 'center', height = 0.12,
            color = ['C0', 'C1', 'C2', 'C3'])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.invert_yaxis()
    ax.set_xlabel('win ratio')
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    plt.savefig(png_name)

def plot_win_ratios_per_opponent(rows, names, png_name):
    n_names = len(names)
    fig, ax = plt.subplots(figsize = (12, 4))

    # Last row is overall and the first column which contains headers.
    wins = [[] for _ in names]
    for y, row in enumerate(rows[:-1]):
        for x, col in enumerate(row[1:]):
            if x != y:
                # If the combatants haven't meet, set the win ratio to
                # 0.
                wins[x].append(col if col != 'n/a' else 0.0)

    assert n_names == 4
    colors = [
        ['C1', 'C2', 'C3'],
        ['C0', 'C2', 'C3'],
        ['C0', 'C1', 'C3'],
        ['C0', 'C1', 'C2']
    ]
    bar_dist = 0.1
    group_dist = bar_dist * n_names

    for i in range(len(wins)):
        ofs = i * group_dist
        ax.bar([ofs - bar_dist, ofs, ofs + bar_dist],
               wins[i],
               width = bar_dist * 0.70,
               color = colors[i])

    ax.set_ylabel('win ratio')
    ax.set_xticks(np.arange(n_names) * group_dist)
    ax.set_xticklabels(names)
    handles = [Patch(color = 'C%d' % i, label = name)
               for i, name in enumerate(names)]
    ax.legend(handles = handles, loc = 'upper right')
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    plt.savefig(png_name)


class Command(BaseCommand):
    help = 'Plots statistics'

    def handle(self, *args, **opts):
        battles = defaultdict(lambda: defaultdict(int))
        wins = defaultdict(lambda: defaultdict(int))

        stdout = self.stdout
        fmt = '%s submitted %d results in %.2f seconds'
        all_duels = []
        for round in Round.objects.all():
            duels = round.duel_set.all()
            duels = [(d.winner.composer, d.loser.composer) for d in duels]
            n_duels = len(duels)
            args = (round.ip, n_duels, round.elapsed_s)
            stdout.write(fmt % args)
            if any('random' in d[0] for d in duels):
                stdout.write('Random clip preferred - skipping round.')
                continue

            # Don't count wins over random
            for winner, loser in duels:
                assert not 'random' in winner
                if 'random' in loser:
                    continue
                all_duels.append((winner, loser))
            # all_duels.extend(duels)

        for winner, loser in all_duels:
            print(winner, loser)
            battles[winner][loser] += 1
            battles[loser][winner] += 1
            wins[winner][loser] += 1

        human_names = {
            k : v[1] if len(v) == 2 else v
            for (k, v) in settings.MUSICSURVEY_COMPOSER_NAMES.items()
            if not 'random' in k
        }

        rows = []
        for gen1 in human_names:
            row = [human_names[gen1]]
            for gen2 in human_names:
                n_battles = battles[gen2][gen1]
                n_wins = wins[gen2][gen1]
                row.append('n/a' if not n_battles else n_wins / n_battles)
            rows.append(row)

        # Add overall
        row = ['Overall']
        for winner in human_names:
            n_battles = sum(battles[winner].values())
            n_wins = sum(wins[winner].values())
            row.append(0 if not n_battles else n_wins / n_battles)
        rows.append(row)

        def cell_fmt(x):
            if isinstance(x, str):
                return x
            return '%.2f' % x

        names = list(human_names.values())
        row_fmt = [cell_fmt] * 5
        header = [''] + names
        print_term_table(row_fmt, rows, header, 'lrrrr')

        png_name = 'win-ratios.png'
        stdout.write('Saving image "%s".' % png_name)
        plot_overall_win_ratios(rows, names, png_name)
        png_name = 'win-ratios-per-opponent.png'
        stdout.write('Saving image "%s".' % png_name)
        plot_win_ratios_per_opponent(rows, names, png_name)
