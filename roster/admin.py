from django.contrib import admin
from django_admin_bootstrapped.admin.models import SortableInline
from roster.models import Team, Player, Coach, Season, OffensiveStats, DefensiveStats

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('conference',)

admin.site.register(Team, TeamAdmin)

class PlayerAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('position', 'team')

admin.site.register(Player, PlayerAdmin)

class CoachAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('position', 'team')

admin.site.register(Coach, CoachAdmin)

class SeasonAdmin(admin.ModelAdmin):
	search_fields = ('',)

admin.site.register(Season, SeasonAdmin)

class OffensiveStatsAdmin(admin.ModelAdmin):
	search_fields = ('',)

admin.site.register(OffensiveStats, OffensiveStatsAdmin)

class DefensiveStatsAdmin(admin.ModelAdmin):
	search_fields = ('',)

admin.site.register(DefensiveStats, DefensiveStatsAdmin)