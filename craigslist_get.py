from requests import get
from bs4 import BeautifulSoup

def get_posts_on_page(url):
    response = get('https://sfbay.craigslist.org/search/eby/fua')
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li', class_= 'result-row')
    return posts
def get_price(post):
    return int(post.a.text[2:])
def get_description(post):
    return post.find('a', class_='result-title hdrlnk').text