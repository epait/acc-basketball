from django.contrib import admin
from django_admin_bootstrapped.admin.models import SortableInline
from roster.models import Team, Player, Season, SeasonStats#, Coach

# Register your models here.

class TeamAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('conference',)
	list_display = ('name', 'overall_record', 'conference', 'conference_record')

admin.site.register(Team, TeamAdmin)

class PlayerAdmin(admin.ModelAdmin):
	search_fields = ('name',)
	list_filter = ('team__name', 'position')
	list_display = ('name', 'team', 'position', 'class_year', 'hometown')

admin.site.register(Player, PlayerAdmin)

# class CoachAdmin(admin.ModelAdmin):
# 	search_fields = ('name',)
# 	list_filter = ('position', 'team')

# admin.site.register(Coach, CoachAdmin)

class SeasonAdmin(admin.ModelAdmin):
	search_fields = ('',)

admin.site.register(Season, SeasonAdmin)

class SeasonStatsAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {
			'fields': ('season',)
		}),
        ('Type', {
        	'classes': ('collapse', 'in'),
            'fields': ('player', 'team'),
            'description': 'Please choose <em>either</em> a team <em>or</em> a player.'
        }),
        ('Offensive Stats', {
        	'classes': ('collapse', 'in'),
        	'fields': ('points_per_game', 'rebounds_per_game', 'assists_per_game', 'turnovers_per_game', 'field_goal_percentage', 'free_throw_percentage', 'three_point_percentage')
        }),
        ('Defensive Stats', {
        	'classes': ('collapse', 'in'),
        	'fields': ('blocks_per_game', 'steals_per_game')
        }),
    )

admin.site.register(SeasonStats, SeasonStatsAdmin)