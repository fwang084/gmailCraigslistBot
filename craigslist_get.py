from requests import get

response = get('https://sfbay.craigslist.org/search/eby/fua')
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')

posts = html_soup.find_all('li', class_= 'result-row')
print(type(posts)) #to double check that I got a ResultSet
print(len(posts)) #to double check I got 120 (elements/page)