import cloudscraper
from bs4 import BeautifulSoup

class PyPiScraper:
	"""
	Scrap PyPi most relevants packages.

	Example:
	>>> url = https://pypi.org/search/?c=Programming+Language+%3A%3A+Python&c=Topic+%3A%3A+Scientific%2FEngineering&o=&q=&page=1
	>>> scraper = PyPiScraper()
	>>> pkg = scraper.get_packages(url)
	"""
	
	def __init__(self, delay = 10, browser = "chrome"):
		self.scraper = cloudscraper.create_scraper(delay = delay, browser = browser)    

	def get_soup(self, url):
		"""
		Returns soup for a given url.
		"""

		info = self.scraper.get(url).text
		soup = BeautifulSoup(info, "html.parser")
		return soup

	def get_packages(self, url, topic):
		"""
		Returns list of dicts with package info for packages in 'url'.
		"""

		soup = self.get_soup(url)

		#Package info containers
		package_titles = soup.find_all('h3', {"class": "package-snippet__title"})
		packages_info = []

		#Get name, version and date for every package in 'url'. Saves info in 'packages_info'.
		for package in package_titles:
			package_name = package.find('span', {"class": "package-snippet__name"}).get_text()
			package_ver = package.find('span', {"class": "package-snippet__version"}).get_text()
			package_date = package.find('time')["datetime"]
			package_topic = topic

			packages_info.append({"name": package_name, "version": package_ver, "date": package_date, "topic": package_topic})
		
		return packages_info

def pypi_url_maker(topic , min_page = 1, max_page = 11):

	urls = [fr"https://pypi.org/search/?c=Programming+Language+%3A%3A+Python&c=Topic+%3A%3A+{topic}&o=&q=&page={i}" 
			for i in range(min_page, max_page)]
	return urls

if __name__ == "__main__":
	import tqdm
	import json
	import os
	
	master_path = r"C:\Users\juanm\OneDrive\Documentos\GitHub\CoNet\Tp Final\network_building\status_files" #Current .py dir
	os.chdir(master_path)
	
	package_scraper = PyPiScraper() #Init scraper

	packages = []
	max_page = 10
	urls_by_topic = {
		"Science":  pypi_url_maker("Scientific%2FEngineering", max_page = max_page),
		"Internet": pypi_url_maker("Internet", max_page = max_page),
		"Soft Dev": pypi_url_maker("Software+Development", max_page = max_page),
		"Communications": pypi_url_maker("Communications", max_page = max_page),
		"Adaptative Technologies": pypi_url_maker("Adaptive+Technologies", max_page = max_page),
		"Artistic Software": pypi_url_maker("Artistic+Software", max_page = max_page),
		"Database": pypi_url_maker("Database", max_page = max_page),
		"Desktop Enviroment": pypi_url_maker("Desktop+Environment", max_page = max_page),
		"Documentation": pypi_url_maker("Documentation", max_page = max_page),
		"Education": pypi_url_maker("Education", max_page = max_page),
		"Games": pypi_url_maker("Games", max_page = max_page),
		"Home automation": pypi_url_maker("Home+Automation", max_page = max_page),
		"Multimedia": pypi_url_maker("Multimedia", max_page = max_page),
		"Office and Business": pypi_url_maker("Office%2FBusiness", max_page = max_page),
		"Other": pypi_url_maker("Other%2FNonlisted+Topic", max_page = max_page),
		"Printing": pypi_url_maker("Printing", max_page = max_page),
		"Religion": pypi_url_maker("Religion", max_page = max_page),
		"Security": pypi_url_maker("Security", max_page = max_page),
		"Sociology": pypi_url_maker("Sociology", max_page = max_page),
		"System": pypi_url_maker("System", max_page = max_page),
		"Terminals": pypi_url_maker("Terminals", max_page = max_page),
		"Text Editors": pypi_url_maker("Text+Editors", max_page = max_page),
		"Text Processing": pypi_url_maker("Text+Processing", max_page = max_page),
		"Utilities": pypi_url_maker("Utilities", max_page = max_page),
		}

	#total = sum of the amount of urls by topic = number of urls.
	pbar = tqdm.tqdm(total= sum([len(topic_urls) for topic_urls in urls_by_topic.values()]))

	#Execute 'get_packages' for every url.
	for topic, urls in urls_by_topic.items():
		for url in urls:
			packages += package_scraper.get_packages(url, topic) 
			pbar.update(1)

	print(len(packages))
	#Dumps result to json.
	with open('pypi-packages.json', 'w') as fout:
		json.dump(packages , fout)