from django.db import models

# Create your models here.

class Team(models.Model):
	name = models.CharField(unique=True, max_length=100, verbose_name='Team')
	mascot = models.CharField(max_length=100)
	abbreviation = models.CharField(max_length=4)
	wins = models.IntegerField(max_length=3)
	losses = models.IntegerField(max_length=3)
	conference = models.CharField(max_length=50)
	conference_wins = models.IntegerField(max_length=3)
	conference_losses = models.IntegerField(max_length=3)
	portrait = models.ImageField(upload_to='portraits/teams/', height_field=None, width_field=None, max_length=200)
	color = models.CharField(max_length=7)

	class Meta(object):
		ordering = ('name', 'conference')

	def __unicode__(self):
		return U'%s' %(self.name)


class Player(models.Model):
	name = models.CharField(max_length=75)
	team = models.ForeignKey('Team')
	position = models.CharField(max_length=25)
	number = models.IntegerField(max_length=2)
	class_year_choices = (
		('FR', 'Freshman'),
		('SO', 'Sophomore'),
		('JR', 'Junior'),
		('SR', 'Senior'),
	)
	class_year = models.CharField(max_length=2, choices=class_year_choices)
	date_of_birth = models.CharField(max_length=18, help_text='Please use the following format: <em>Month Day, Year</em>')
	hometown=models.CharField(max_length=150, help_text='Please use the following format: <em>City, State</em>.')
	height = models.IntegerField(max_length=3, help_text='Please use inches.')
	weight = models.IntegerField(max_length=3, help_text='Please use pounds.')
	high_school = models.CharField(max_length=100)
	bio = models.TextField()
	portrait = models.ImageField(upload_to='portraits/players/', height_field=None, width_field=None, max_length=200)

	class Meta(object):
		ordering = ('team','name', 'position')

	def __unicode__(self):
		return U'%s, %s | %s' %(self.name, self.position, self.team)


class Coach(models.Model):
	name = models.CharField(max_length=75)
	team = models.ForeignKey('Team')
	position = models.CharField(max_length=25)
	bio = models.TextField()
	hometown = models.CharField(max_length=150, help_text='Please use the following format: <em>City, State</em>.')
	experience = models.IntegerField(max_length=3)
	portrait = models.ImageField(upload_to='portraits/coaches/', height_field=None, width_field=None, max_length=200)

	class Meta(object):
		verbose_name_plural = 'Coaches' 
		ordering = ('position','name')

	def __unicode__(self):
		return U'%s, %s' %(self.name, self.position)


class SeasonStats(models.Model):
	team = models.ForeignKey('Team', null=True, blank=True)
	player = models.ForeignKey('Player', null=True, blank=True)
	season = models.ForeignKey('Season') 
	points_per_game = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='PPG')
	rebounds_per_game = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='RPG')
	assists_per_game = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='APG')
	field_goal_percentage = models.DecimalField(max_digits=3, decimal_places=3, verbose_name='FG%')
	free_throw_percentage = models.DecimalField(max_digits=3, decimal_places=3, verbose_name='FT%')
	three_point_percentage = models.DecimalField(max_digits=3, decimal_places=3, verbose_name='3P%')
	points_allowed_per_game = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Points Allowed')
	blocks_per_game = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='BPG')
	steals_per_game = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='SPG')

	class Meta(object):
		verbose_name = 'Season Stats' 
		verbose_name_plural = 'Season Stats' 

	def __unicode__(self):
		if self.team == None:
			return U'(%s) %s' %(self.season, self.player)
		else:
			return U'(%s) %s' %(self.season, self.team)


class Season(models.Model):
	start_year = models.IntegerField(max_length=4)
	end_year = models.IntegerField(max_length=4)

	def __unicode__(self):
		return U'%s - %s' %(self.start_year, self.end_year)