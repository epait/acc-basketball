from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player, Season, SeasonStats

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports player info from the uva athletic department website'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			response = urllib2.urlopen("http://www.virginiasports.com/sports/m-baskbl/mtt/va-m-baskbl-mtt.html")
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
			team = 'Virginia'

			current_team = Team.objects.get(name=team)
			current_team.twitter = 'UVAMensHoops'
			current_team.color = '#0D3268'
			current_team.logo = 'logos/virginia.png'
			current_team.portrait = 'portraits/teams/jpjarena.jpg'
			current_team.save()


			for link in tabledata.find_all('a'):
				player_links.append(link.get('href'))
				player_names.append(link.get_text())
				name = link.get_text()
				position_abv = soup.find(text=name).next.next.next.next.next.next.next.next.next.text
				if 'G' in position_abv:
					position = re.sub('G', 'Guard', position_abv)
				elif 'F/C' in position_abv:
					position = re.sub('F/C', 'Forward/Center', position_abv)
				elif 'F' in position_abv:
					position = re.sub('F', 'Forward', position_abv)
				elif 'C' in position_abv:
					position = re.sub('C', 'Center', position_abv)
				else:
					position = position_abv
				player_positions.append(position)
				player_heights.append(soup.find(text=name).next.next.next.text)
				player_weights.append(soup.find(text=name).next.next.next.next.next.next.text)


			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://virginiasports.com%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find('table')

				number = soup.find('div', {'class': 'player-number'}).get_text()
				player_numbers.append(number)

				portrait = soup.find('img', {'alt': player_names[player_count]})
				player_portraits.append(portrait.get('src'))

				class_year = soup.find(text='Class:').next.next
				redshirt_replace = re.sub('RS', 'Redshirt', class_year.strip())
				player_class_years.append(redshirt_replace)

				highschool = soup.find(text='High School:').next.next
				player_highschools.append(highschool.strip())

				hometown = soup.find(text='Hometown:').next.next
				player_hometowns.append(hometown.strip())


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

		self.stdout.write('end of scrapevirginia.py')