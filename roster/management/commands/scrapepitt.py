from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player, Season, SeasonStats

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports player info from the pitt athletic department website'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			response = urllib2.urlopen("http://www.pittsburghpanthers.com/sports/m-baskbl/mtt/pitt-m-baskbl-mtt.html")
			html = response.read()

			#end server version


			#use this code when file is local:
			#with open ('transcript.html', 'r') as tempFile:
			#html=tempFile.read()

			#end local version
			#print html

			soup = BeautifulSoup(html)

			tabledata = soup.find('table', {'id': 'sortable_roster'}) #find the proper table
			player_names = [] #list to store every player in the table
			player_links = []
			player_count = 0
			player_hometowns = []
			player_highschools = []
			player_positions = []
			player_portraits = []
			player_heights = []
			player_weights = []
			player_class_years = []
			player_numbers = []
			team = 'Pittsburgh'

			current_team = Team.objects.get(name=team)
			current_team.twitter = 'HailToPittHoops'
			current_team.color = '#111150'
			current_team.logo = 'logos/pitt.png'
			current_team.portrait = 'portraits/teams/petersencenter.jpg'
			current_team.save()


			for link in tabledata.find_all('a'):
				player_links.append(link.get('href'))
				player_names.append(link.get_text())


			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://pittsburghpanthers.com%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find('table')

				number_button = playerdata.find_all('img')[4]
				number = number_button.get('src').strip(' abcdefghijklmnopqrstuvwxyz:_/.-')
				player_numbers.append(number)

				portrait = soup.find('img', {'alt': player_names[player_count]})
				player_portraits.append(portrait.get('src'))

				class_year = soup.find(text='Class:').next.next
				redshirt_replace = re.sub('RS', 'Redshirt', class_year.strip())
				remove_student = re.sub('Student', '', redshirt_replace)
				player_class_years.append(remove_student.strip())

				highschool = soup.find(text='High School:').next.next
				player_highschools.append(highschool.strip())

				height = soup.find(text='Height / Weight:').next.next
				player_heights.append(height.split(' ')[0].strip())

				weight = soup.find(text='Height / Weight:').next.next
				player_weights.append(weight.split(' ')[2].strip())

				hometown = soup.find(text='Hometown:').next.next
				player_hometowns.append(hometown.strip())

				position = soup.find(text='Position:').next.next
				player_positions.append(position.strip())


				current_player, created = Player.objects.get_or_create(name= player_names[player_count])
				print 'Name:', current_player.name

				# print 'Name:', player_names[player_count]
				print 'Portrait:', player_portraits[player_count]
				print 'Number:', player_numbers[player_count]
				print 'Position:', player_positions[player_count]
				print 'Height:', player_heights[player_count]
				print 'Weight:', player_weights[player_count]
				print 'Class Year:', player_class_years[player_count]
				print 'Hometown:', player_hometowns[player_count]
				print 'High School:', player_highschools[player_count]
				print ' '

				current_player.team = Team.objects.get(name=team)
				current_player.position = player_positions[player_count]
				current_player.number = player_numbers[player_count]
				current_player.portrait = player_portraits[player_count]
				current_player.height = player_heights[player_count]
				current_player.weight = player_weights[player_count]
				current_player.class_year = player_class_years[player_count]
				current_player.hometown = player_hometowns[player_count]
				current_player.highschool = player_highschools[player_count]
				current_player.class_year = player_class_years[player_count]
				current_player.save()

				stats_data, created = SeasonStats.objects.get_or_create(player=current_player)
				stats_data.season = Season.objects.get(start_year=2013, end_year=2014)
				stats_data.save()

				player_count += 1





		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrapepitt.py')