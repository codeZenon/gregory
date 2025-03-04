import feedparser
from dateutil.parser import parse
from dotenv import load_dotenv
from .models import Articles,Trials,Sources,Authors
from django_cron import CronJobBase, Schedule
import requests
from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from db_maintenance.unpaywall import unpaywall_utils
from sitesettings.models import *
from crossref.restful import Works, Etiquette
import os
import gregory.functions as greg
from gregory.classes import SciencePaper
from django.utils import timezone
import pytz
SITE = CustomSetting.objects.get(site__domain=os.environ.get('DOMAIN_NAME'))
CLIENT_WEBSITE = 'https://' + SITE.site.domain + '/'
my_etiquette = Etiquette(SITE.title, 'v8', CLIENT_WEBSITE, SITE.admin_email)
works = Works(etiquette=my_etiquette)

def remove_utm(url):
	u = urlparse(url)
	query = parse_qs(u.query, keep_blank_values=True)
	query.pop('utm_source', None)
	query.pop('utm_medium', None)
	query.pop('utm_campaign', None)
	query.pop('utm_content', None)
	u = u._replace(query=urlencode(query, True))
	return urlunparse(u)

class FeedReaderTask(CronJobBase):
	RUN_EVERY_MINS = 30
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'gregory.feedreadertask'    # a unique code

	def do(self):
		###
		# GET ARTICLES
		###
		sources = Sources.objects.filter(method='rss',source_for='science paper')

		for i in sources:
			source_name = i.name
			source_for = i.source_for
			link = i.link
			d = None
			if i.ignore_ssl == False:
				d = feedparser.parse(link)
			else:
				response = requests.get(link, verify=False)
				d = feedparser.parse(response.content)
			for entry in d['entries']:
				summary = ''
				if hasattr(entry,'summary_detail'):
					summary = entry['summary_detail']['value']
				if hasattr(entry,'summary'):
					summary = entry['summary']
				published = entry.get('published')
				if source_name == 'PubMed' and hasattr(entry,'content'):
					summary = entry['content'][0]['value']
				if published:
					published = parse(entry['published'])
				else:
					published = parse(entry['prism_coverdate'])
				link = remove_utm(entry['link'])
				###
				# This is a bad solution but it will have to do for now
				###
				doi = None
				if source_name == 'PubMed':
					if entry['dc_identifier'].startswith('doi:'):
						doi = entry['dc_identifier'].replace('doi:','')
				if source_name == 'FASEB':
					doi = entry['prism_doi']
				paper = SciencePaper(doi)
				try:
					science_paper = Articles.objects.create(discovery_date=timezone.now(), title = entry['title'], summary = summary, link = link, published_date = published, source = i, doi = doi, kind = source_for)
					if paper != None:
						science_paper.access=paper.access
						science_paper.container_title = paper.journal
						science_paper.publisher = paper.publisher
						if paper.abstract != None:
							science_paper.summary = paper.abstract
						science_paper.save()
						# get author information
						for author in paper.authors:
							if 'given' in author and 'family' in author:
								given_name = None
								if 'given' in author:
									given_name = author['given']
								family_name = None
								if 'family' in author:
									family_name = author['family']
								orcid = None
								if 'ORCID' in author:
									orcid = author['ORCID']
								# get or create author
								author_obj = Authors.objects.get_or_create(given_name=given_name,family_name=family_name,ORCID=orcid)
								author_obj = author_obj[0]
								## add to database
								if author_obj.author_id is not None:
									# make relationship
									science_paper.authors.add(author_obj)
						science_paper.save()
						# the articles variable needs to be a queryset list in order to be turned into a pandas dataframe
						greg.predict(articles=Articles.objects.filter(pk=science_paper.article_id))
				except:
					pass

		###
		# GET TRIALS
		###
		sources = Sources.objects.filter(method='rss',source_for='trials')

		for i in sources:
			source_name = i.name
			source_for = i.source_for
			link = i.link
			d = None
			if i.ignore_ssl == False:
				d = feedparser.parse(link)
			else:
				response = requests.get(link, verify=False)
				d = feedparser.parse(response.content)
			for entry in d['entries']:
				summary = ''
				if hasattr(entry,'summary_detail'):
					summary = entry['summary_detail']['value']
				if hasattr(entry,'summary'):
					summary = entry['summary']
				published = entry.get('published')
				if published:
					published = parse(entry['published'])
				link = remove_utm(entry['link'])
				try:
					trial = Trials.objects.create( discovery_date=timezone.now(), title = entry['title'], summary = summary, link = link, published_date = published)
				except:
					pass
