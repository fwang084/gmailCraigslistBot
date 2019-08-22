from __future__ import print_function
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


from oauth2client import tools

import httplib2
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
import auth

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE  = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python'
authInst = auth.auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

import send_email
import craigslist_get as cl
import time
url = 'https://sfbay.craigslist.org/search/eby/fua'
sendInstance = send_email.send_email(service)

#Getting user input for interested items
items_budgets = {}
while True:
    item = input("Type an item you are interested in: ")
    budget = int(input("What is the most you are willing to spend on that item (in dollars)? "))
    items_budgets[item] = budget
    another = input("Enter Y to enter another item, N if you are done.")
    if another == "N":
        break
duration = float(input("How many hours do you want to search for?"))
halfHours = round(duration * 2)
iterations = 0
previous_last_seen = 0
for x in range(halfHours):
    posts = cl.get_posts_on_page(url)
    posts_to_email = []
    current_last_seen = posts[0]
    if iterations == 0:
        for x in range(len(posts)):
            for item in items_budgets:
                if item in cl.get_description(posts[x]) and cl.get_price(posts[x]) < items_budgets[item]:
                    posts_to_email.append(posts[x])
                    break
    else:
        for x in range(len(posts)):
            if posts[x] == previous_last_seen:
                break
            for item in items_budgets:
                if item in cl.get_description(posts[x]) and cl.get_price(posts[x]) < items_budgets[item]:
                    posts_to_email.append(posts[x])
                    break
    for post in posts_to_email:
        message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', cl.get_description(post), 'The price is ${price} at {url}'.format(price = cl.get_price(post), url = url))
        sendInstance.send_message('me', message)
    if len(posts_to_email) == 0:
        message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', 'Nothing found', 'Will keep looking.')
        sendInstance.send_message('me', message)
    previous_last_seen = current_last_seen
    iterations += 1
    time.sleep(5)
message = sendInstance.create_message('frankw084084@gmail.com', 'frankw084084@gmail.com', 'Searching completed', 'Restart program to resume searching')
sendInstance.send_message('me', message)

