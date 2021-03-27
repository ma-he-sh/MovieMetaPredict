#!/usr/bin/bash python3
# -*- coding: utf-8 -*-

from api.imdb_api import IMDB_MOVIE_LIST, IMDB_MOVIE, REST
import time
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup as BS
import re

url = ('http://www.imdb.com/search/title?count=220&view=simple'
    '&boxoffice_gross_us=1,&title_type=feature&release_date={year}&view=advanced')

def get_title_id( title_url ):
    imdb_id = re.search('/ev\d{7}\/\d{4}(-\d)?|(ch|co|ev|nm|tt)\d{7}/', title_url )
    if imdb_id:
        imdb_id = imdb_id.group(0).strip('/')
        return imdb_id
    return '-'

def get_movie_list( year ):
    """get movie list for the given year"""
    URL = url.format(year=year)
    print(URL)

    r = requests.get(URL)
    content = r.content

    movie_list = []
    page = BS(content, 'html.parser')
    pageContent = page.find(class_='lister-list')
    if pageContent is not None:
        listerItems = pageContent.findAll('div', class_='lister-item')
        for item in listerItems:
            listerItem = item.find('span', class_='lister-item-header')
            link = listerItem.find('a', href=True)
            movie_list.append( get_title_id( link['href'] ) )
    return movie_list

def save_datafile( file_index, dictionary ):
    with open('./data/dataset_' + str(file_index) + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)

def run_dataset_creator():
    print('---title_data_collector---');
    movieList = get_movie_list(1986)

    # movie = IMDB_MOVIE('tt0095958')
    # data = movie.parse()
    # print(json.dumps( data, indent=4 ))

    # for year in range(1986, 2020):
    #     movieList = get_movie_list(year)
    #     dataset = []
    #     count = 1
    #     file_index = 0
    #     if len(movieList) > 0:
    #         for title in movieList:
    #             print('--collecting--' +  title + '::' + str(count) )
    #             try:
    #             	movie = IMDB_MOVIE(title)
    #             	data = movie.parse()
    #             except Exception as ex:
    #             	print('ERROR', ex)
    #             finally:
    #             	dataset.append(data)
                
    #             time.sleep(0.00001)
    #             count += 1

    #     # save dataset 
    #     save_datafile( year, dataset )
    #     file_index += 1
    #     time.sleep(0.001)

if __name__ == '__main__':
    print('data')
    run_dataset_creator()
