from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports player info from the syracuse athletic department website'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			headers = { 'User-Agent' : 'Mozilla/5.0' }
			req = urllib2.Request('http://www.cuse.com/roster.aspx?path=mbasket', None, headers)
			html = urllib2.urlopen(req).read()

			#end server version


			#use this code when file is local:
			#with open ('transcript.html', 'r') as tempFile:
			#html=tempFile.read()

			#end local version
			#print html

			soup = BeautifulSoup(html)

			tabledata = soup.find('table', {'class': 'roster_dgrd'}) #find the proper table
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
			team = 'Syracuse'

			current_team = Team.objects.get(name=team)
			current_team.twitter = 'SyracuseMBB'
			current_team.color = '#FF5A00'
			current_team.save()


			for link in tabledata.find_all('a'):
				player_links.append(link.get('href'))
				# print link.get('href')
				player_names.append(link.get_text())
				name = link.get_text()

			for number in tabledata.find_all('td', {'class': 'roster_dgrd_no'}):
				player_numbers.append(number.get_text().strip())

			for height in tabledata.find_all('td', {'class': 'roster_dgrd_height'}):
				player_heights.append(height.get_text())

			for weight in tabledata.find_all('td', {'class': 'roster_dgrd_rp_weight'}):
				player_weights.append(weight.get_text())

			
			# for number in tabledata.select('td.odd')[0]:
				# number = oddrow[0::0]
				# player_numbers.append(number.strip())
			
			# print player_numbers

			for player_link, val in enumerate(player_links):
				# print team_link, val, team_count
				headers = { 'User-Agent' : 'Mozilla/5.0' }
				req = urllib2.Request('http://www.cuse.com%s' % (val), None, headers)
				html = urllib2.urlopen(req).read()

				soup = BeautifulSoup(html)

				playerdata = soup.find('table')

				position = playerdata.find(text='Position:').next.next
				player_positions.append(position.text.strip())

				hometown = playerdata.find(text='Hometown:').next.next
				player_hometowns.append(hometown.text.strip())

				highschool = playerdata.find(text='High School:').next.next
				player_highschools.append(highschool.text.strip())

				portrait = playerdata.find('img')
				player_portraits.append('http://www.cuse.com%s' % (portrait.get('src')))

				class_year = playerdata.find(text='Class:').next.next
				player_class_years.append(class_year.text.strip())

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

		self.stdout.write('end of scrapesyracuse.py')