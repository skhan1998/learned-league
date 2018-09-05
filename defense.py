#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 13:07:22 2018

@author: samirkhan
"""

import sys
import os
import warnings

from scraper import scrape_history, scrape_match
from neighbors import find_neighbors
from publisher import publish


warnings.filterwarnings("ignore")

if __name__ == "__main__":
    _, league, day, opponent, username, password = sys.argv

    title = "LL%sMD%s_%s_Defense" % (league, day, opponent)
    payload = {
    'username': username,
    'password': password,
    'login': 'Login'}

    df = scrape_history(opponent, payload)
    new = scrape_match(league, day, payload)

    neighbors = find_neighbors(df, new[1])

    publish(neighbors[0], neighbors[1], new[0], title)

    os.system("pdflatex %s.tex" % title)
    os.remove("%s.tex" % title)
    os.remove("%s.aux" % title)
    os.remove("%s.log" % title)
