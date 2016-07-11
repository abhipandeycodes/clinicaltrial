import requests
from bs4 import BeautifulSoup
import re

def getClinicalTrialsUrl(brca_xml):
	brca_soup = BeautifulSoup(brca_xml, 'lxml')
	a_tags = brca_soup.find_all('a')
	ct_list = list()
	base_url = "https://clinicaltrials.gov"
	for x in a_tags: 
		if re.search('NCT', x['href']):
			ct_list.append(base_url + x['href'])
		else: 
			continue
	return ct_list
	
def getRecruitingStatus(ct_list):
	recruiting = {}
	not_recruiting = {}
	unknown_recruiting_status = {}
	for trial in ct_list:
		#print trial
		trial_url = requests.get(trial).text
		trial_soup = BeautifulSoup(trial_url, 'lxml')
		if trial_soup.find('div', 'not-recruiting-status'):
			not_recruiting[trial] = str(trial_soup.find('div', 'not-recruiting-status').contents[0]).rstrip()
		elif trial_soup.find('div', 'recruiting-status'):
			recruiting[trial] = str(trial_soup.find('div', 'recruiting-status').contents[0]).rstrip()
		elif trial_soup.find('div', 'unknown-recruiting-status'):
			unknown_recruiting_status[trial] = str(trial_soup.find('div', 'unknown-recruiting-status').contents[0]).rstrip()
		else: 
			print "no recruitment text found"
	print "There are", len(recruiting), "trials that are recruiting currently!"
	print "There are", len(not_recruiting), "trials that are NOT recuriting"
	print "For", len(unknown_recruiting_status), "trials, the recruiting status is unknown"
	return brca_soup
	return recruiting
	return not_recruiting
	return unknown_recruiting_status
	


def getClinicalTrialXml():
	term = raw_input('Please type a disease name: ')
	brca_xml = requests.get("https://clinicaltrials.gov/ct2/results?term={0}+&Search=Search".format(term)).text
	brca_soup = BeautifulSoup(brca_xml, 'lxml')
	return brca_soup
	return brca_xml

def getNextPage(brca_soup):
	next_page_links_list = brca_soup.find_all(title=re.compile('Show next page of results'))
	next_page_href = next_page_links_list[0]['href']
	next_page_url = base_url + next_page_href
	brca_xml = requests.get(next_page_url)
	return brca_xml 


	#print "There are", len(recruiting), "trials that are recruiting currently!"
	#print "There are", len(not_recruiting), "trials that are NOT recuriting"
	#print "For", len(unknown_recruiting_status), "trials, the recruiting status is unknown"

getRecruitmentStatus()
