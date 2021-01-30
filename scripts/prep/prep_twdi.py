# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

url = "https://blog.tdwi.eu/page/"
end_url = "/"
# Make the request to a url
r = requests.get(url)
# Create soup from content of request
c = r.content
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Extract Links from first page
links = []
links_cleaned = []
for a in soup.find_all('a', href=True):
    links.append(a["href"])
    #print("Found the URL:", a['href'])
    for link in links:
      link_splitted = link.split("/")
      if len(link_splitted) ==  5:
          links_cleaned.append(link)
      else:
        pass

links_cleaned = list(dict.fromkeys(links_cleaned))
links_cleaned = links_cleaned[6:]
del links_cleaned[1::2] 
linksfirstpage = links_cleaned
# Add Urls from other pages
links_cleaned = []
for i in range(2,7):
  i = str(i)
  url_new = str(url+i+end_url)
  page = requests.get(url_new)
  soup = BeautifulSoup(page.content, 'html.parser')
  links = []
  #links_cleaned = []

  for a in soup.find_all('a', href=True):
      links.append(a["href"])
      #print("Found the URL:", a['href'])
      for link in links:
          link_splitted = link.split("/")
          if len(link_splitted) == 5:
              links_cleaned.append(link)
          else:
              pass

links_cleaned = list(dict.fromkeys(links_cleaned))
links_cleaned = links_cleaned[3:]
for element in linksfirstpage:
  links_cleaned.append(element)

dates = []
headers = []
bodies = []
authors = []

for element in links_cleaned:
  url = element
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  author = str(soup.find_all("span", class_ = "author-name"))
  author = cleanhtml(author)
  author = author.replace("[", "")
  author = author.replace("]", "")
  authors.append(author)

  header = str(soup.find_all("h1", class_ ="entry-title"))
  header = cleanhtml(header)
  header = header.replace("[", "")
  header = header.replace("]", "")
  header = header.replace("\n", "")
  headers.append(header)

  date = str(soup.find_all("time", class_ ="entry-date published updated"))
  date = cleanhtml(date)
  date = date.replace("[", "")
  date = date.replace("]","")
  dates.append(date)

  text = str(soup.find_all("p", class_ = ""))
  text = cleanhtml(text)
  text = text.replace("[", "")
  text = text.replace("]", "")
  text = text.replace("\xa0", "")
  text = text.replace("\n", "")
  #header = header.replace("\n", "")
  bodies.append(text)

# Create New Dataframe
twdi_blog = pd.DataFrame()
twdi_blog["Datum"] = dates
twdi_blog["Titel"] = headers
twdi_blog["Text"] = bodies
twdi_blog["Link"] = links_cleaned
twdi_blog["Quelle"] = "TDWI"
twdi_blog["Autor"] = authors

# Export CSV File
twdi_blog.to_csv("../data/blogs/TDWIBlog.csv", index = False)
