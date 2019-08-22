from requests import get
from bs4 import BeautifulSoup

def get_posts_on_page(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    posts = html_soup.find_all('li', class_= 'result-row')
    return posts
def get_price(post):
    if len(post.a.text[2:]) > 0: #Checking if a price was listed
        return int(post.a.text[2:])
    return 99999999 #If there is no price listed, do not consider
def get_description(post):
    return post.find('a', class_='result-title hdrlnk').text.lower()