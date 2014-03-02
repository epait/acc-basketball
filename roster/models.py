from django.db import models

# Create your models here.
 
class Team(models.Model):
	name = models.CharField(null=True, unique=True, max_length=100, verbose_name='Team')
 	abbreviation = models.CharField(null=True, max_length=4)
	overall_record = models.CharField(null=True, max_length=5)
	conference = models.CharField(null=True, max_length=50)
	conference_record = models.CharField(null=True, max_length=5)
	portrait = models.ImageField(null=True, upload_to='portraits/teams/', height_field=None, width_field=None, max_length=200)
	color = models.CharField(null=True, max_length=7)

	class Meta(object):
		ordering = ('name', 'conference')

	def __unicode__(self):
		return U'%s' %(self.name)


class Player(models.Model):
	name = models.CharField(null=True, max_length=75)
	team = models.ForeignKey('Team', null=True)
	position = models.CharField(null=True, max_length=25)
	number = models.IntegerField(null=True, max_length=2)
	class_year_choices = (
		('Freshman', 'Freshman'),
		('Sophomore', 'Sophomore'),
		('Junior', 'Junior'),
		('Senior', 'Senior'),
		('Redshirt Freshman', 'Redshirt Freshman'),
		('Redshirt Sophomore', 'Redshirt Sophomore'),
		('Redshirt Junior', 'Redshirt Junior'),
		('Redshirt Senior', 'Redshirt Senior'),
		('Graduate', 'Graduate'),
	)
	class_year = models.CharField(null=True, max_length=2, choices=class_year_choices, verbose_name='Class Year')
	hometown = models.CharField(null=True, max_length=150, help_text='Please use the following format: <em>City, State</em>.')
	highschool = models.CharField(null=True, max_length=150, verbose_name='High School')
	height = models.CharField(null=True, max_length=5, help_text='Please use the following format: <em>5\'11\"</em>.')
	weight = models.IntegerField(null=True, max_length=3, help_text='Please use pounds.')
	portrait = models.ImageField(null=True, upload_to='portraits/players/', height_field=None, width_field=None, max_length=200)

	class Meta(object):
		ordering = ('team','name', 'position')

	def __unicode__(self):
		return U'%s' %(self.name)


# class Coach(models.Model):
# 	name = models.CharField(null=True, max_length=75)
# 	team = models.ForeignKey('Team', null=True)
# 	position = models.CharField(null=True, max_length=25)
# 	bio = models.TextField(null=True, )
# 	hometown = models.CharField(null=True, max_length=150, help_text='Please use the following format: <em>City, State</em>.')
# 	experience = models.IntegerField(null=True, max_length=3)
# 	portrait = models.ImageField(null=True, upload_to='portraits/coaches/', height_field=None, width_field=None, max_length=200)

# 	class Meta(object):
# 		verbose_name_plural = 'Coaches' 
# 		ordering = ('position','name')

# 	def __unicode__(self):
# 		return U'%s, %s' %(self.name, self.position)


class SeasonStats(models.Model):
	team = models.ForeignKey('Team', null=True, blank=True)
	player = models.ForeignKey('Player', null=True, blank=True)
	season = models.ForeignKey('Season', null=True) 
	points_per_game = models.DecimalField(null=True, max_digits=4, decimal_places=1, verbose_name='PPG')
	rebounds_per_game = models.DecimalField(null=True, max_digits=4, decimal_places=1, verbose_name='RPG')
	assists_per_game = models.DecimalField(null=True, max_digits=3, decimal_places=1, verbose_name='APG')
	turnovers_per_game = models.DecimalField(null=True, max_digits=4, decimal_places=1, verbose_name='TPG')
	field_goal_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=3, verbose_name='FG%')
	free_throw_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=3, verbose_name='FT%')
	three_point_percentage = models.DecimalField(null=True, max_digits=5, decimal_places=3, verbose_name='3P%')
	blocks_per_game = models.DecimalField(null=True, max_digits=4, decimal_places=1, verbose_name='BPG')
	steals_per_game = models.DecimalField(null=True, max_digits=4, decimal_places=1, verbose_name='SPG')

	class Meta(object):
		verbose_name = 'Season Stats' 
		verbose_name_plural = 'Season Stats' 
		ordering = ('player', 'team')

	def __unicode__(self):
		if self.team == None:
			return U'%s' %(self.player)
		else:
			return U'%s' %(self.team)


class Season(models.Model):
	start_year = models.IntegerField(null=True, max_length=4)
	end_year = models.IntegerField(null=True, max_length=4)

	def __unicode__(self):
		return U'%s - %s' %(self.start_year, self.end_year)