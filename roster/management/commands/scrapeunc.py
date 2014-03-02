from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports player info from the unc athletic department website'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			response = urllib2.urlopen("http://www.goheels.com/SportSelect.dbml?SITE=UNC&DB_OEM_ID=3350&SPID=12965&SPSID=667867")
			html = response.read()

			#end server version


			#use this code when file is local:
			#with open ('transcript.html', 'r') as tempFile:
			#html=tempFile.read()

			#end local version
			#print html

			soup = BeautifulSoup(html)

			tabledata = soup.find('table') #find the proper table
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
			team = 'North Carolina'

			current_team = Team.objects.get(name=team)
			current_team.twitter = 'UNC_Basketball'
			current_team.color = '#56A0D3'
			current_team.save()

			for link in tabledata.find_all('a'):
				player_links.append(link.get('href'))
				name_list = link.text.strip().replace(',', '').split(' ')
				reverse_places = len(name_list) - 1
				reverse_name = name_list[::-reverse_places]
				name = ' '.join(reverse_name)
				player_names.append(name)

			for name_string in tabledata.find_all('td', {'class': 'number'}):
				number = name_string.text.strip()
				player_numbers.append(number.strip('  ".?<> $%^&* '))

			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://goheels.com%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find_all('table')[0]

				# for name in soup.find_all('span', {'class': 'whiteBox'}):
				# 	player_names.append(name.next.next.strip())

				for portrait in soup.select('.bio-photo img'):
					player_portraits.append(portrait.get('src'))

				for position in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[0]:
					player_positions.append(position.strip())

				for height in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[1]:
					player_heights.append(height.strip())

				for weight in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[2]:
					player_weights.append(weight.strip())

				for class_year in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[3]:
					player_class_years.append(class_year.strip())

				for hometown in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[4]:
					player_hometowns.append(hometown.strip())

				for highschool in playerdata.find_all('td', {'class': 'PlayerBioPosValue'})[5]:
					player_highschools.append(highschool.strip())


				# print player_numbers[player_count], player_names[player_count], player_positions[player_count], player_highschools[player_count]
				# print player_count, player_names[player_count]
				# print player_names[player_count]
				current_player = Player.objects.get(name__contains= player_names[player_count])
				print 'Name:', current_player.name
				print 'Portrait:', player_portraits[player_count]
				print 'Number:', player_numbers[player_count]
				print 'Position:', player_positions[player_count]
				print 'Height:', player_heights[player_count]
				print 'Weight:', player_weights[player_count]
				print 'Class Year:', player_class_years[player_count]
				print 'Hometown:', player_hometowns[player_count]
				print 'High School:', player_highschools[player_count]
				print ' '

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

				player_count += 1





		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrapeunc.py')