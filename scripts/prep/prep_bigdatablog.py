# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

url = "https://bigdatablog.de/2014/03/05/asos-setzt-auf-big-data/"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)

links = []
for a in soup.find_all('a', href=True):
    links.append(a["href"])
    print("Found the URL:", a['href'])

dates = []
headers = []
bodies = []
authors = []

for element in links:
  url = element
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  author = str(soup.find_all("span", class_ ="name"))
  author = cleanhtml(author)
  author = author.replace("[", "")
  author = author.replace("]", "")
  author = author.replace("\n", "")
  author = author.split(",")
  author = author[0]
  authors.append(author)

  header = str(soup.find_all("h1"))
  header = cleanhtml(header)
  header = header.replace("[", "")
  header = header.replace("]", "")
  header = header.replace("\n", "")
  header = header.replace("&amp;", "und")
  headers.append(header)

  date = str(soup.find_all("span", class_ ="date"))
  date = cleanhtml(date)
  date = date.replace("[", "")
  date = date.replace("]","")
  dates.append(date)

  
  text = str(soup.find_all("span"))
  text = cleanhtml(text)
  text = text.replace("[", "")
  text = text.replace("]","")
  text = text.replace("\xa0","")
  #header = header.replace("\n", "")
  bodies.append(text)

bigdatablog = pd.DataFrame()
bigdatablog["Datum"] = dates
bigdatablog["Titel"] = headers
bigdatablog["Text"] = bodies
bigdatablog["Link"] = links
bigdatablog["Quelle"] = "Big Data Blogs"
bigdatablog["Autor"] = authors

# Export CSV File
bigdatablog.to_csv("../data/raw/blogs/BigDataBlog.csv" = False)