import requests
from bs4 import BeautifulSoup

import re
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Link, Snapshot, Base

import os
import time

import pprint


def extract_info(link,timestamp):
    try:
        comments = re.sub(r' comments?','',link.next_sibling()[6].text)
        comments = 0 if comments == 'discuss' else comments
    except IndexError:
        comments = 0

    points = [i.select('.score')[0] for i in link.next_sibling() if i.select('.score')]
    if len(points) == 1:
        points = re.sub(r' points?','',points[0].text)
    else:
        points = 0

    position = link.select('.rank')[0].text.replace('.','')

    if isinstance(int(position),int) and isinstance(int(points),int) and isinstance(int(comments),int):
        pass
    else:
        raise Exception('damn: {} {} {}'.format(comments,points,position))

    try:
        domain = link.find("span","sitestr").text
    except AttributeError:
        domain = 'news.ycombinator.com'

    return {
        'position'   : position,
        'url'        : link.find_all("td","title")[1].a["href"],
        'title'      : link.find_all("td","title")[1].a.text,
        'points'     : points,
        'comments'   : comments,
        'user'       : link.next_sibling()[3].text,
        'item_id'    : link.next_sibling()[1].find("a",href=re.compile('item\?id='))["href"].split('=')[1],
        'domain'     : domain,
        'created_at' : timestamp
    }


def get_links(page=1,links=[]):

    if page==1:
        url = 'http://news.ycombinator.com'
    else:
        url = 'https://news.ycombinator.com/news?p={}'.format(page)

    r = requests.get(url)
    html = r.text
    soup  = BeautifulSoup(html,"html5lib")

    links = links + soup.find_all('tr',"athing")

    if page == 5:
        return links
    else:
        return get_links(page+1,links)


def process_links(DBSession):
    links = get_links()
    timestamp = int(time.time())
    data  = [extract_info(link,timestamp) for link in links]

    session = DBSession()

    for d in data:
        print("Processing {} --- ".format(d['url']))

        link = Link(id=d['item_id'], url=d['url'], title=d['title'], user=d['user'], domain=d['domain'])
        session.merge(link)

        snapshot = Snapshot(link_id=d['item_id'], comments=d['comments'], points=d['points'], position=d['position'])

        session.add(snapshot)

    session.close()
    pprint.pprint(data)


if __name__ == "__main__":

    # export DB_URL=postgresql://dn_user:db_pass@db_host/db_name
    db_url = os.getenv('DB_URL')
    engine = create_engine(db_url)

    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine, autocommit=True)

    while True:
        process_links(DBSession)
        print('sleeping for two minutes')
        time.sleep(120)





