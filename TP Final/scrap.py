import requests
from bs4 import BeautifulSoup
import cloudscraper
import re

def get_problems(scraper, url):
	#Obtención de los divs que contienen los datos de cada problema.
	info = scraper.get(url).text
	soup = BeautifulSoup(info, "html.parser")
	divs = soup.find_all('div')

	#Obtención de texto de problemas.
	texts = [data.get_text() for data in divs]
	texts_re = [re.sub("\n", " ", text) for text in texts]

	#Split y obtención de los problemas
	sentences = [text.split("\t") for text in texts_re]
	sentences_flat = [subsen for sen in sentences for subsen in sen]
	sentences_re = [re.sub("/\s\s+/g"," ", sen) for sen in sentences_flat]
	sentences_filter = [sen for sen in sentences_re if "Problema" in sen]

	#Split extra por si las moscas.
	problems = sentences_filter[-3:]
	problems = [p.split("Problema") for p in problems]
	problems_flat = [p for ps in problems for p in ps]
	problems_re = [re.sub(' +', ' ', p) for p in problems_flat]
	problems_filter = [p for p in problems_re if p != " "]

	return sorted(list(set(problems_filter)))