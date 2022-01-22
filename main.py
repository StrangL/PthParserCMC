import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import yagooglesearch
#from selenium import webdriver


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36',
           'accept': '*/*'}
HOST = 'https://coinmarketcap.com/'

names_of_projects = ['CTK', 'WING', 'CHR', 'CAKE', 'OXT', 'MIR', 'SRM', 'SKL', 'COTI',
                     'TRB', 'ALGO', 'EGLD', 'ONT', 'FIS', 'REN', 'OOKI', 'OGN', 'FET', 'CTSI']

FILE = 'projects.csv'
FILE2 = 'projects_that_michael_likes.csv'


def get_urls(names):
    urls = []
    for i in range(len(names)):
        url = search(names[i]+' coinmarketcap', num_results=0)[0]
        urls.append(url)
        time.sleep(3)
    return urls


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def save_file(projects, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for project in projects:
            writer.writerow([project['title']])
            writer.writerows([project['tags']])


def save_names(projects, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for project in projects:
            writer.writerow([project['title']])


def get_content(names):
    urls = get_urls(names)
    projects = []
    i = 0
    for url in urls:
        html = get_html(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        item = soup.find('div', class_='top-summary-container')
        projects.append({
            'title': item.find('h2', class_='h1').get_text('|'),
            'tags': [x.get_text() for x in item.find_all('div', attrs={'class': 'tagBadge'})]
        })
        projects[i]['tags'] = list(set(projects[i]['tags']))
        '''projects[i]['tags'] = [x
            for x in projects[i]['tags']
            if not isinstance(x, int)
        ]'''
        i += 1
    return projects


def create_matchers():
    df = pd.read_csv('list.csv')  # can also index sheet by name or fetch all sheets
    matchers = df['matchers'].tolist()
    return matchers


def linear_search(projects, matchers):
    project_which_michael_likes = []
    for i in range(len(projects)):
        tmp = [s for s in projects[i]['tags'] if any(xs in s for xs in matchers)]
        if bool(tmp):
            project_which_michael_likes.append(projects[i])
    return project_which_michael_likes


def parse():
    projects = get_content(names_of_projects)
    #print(projects)

    matchers = create_matchers()
    projects_which_michael_likes = linear_search(projects, matchers)
    print(projects_which_michael_likes)
    save_names(projects_which_michael_likes, FILE2)


parse()
