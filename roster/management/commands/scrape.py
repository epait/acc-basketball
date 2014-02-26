from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
from roster.models import Team

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
			stat_links = []
			team_count = 0
			team_conference_records = []
			team_overall_records = []
			team_conference = 'ACC'

			for link in tabledata.select('a'):
				team_links.append(link.get('href'))
				team_names.append(link.get_text())
				name = link.get_text()
				team_conference_records.append(soup.find(text=name).next.text)
				team_overall_records.append(soup.find(text=name).next.next.next.next.next.next.next.text)



			for team_link, val in enumerate(team_links):
				# print team_link, val, team_count
				response = urllib2.urlopen('http://espn.go.com', val)
				html = response.read()
				soup = BeautifulSoup
				print team_names[team_count]
				team_data = Team.objects.create(name= team_names[team_count], conference= team_conference, conference_record= team_conference_records[team_count], overall_record= team_overall_records[team_count])
				team_data.save()
				team_count += 1


			# print team_names
			# print team_conference_records
			# print team_overall_records

		except Team.DoesNotExist:
			raise CommandError('Didn\'t work')

		self.stdout.write('end of scrape.py')