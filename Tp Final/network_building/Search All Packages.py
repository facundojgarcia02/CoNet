import cloudscraper
import json
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

# Avoid HTTPS warning.
import warnings
warnings.filterwarnings("ignore")

print("Scrapping PyPi/Simple.")

# Scrap all package names.
scraper = cloudscraper.create_scraper(delay = 10, browser = "chrome")
html = scraper.get("https://pypi.org/simple/").text
soup = BeautifulSoup(html, "html.parser")
soup_as = soup.find_all("a")
packages = [a.get_text() for a in soup_as]

print("Scrapped PyPi/Simple.")
print(f"Found {len(packages)}.")

json_path = input("Select a path for saving jsons: ") # r"C:/Users/facuj/OneDrive/Escritorio/full scrap/all jsons/"
json_path += "/"
start = int(input("Select initial package index: "))
end = int(input("Select final package index: "))

print("Searching deps:")

# Request JSON for each package.
not_found = []
for p in tqdm(packages[start:end]):
    try:
        # Try to download json
        url = f'https://pypi.org/pypi/{p}/json'
        package_json = requests.get(url, verify = False).json()

        # Save json
        filename = json_path + p + ".json"
        with open(filename, 'w') as fout:
            json.dump(package_json , fout)

    except: #Save name of not found jsons.
        not_found.append(p)
        print("Package JSON not found:", not_found[-1])

# Save not found JSONS
with open("Not found from simple.txt", 'w') as fp:
    for item in not_found:
        fp.write("%s\n" % item) #Write each element in a new line.

print("Saved found JSON´s.")
