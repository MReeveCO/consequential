from bs4 import BeautifulSoup
import requests

url = 'https://www.legislation.gov.uk/ukpga/2023/41/notes/division/7/index.htm'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html')

article = soup.find("article")

children = article.findChildren()

currentSection = None
for child in children:
    print(child.attrs)


