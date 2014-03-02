from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports player info from the gt athletic department website'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			response = urllib2.urlopen("http://www.ramblinwreck.com/sports/m-baskbl/mtt/geot-m-baskbl-mtt.html")
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
			team = 'Georgia Tech'


			for link in tabledata.find_all('a'):
				player_links.append(link.get('href'))
				player_names.append(link.get_text())
				name = link.get_text()
				player_positions.append(soup.find(text=name).next.next.text)
				player_heights.append(soup.find(text=name).next.next.next.next.next.next.next.text)
				player_weights.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.text)


			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://ramblinwreck.com%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find('table')

				name = soup.find('div', {'class': 'player-name'})
				number = re.sub("[^0-9]", "", name.text.strip())
				player_numbers.append(number)

				portrait = soup.find('img', {'id': 'player-photo'})
				player_portraits.append(portrait.get('src'))

				class_year = soup.find(text='Class:').next.next
				player_class_years.append(class_year.strip())

				highschool = soup.find(text='High School:').next.next
				player_highschools.append(highschool.strip())

				hometown = soup.find(text='Hometown:').next.next
				player_hometowns.append(hometown.strip())

				# for position in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[0]:
				# 	player_positions.append(position.strip())

				# for height in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[1]:
				# 	player_heights.append(height.strip())

				# for weight in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[2]:
				# 	player_weights.append(weight.strip())

				# for class_year in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[3]:
				# 	player_class_years.append(class_year.strip())

				# for hometown in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[4]:
				# 	player_hometowns.append(hometown.strip())

				# for highschool in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[5]:
				# 	player_highschools.append(highschool.strip())

				# print player_numbers[player_count], player_names[player_count], player_positions[player_count], player_highschools[player_count]
				# print player_count, player_names[player_count]
				# print player_names[player_count]
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

				# current_player.team = Team.objects.get(name=team)
				# current_player.position = player_positions[player_count]
				# current_player.number = player_numbers[player_count]
				# current_player.portrait = player_portraits[player_count]
				# current_player.height = player_heights[player_count]
				# current_player.weight = player_weights[player_count]
				# current_player.class_year = player_class_years[player_count]
				# current_player.hometown = player_hometowns[player_count]
				# current_player.highschool = player_highschools[player_count]
				# current_player.class_year = player_class_years[player_count]
				# current_player.save()

				player_count += 1





		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrapegt.py')