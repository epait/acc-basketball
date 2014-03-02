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
			response = urllib2.urlopen("http://www.hokiesports.com/mbasketball/players/")
			html = response.read()

			#end server version


			#use this code when file is local:
			#with open ('transcript.html', 'r') as tempFile:
			#html=tempFile.read()

			#end local version
			#print html

			soup = BeautifulSoup(html)

			tabledata = soup.find_all('table')[1] #find the proper table
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
			team = 'Virginia Tech'

			current_team = Team.objects.get(name=team)
			current_team.twitter = 'VT_MBBall'
			current_team.color = '#660000'
			current_team.save()

			for link in tabledata.select('.evenrow a'):
				player_links.append(link.get('href'))
				if link.get_text() == 'Joey van Zegeren':
					player_names.append('Joey Van Zegeren')
				else:
					player_names.append(link.get_text())

			for link in tabledata.select('.oddrow a'):
				player_links.append(link.get('href'))
				if link.get_text() == 'Joey van Zegeren':
					player_names.append('Joey Van Zegeren')
				else:
					player_names.append(link.get_text())

			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://hokiesports.com/mbasketball/players/%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find_all('ul')[26]

				# for name in soup.find_all('span', {'class': 'whiteBox'}):
				# 	player_names.append(name.next.next.strip())

				for portrait in soup.find_all('div', {'class': 'bioimg'}):
					portrait_urlpath = portrait.get('style')
					portrait_url = re.sub('background-image: url\(', '', portrait_urlpath)
					url = re.sub('\)', '', portrait_url)
					player_portraits.append('http://hokiesports.com%s' %(url))

				number = soup.find('span', {'id': 'number'})
				player_numbers.append(number.text)

				for position in playerdata.find_all('li')[0]:
					player_positions.append(position.strip())

				for height in playerdata.find_all('li')[2]:
					no_space = re.sub(' ', '', height)
					player_heights.append(no_space.strip())

				for weight in playerdata.find_all('li')[3]:
					player_weights.append(weight.strip(' lbs.'))

				for class_year in playerdata.find_all('li')[1]:
					year = re.sub('r-', 'Redshirt ', class_year.strip())
					player_class_years.append(year)

				for hometown in playerdata.find_all('li')[5]:
					player_hometowns.append(hometown.strip())

				for highschool in playerdata.find_all('li')[4]:
					player_highschools.append(highschool.strip())


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

				player_count += 1





		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrapevt.py')