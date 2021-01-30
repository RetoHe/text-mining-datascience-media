# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

url = "https://www.statworx.com/de/blog/"
# Make the request to a url
r = requests.get(url)
# Create soup from content of request
c = r.content

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# Get Links first page
links = []
links_cleaned = []
for a in soup.find_all('a', href=True):
    links.append(a["href"])
    #print("Found the URL:", a['href'])
    for link in links:
      link_splitted = link.split("/")
      if len(link_splitted) == 7 and link_splitted[4] == "blog":
          links_cleaned.append(link)
      else:
        pass

links_cleaned = list(dict.fromkeys(links_cleaned))
linksfirstpage = links_cleaned
# Get Links from other pages
links_cleaned = []
for i in range(2,25):
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
          if len(link_splitted) == 7 and link_splitted[4] == "blog":
              links_cleaned.append(link)
          else:
              pass
# Add Links together
for element in linksfirstpage:
  links_cleaned.append(element)

dates = []
headers = []
bodies = []
authors = []
# Loop for extracting necessary information
for element in links_cleaned:
  url = element
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  author = str(soup.find_all("span"))
  author = cleanhtml(author)
  author = author.replace("[", "")
  author = author.replace("]", "")
  author = author.replace("\n", "")
  #author = author.replace(",","")
  author = author.split(",")
  #if len(author) < 7:
      #author = ""
  #else:
  author = author[7]
  authors.append(author)

  header = str(soup.find_all("h1"))
  header = cleanhtml(header)
  header = header.replace("[", "")
  header = header.replace("]", "")
  header = header.replace("\n", "")
  header = header.replace("&amp;", "und")
  header = header.split(",")
  header = header[0]
  headers.append(header)

  date = str(soup.find_all("span"))
  date = cleanhtml(date)
  date = date.replace("[", "")
  date = date.replace("]","")
  date = date.replace("\n", "")
  date = date.split(",")
  date = date[8]
  dates.append(date)

  
  text = str(soup.find_all("div", class_ = "entry-content content"))
  text = cleanhtml(text)
  text = text.replace("[", "")
  text = text.replace("]","")
  text = text.replace("\xa0","")
  text = text.replace("\n", "")
  bodies.append(text)

# Create New Dataframe
statworx_blog = pd.DataFrame()
statworx_blog["Datum"] = dates
statworx_blog["Titel"] = headers
statworx_blog["Text"] = bodies
statworx_blog["Link"] = links_cleaned
statworx_blog["Quelle"] = "Statworx"
statworx_blog["Autor"] = authors

# Export CSV- File
statworx_blog.to_csv("../data/raw/blogs/Articles_StatworxBlog.csv", index = False)