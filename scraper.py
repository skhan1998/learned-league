#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 16:14:00 2018

@author: samirkhan
"""

#This file contains all functions for scraping data from the LL website

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def half_strip(q):
    q = q.decode("utf-8")

    puncs = ["<i>", "</i>", "<b>", "</b>", r'\xa0']
    for p in puncs:
        q = q.replace(p, "")

    q = q.replace("_", "-")
    q = q.replace(u"\u2014", " ")
    q = q.replace(u"\xa0", " ")

    q = q.replace("#", r'\#')
    q = q.replace("&", r'\&')
    q = q.replace("%", r'\%')

    if "href" in q:
        q = q.split("<")[0] + q.split(">")[-1]

    return q

def strip(q):
    q = q.decode("utf-8")

    puncs = [",", "'", ".", r'"', "?", "&", "<i>", "</i>", "<b>", "</b>", ":", ")", "(", "_", r'\xa0', "\n"]
    for p in puncs:
        q = q.replace(p, "")

    q = q.replace("-", " ")
    q = q.replace(u"\u2014", " ")
    q = q.replace(u"\xa0", " ")

    if "href" in q:
        q = q.split("<")[0] + q.split(">")[-1]

    return q

def scrape_history(player, payload):
    with requests.Session() as s:
        s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
        qhist = s.get('https://www.learnedleague.com/profiles/qhist.php?%s' % player.lower())
        soup = BeautifulSoup(qhist.content, "html.parser")

    df_rows = []

    lis = soup.find_all("li")
    for li in lis[::2]:

        category = re.findall(r">(.+)<ul>", str(lis[0]))[0]
        rows = li.find_all("tr")
        rows.pop(0)

        for row in rows:
            cols = row.find_all("td")
            q = re.findall(">(.+)<", str(cols[1]))[0]

            c = 1 if "greendot" in str(cols[2]) else 0
            df_rows.append([category, half_strip(q), strip(q.lower()), c])

    df = pd.DataFrame(df_rows, columns = ["Category", "Raw Question", "Question", "Correct?"])

    return df

def scrape_match(league, day, payload):
    with requests.Session() as s:
        s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
        qhist = s.get('https://www.learnedleague.com/match.php?%s&%s' % (league, day))
        soup = BeautifulSoup(qhist.content, "html.parser")

    qs = list(soup.find_all("span"))
    qs = [q.get_text() for q in qs if "id" in q.attrs]

    raw_qs = [half_strip(q) for q in qs]
    qs = [strip(q) for q in qs]

    return raw_qs, qs
