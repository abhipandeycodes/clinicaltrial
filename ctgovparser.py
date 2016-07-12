
"""
The following function will take raw input from the user
describing a 'disease' (e.g. "breast cancer"). That raw input
will be fed into a relative url, which will be concatenated to
a base url for clinicaltrials.gov. Using that URL, the program
will search for clinical trials for the user-defined 'disease'.
The program will then iterate through PAGES of clinical trial search results, and: 
1) create a list of clinical trials
2) iterate through the list to find the trial's 'recruiting status' 
3) store each 'recruiting status' in a dedicated list
4) navigate to the next page of results and repeate steps 1-3. 

go through each url in ct_list and: 
1) store the html content within a python object
2) from the html; 
	a) find the "recruiting-status" and store it within a dictionary
	b) find the "info-date" corresponding to when the trial was "last updated",
		and store that value within a dictionary. 
		**Note: .startswith() can be applied to strings !!

{status: "Recruiting", "Unknown", "Active, not recruiting", "Completed", "Recruiting",
"Not yet recruiting"}

Because each search results page returns 20 results, the program must navigate to the next page of 
results. Below is the relative URL to get to the next page. 
<a title="Show next page of results" href="/ct2/results?term=breast+cancer&amp;pg=2">Next Page (21-40)</a>
1) Find and parse out thet relative URL. 
2) Use requests.get() to access that URL. 
3) Iterate through the contents of the page and extrace + store 
recrutiment statuses for each trial.
"""
import requests
from bs4 import BeautifulSoup
import re 

def getRecruitmentStatus():
	term = raw_input('Please type a disease name: ')
	base_url = "https://clinicaltrials.gov"
	brca_xml = requests.get("https://clinicaltrials.gov/ct2/results?term={0}+&Search=Search".format(term)).text
	brca_soup = BeautifulSoup(brca_xml, 'lxml')
	a_tags = brca_soup.find_all('a')
	ct_list = list()
	for x in a_tags: 
		if re.search('NCT', x['href']):
			ct_list.append(base_url + x['href'])
		else: 
			continue
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
	while brca_soup.find_all(title=re.compile('Show next page of results')): 
		next_page_links_list = brca_soup.find_all(title=re.compile('Show next page of results'))
		next_page_href = next_page_links_list[0]['href']
		print next_page_href
		next_page_url = base_url + next_page_href
		print next_page_url
		brca_xml = requests.get(next_page_url).text
		brca_soup = BeautifulSoup(brca_xml, 'lxml')
		a_tags = brca_soup.find_all('a')
		ct_list = list()
		for x in a_tags: 
			if re.search('NCT', x['href']):
				ct_list.append(base_url + x['href'])
			else: 
				continue
				#return ct_list
		for trial in ct_list:
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
	return recruiting
	return not_recruiting
	return unknown_recruiting_status

getRecruitmentStatus()


#need to look up Object Relational Model on Github. 