from django.contrib import admin
from .models import Game, History, Trial

# Register your models here.

admin.site.register(Game)
admin.site.register(History)
admin.site.register(Trial)