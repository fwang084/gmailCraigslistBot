import requests
import craigslist_get as cl

def check_post(posts_to_email, post, items_budgets):
    for item in items_budgets:
        if item in cl.get_description(post) and cl.get_price(post) < items_budgets[item]:
            posts_to_email.append(post)
            break
def send_posts(posts_to_email, sendInstance, url):
    for post in posts_to_email:
        message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', cl.get_description(post), 'The price is ${price} at {url}'.format(price = cl.get_price(post), url = url))
        sendInstance.send_message('me', message)
def check_for_failure(posts_to_email, sendInstance):
    if len(posts_to_email) == 0:
        message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', 'Nothing new found', 'Will keep looking.')
        sendInstance.send_message('me', message)