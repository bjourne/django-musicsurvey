from django.db.models import *

class Clip(Model):
    name = CharField(max_length = 10, unique = True)
    offset = CharField(max_length = 32)
    gen_type = CharField(max_length = 64)

    def __str__(self):
        return '%s (%s, %s)' % (self.name, self.offset, self.gen_type)

    class Meta:
        constraints = [
            UniqueConstraint(fields = ['offset', 'gen_type'],
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
