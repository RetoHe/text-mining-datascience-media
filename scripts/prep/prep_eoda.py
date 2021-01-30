# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

url = "https://www.eoda.de/wissen/blog/"
# Make the request to a url
r = requests.get(url)
# Create soup from content of request
c = r.content
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Get Datum Eoda Blog
dates = []
for a in soup.find_all('p', class_="blogoverview__date"):
    a = cleanhtml(str(a))
    dates.append(a)

# Get Links Eoda Blog
links = []
for a in soup.find_all('a', href=True):
    links.append(a["href"])

# Create Urls
url_begin = "https://www.eoda.de"
urls = []
for link in correct_links:
  link = str(link)
  url_total = url_begin+link
  urls.append(url_total)
# Filter correct Links
correct_links = links[59:83]

# Loop for extracting necessary Data
#dates = []
headers = []
bodies = []
#authors = []

for element in correct_links:
  url = element
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  #author = str(soup.find_all("span", class_ ="name"))
  #author = cleanhtml(author)
  #author = author.replace("[", "")
  #author = author.replace("]", "")
  #author = author.replace("\n", "")
  #author = author.split(",")
  #author = author[0]
  #authors.append(author)

  header = str(soup.find_all("h1"))
  header = cleanhtml(header)
  header = header.replace("[", "")
  header = header.replace("]", "")
  header = header.replace("\n", "")
  header = header.replace("&amp;", "und")
  headers.append(header)

  #date = str(soup.find_all("span", class_ ="date"))
  #date = cleanhtml(date)
  #date = date.replace("[", "")
  #date = date.replace("]","")
  #dates.append(date)

  
  text = str(soup.find_all("span"))
  text = cleanhtml(text)
  text = text.replace("[", "")
  text = text.replace("]","")
  text = text.replace("\xa0","")
  #header = header.replace("\n", "")
  bodies.append(text)

  # Create New Dataframe
  eodablog = pd.DataFrame()
eodablog["Datum"] = dates
#eodablog["Titel"] = headers
#eodablog["Text"] = bodies
eodablog["Link"] = correct_links
#eodablog["Quelle"] = "EODA"
#eodablog["Autor"] = ""

# Export CSV File
eodablog.to_csv("../data/raw/blogs/Articles_EODA-Blog", index = False, sep= ";")