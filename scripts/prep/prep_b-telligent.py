# Import Libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Extract Links from first page
url = "https://www.btelligent.com/blog/"
# Make the request to a url
r = requests.get(url)
# Create soup from content of request
c = r.content
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

links = []
links_cleaned = []
for a in soup.find_all('a', href=True):
    links.append(a["href"])
    #print("Found the URL:", a['href'])
    for link in links:
      link_splitted = link.split("/")
      if len(link_splitted) == 4 and link_splitted[1] == "blog":
          links_cleaned.append(link)
      else:
        pass

links_firstpage= list(dict.fromkeys(links_cleaned))
links_firstpage
# Get Dates from first page
dates = []
for a in soup.find_all('time'):
    date = cleanhtml(str(a))
    date = date.replace("[", "")
    date = date.replace("]","")
    date = date.replace("\n", "")
    date = date.replace("\t", "")
    dates.append(a)

dates_firstpage = dates
url = "https://www.btelligent.com/blog/page/"
end_url = "/"
# Make the request to a url
r = requests.get(url)

# Create soup from content of request
c = r.content

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
# Add Links from other pages
url = "https://www.btelligent.com/blog/page/"
end_url = "/"
# Make the request to a url
r = requests.get(url)
# Create soup from content of request
c = r.content
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

links_cleaned = []
for i in range(2,11):
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
          if len(link_splitted) == 4 and link_splitted[1] == "blog":
              links_cleaned.append(link)
          else:
              pass

links_cleaned = list(dict.fromkeys(links_cleaned))
for element in links_firstpage:
  links_cleaned.append(element)

dates_cleaned = []
for i in range(2,11):
  i = str(i)
  url_new = str(url+i+end_url)
  page = requests.get(url_new)
  soup = BeautifulSoup(page.content, 'html.parser')
  dates = []
  #links_cleaned = []

  for a in soup.find_all('time'):
      a = cleanhtml(str(a))
      a = a.replace("[", "")
      a = a.replace("]","")
      a = a.replace("\n", "")
      a = a.replace("\t", "")
      dates_cleaned.append(a)

for element in dates_firstpage:
  dates_cleaned.append(element)

#dates = []
headers = []
bodies = []
authors = []

for element in urls:
  url = element
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  author = str(soup.find_all("span", class_ = "card-name"))
  author = cleanhtml(author)
  author = author.replace("[", "")
  author = author.replace("]", "")
  authors.append(author)

  header = str(soup.find_all("h1"))
  header = cleanhtml(header)
  header = header.replace("[", "")
  header = header.replace("]", "")
  header = header.replace("\n", "")
  headers.append(header)

  #date = str(soup.find_all("time", class_ ="entry-date published updated"))
  #date = cleanhtml(date)
  #date = date.replace("[", "")
  #date = date.replace("]","")
  #dates.append(date)

  text = str(soup.find_all("p", class_ = ""))
  text = cleanhtml(text)
  text = text.replace("[", "")
  text = text.replace("]", "")
  text = text.replace("\xa0", "")
  text = text.replace("\n", "")
  #header = header.replace("\n", "")
  bodies.append(text)

btelligent_blog = pd.DataFrame()
btelligent_blog["Datum"] = dates_cleaned
btelligent_blog["Titel"] = headers
btelligent_blog["Text"] = bodies
btelligent_blog["Link"] = urls
btelligent_blog["Quelle"] = "B-Telligent"
btelligent_blog["Autor"] = authors

btelligent_blog.to_csv("../data/raw/blogs/Articles_BTelligentBlog", index = False, sep=";")
