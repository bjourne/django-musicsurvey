from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

class ClipAdmin(ModelAdmin):
    list_display = 'random_name', 'composer', 'composition', 'misc'

class DuelAdmin(ModelAdmin):
    list_display = 'winner', 'loser', 'round'

class RoundAdmin(ModelAdmin):
    list_display = 'name', 'ip', 'submitted', 'elapsed_s'
    readonly_fields = 'submitted',

admin.site.register(Clip, ClipAdmin)
admin.site.register(Duel, DuelAdmin)
admin.site.register(Round, RoundAdmin)
