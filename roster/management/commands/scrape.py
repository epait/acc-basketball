from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team, Player, SeasonStats

#below imports only needed if from URL
import urllib2
import re

class Command(BaseCommand):
	args = '<url>'
	help = 'Parses and imports ACC teams from espn.com'

	def handle(self, *args, **options):
		try:
			print('starting to scrape')


			#use code below when file to import is on web server
			response = urllib2.urlopen("http://espn.go.com/mens-college-basketball/conferences/standings/_/id/2/acc-conference")
			html = response.read()

			#end server version


			#use this code when file is local:
			#with open ('transcript.html', 'r') as tempFile:
			#html=tempFile.read()

			#end local version
			#print html

			soup = BeautifulSoup(html)

			tabledata = soup.find('table') #find the proper table
			team_names = [] #list to store every player in the table
			team_links = []
			team_count = 0
			team_conference_records = []
			team_overall_records = []
			team_conference = 'ACC'
			team_stats_links = []

			for link in tabledata.find_all('a'):
				team_links.append(link.get('href'))
				team_names.append(link.get_text())

				name = link.get_text()
				team_conference_records.append(link.find(text=name).next.text)
				team_overall_records.append(link.find(text=name).next.next.next.next.next.next.next.text)


				team_url = link.get('href')
				response = urllib2.urlopen(team_url)
				html = response.read()
				soup = BeautifulSoup(html)

				stats = soup.find('a', text='Statistics')
				team_stats_links.append(stats.get('href'))
				# response = urllib2.urlopen('http://espn.go.com', stats_url)
				# html = response.read()
				# soup = BeautifulSoup(html)
				# player_data = soup.find('table')
				# player_names = []

				# for player in player_data.find_all('a'):
				# 	player_names.append(player.get_text())





			for team_stats_link, val in enumerate(team_stats_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://espn.go.com%s' % (val), val)
				html = response.read()
				soup = BeautifulSoup(html, 'html.parser')

				playerdata = soup.find('table')
				player_names = []
				player_count = 0
				player_ppg = []
				player_rpg = []
				player_apg = []
				player_spg = []
				player_bpg = []
				player_tpg = []
				player_fgp = []
				player_ftp = []
				player_tpp = []

				team_data = Team.objects.create(name= team_names[team_count], conference= team_conference, conference_record= team_conference_records[team_count], overall_record= team_overall_records[team_count])
				team_data.save()
				print team_names[team_count], team_overall_records[team_count], team_conference_records[team_count]

				for player in playerdata.select('.evenrow a'):
					player_names.append(player.get_text())
					name = player.get_text()
					player_ppg.append(soup.find(text=name).next.next.next.next.next.text)
					player_rpg.append(soup.find(text=name).next.next.next.next.next.next.next.text)
					player_apg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.text)
					player_spg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.text)
					player_bpg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_tpg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_fgp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_ftp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_tpp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					print player_names[player_count], player_ppg[player_count], player_rpg[player_count], player_apg[player_count], player_spg[player_count], player_bpg[player_count], player_tpg[player_count], player_fgp[player_count], player_ftp[player_count], player_tpp[player_count]
					player_data = Player.objects.create(name= player_names[player_count], team= Team.objects.get(name=team_names[team_count]))
					player_data.save()
					player_stats_data = SeasonStats.objects.create(player= Player.objects.get(name=player_names[player_count]), points_per_game= player_ppg[player_count], rebounds_per_game= player_rpg[player_count])
					player_stats_data.save()

					player_count += 1

				for player in playerdata.select('.oddrow a'):
					player_names.append(player.get_text())
					name = player.get_text()
					player_ppg.append(soup.find(text=name).next.next.next.next.next.text)
					player_rpg.append(soup.find(text=name).next.next.next.next.next.next.next.text)
					player_apg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.text)
					player_spg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.text)
					player_bpg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_tpg.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_fgp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_ftp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					player_tpp.append(soup.find(text=name).next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.next.text)
					print player_names[player_count], player_ppg[player_count], player_rpg[player_count], player_apg[player_count], player_spg[player_count], player_bpg[player_count], player_tpg[player_count], player_fgp[player_count], player_ftp[player_count], player_tpp[player_count]
					player_data = Player.objects.create(name= player_names[player_count], team= Team.objects.get(name=team_names[team_count]))
					player_data.save()
					player_stats_data = SeasonStats.objects.create(player= Player.objects.get(name=player_names[player_count]), points_per_game= player_ppg[player_count], rebounds_per_game= player_rpg[player_count])
					player_stats_data.save()
					
					player_count += 1

				team_count += 1



			# print team_names
			# print player_names
			# print team_conference_records
			# print team_overall_records

		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrape.py')