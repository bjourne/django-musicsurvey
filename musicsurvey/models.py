from django.db.models import *

class Clip(Model):
    random_name = CharField(max_length = 10, unique = True)
    composition = CharField(max_length = 32)
    composer = CharField(max_length = 64)
    misc = CharField(max_length = 32)

    def __str__(self):
        return '%s (%s, %s, %s)' % (self.random_name,
                                    self.composition,
                                    self.composer,
                                    self.misc)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields = ['composition', 'composer', 'misc'],
                name = 'uq_clip')
        ]

class Round(Model):
    submitted = DateTimeField(auto_now_add = True)
    ip = GenericIPAddressField()
    elapsed_s = FloatField()
    name = CharField(max_length = 10, unique = True)
    def __str__(self):
        time_str = self.submitted.strftime('%Y-%m-%d %H:%M:%S')
        return '%s/%s in %.2fs' % (self.ip, time_str, self.elapsed_s)
    class Meta:
        constraints = [
            UniqueConstraint(fields = ['submitted', 'ip'],
                             name = 'uq_round')
        ]

class Duel(Model):
    winner = ForeignKey(Clip, on_delete = CASCADE,
                        related_name = 'winner')
    loser = ForeignKey(Clip, on_delete = CASCADE,
                       related_name = 'loser')
    round = ForeignKey(Round, on_delete = CASCADE)

    def __str__(self):
        return '%s prefer %s over %s' % (self.round.ip,
                                         self.winner, self.loser)
