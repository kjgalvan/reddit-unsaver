#!/usr/bin/env python3.6

import requests
import requests.auth
import request_counter
import pprint
import sys
import webbrowser
import time
import os

#change username and password
username = "reddit_bot"
password = "snoo"
filename = "saveprogress"

#begin ratelimit counter
mycounter = request_counter.Counter()

#request access token and save information
client_auth = requests.auth.HTTPBasicAuth('O0TvVKv68jPB4A', '-N2nJvg2JiIKPpEcYYDq9_V67GU')
post_data = {"grant_type": "password", "username": username, "password": password}
headers = {"User-Agent": "Unsaver by kjgalvan"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
access_token = response.json()['access_token']
token_type = response.json()['token_type']
headers = {"Authorization": token_type + " " + access_token , "User-Agent": "Unsaver by kjgalvan"}

#get max amount of saved posts possible
limit = 100
with open(filename, 'r+') as f:
    after = f.read()

while True:
    parameters = {'after':after,'limit':limit,}
    response = requests.get("http://oauth.reddit.com/user/" + username + "/saved",params=parameters,headers=headers)
    data2 = response.headers
    mycounter.limitused(int(data2['x-ratelimit-used']))
    data = response.json()

#displays a post and waits for input
    for x in range(limit):
        name = data['data']['children'][x]['data']['name']
        a,b = name.split("_")
        if a == 't1':
            print("\n\n" + "Title: " + data['data']['children'][x]['data']['link_title'] + "\n\n" + "Subreddit: " + data['data']['children'][x]['data']['subreddit'] + '\n\n' +
                    data['data']['children'][x]['data']['body'] + "\n\n" + data['data']['children'][x]['data']['link_url'] + b ,sep='')
        elif a == 't3':
            print("\n\n" + "Title: " + data['data']['children'][x]['data']['title'] + '\n\n' + "Subreddit: " + data['data']['children'][x]['data']['subreddit'] + '\n\n' + 
                    data['data']['children'][x]['data']['selftext'] + "\n\n" + "https://www.reddit.com/" + data['data']['children'][x]['data']['permalink'] ,sep='')
        else:
            sys.stdout.write("WTF")

#allows options to keep, unsave, open link, or quit
        while True:
            sys.stdout.write("\nUnsave? [Y/n/o/q]")
            choice = input().lower()
            if choice == '' or choice == 'yes' or choice == 'ye' or choice == 'y':
                if mycounter.ratelimit > 0:
                    requests.post("https://oauth.reddit.com/api/unsave",data={'id':name,}, headers=headers)
                    mycounter.decrease()
                else:
                    while mycounter.ratelimit == 0:
                        time.sleep(1)
                    requests.post("https://oauth.reddit.com/api/unsave",data={'id':name,}, headers=headers)
                    mycounter.decrease()
                    time.sleep(1)
                break
            elif choice == 'no' or choice == 'n':
                with open(filename, 'r+') as f:
                    text = name
                    f.seek(0)
                    f.write(text)
                break
            elif choice == 'quit' or choice == 'q':
                with open(filename, 'r+') as f:
                    text = name
                    f.seek(0)
                    f.write(text)
                os._exit(1)
                thread.interrupt_main()
            elif choice == 'open' or choice == 'o':
                if a == 't1':
                    webbrowser.open_new_tab(data['data']['children'][x]['data']['link_url'] + b)
                elif a == 't3':
                    webbrowser.open_new_tab("https://www.reddit.com/" + data['data']['children'][x]['data']['permalink'])
            else:
                sys.stdout.write("Invalid input")
                                        
        os.system("clear")

