#!/usr/bin/bash python3
# -*- coding: utf-8 -*-

import time
import pandas as pd
import json
import requests
import re
from bs4 import BeautifulSoup as BS
from requests_html import HTMLSession
from api import IMDB_MOVIE, IMDB_EXRACT_SYNOPSIS

#url = ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3AG,US%3APG,US%3APG-13,US%3AR,US%3ANC-17&adult=include&sort=alpha,asc&count=250&start={pagination}&ref_=adv_nxt')
urls = {
	'G' : {
		'url' : ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3AG&adult=include&sort=alpha,asc&count=250&start={pagination}'),
		'count' : 1853
	},
	'PG': {
		'url' : ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3APG&adult=include&sort=alpha,asc&count=250&start={pagination}'),
		'count' :  5664
	},
	'PG-13' : {
		'url' : ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3APG-13&adult=include&sort=alpha,asc&count=250&start={pagination}'),
		'count' : 5864
	},
	'R' : {
		'url' : ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3AR&adult=include&sort=alpha,asc&count=250&start={pagination}'),
		'count' : 1853
	},
	'NC-17' : {
		'url' :  ('https://www.imdb.com/search/title/?title_type=feature,tv_movie&certificates=US%3ANC-17&adult=include&sort=alpha,asc&count=250&start={pagination}'),
		'count' : 74
	}
}

rootURL = 'http://www.imdb.com'
defaultRating = 'NA'
reqURL  = 'NA'

def save_datafile( file_index, dictionary ):
    with open('./data_2/dataset_' + defaultRating + '_' + str(file_index) + '.json', 'w') as f:
        json.dump(dictionary, f, indent=4)

def save_synopsis( file_index, txt_content ):
	f = open( './synopsis_2/' + str( file_index ) + '.txt', 'w' )
	f.write( txt_content )
	f.close()

def get_title_id( title_url ):
    imdb_id = re.search('/ev\d{7}\/\d{4}(-\d)?|(ch|co|ev|nm|tt)\d{7}/', title_url )
    if imdb_id:
        imdb_id = imdb_id.group(0).strip('/')
        return imdb_id
    else:
    	imdb_id = title_url.replace('/title/', '').strip('/')
    	return imdb_id
    return '-'

def extract_content( page ):
	movie = {}

	itemHeader = page.find('h3', class_='lister-item-header')

	link = itemHeader.find('a', href=True)
	_id = get_title_id( link['href'] )
	if _id == '-':
		return

	movie['link'] = rootURL + link['href']
	movie['id'] = _id
	movie['name'] = link.text.strip()
	movie['year'] = itemHeader.find('span', class_='lister-item-year').text.strip().replace('(', '').replace(')', '')

	try:
		rating = page.find('span', class_='certificate').text.strip()
	except:
		rating = defaultRating
	movie['rating'] = rating

	try:
		genre = page.find('span', class_='genre').text.strip()
	except:
		genre = 'NA'
	movie['genre'] = genre

	try:
		runtimeText = page.find('span', class_='runtime').text.strip() 
		runtime = int(runtimeText.replace('min', ''))
	except:
		runtime = 0
	movie['runtime'] = runtime

	try:
		rate_val = page.find('div', class_='ratings-bar')
		imdb_rate = float(rate_val.find('strong').text.strip())
	except:
		imdb_rate = 0
	movie['imdb_rate'] = imdb_rate

	try:
		ptags = page.findAll('p', class_='text-muted')
		description = ptags[1].get_text().strip()
	except:
		description = ''
	movie['description'] = description

	votesNgross = page.find('p', class_='sort-num_votes-visible')
	if votesNgross is not None:
		spans = votesNgross.findAll('span', class_='text-muted')
		value = votesNgross.findAll('span', {'name': 'nv'})
		if len(spans) > 1:
			try:
				movie[ spans[0].get_text().replace(':', '') ] = float(value[0]['data-value'].replace(',', ''))
			except:
				print('-')
			
			try:
				movie[ spans[1].get_text().replace(':', '') ] = float(value[1]['data-value'].replace(',', ''))
			except:
				print('-')
		else:
			try:
				movie[ spans[0].get_text().replace(':', '') ] = float(value[0]['date-value'].replace(',', ''))
			except:
				print('-')

	movieMeta = IMDB_MOVIE(_id)
	dataObj = movieMeta.parse()
	movie['meta'] = dataObj['meta']
	time.sleep(0.0001)
	return movie

def extract_movies( URL, year ):
	print(URL)
	r = requests.get(URL)
	content = r.text

	movieList = []
	movieIdList=[]
	page = BS(content, 'html.parser')

	main = page.find(id='main')
	if main is not None:
		lister_items = main.findAll('div', class_='lister-item')
		print(len(lister_items))
		for item in lister_items:
			lister_item_content = item.find('div', class_='lister-item-content')
			movie = extract_content( lister_item_content )
			movieList.append( movie )

	return movieList

def extract_movie_ids( URL, year ):
	print(URL)
	r = requests.get(URL)
	content = r.text

	movieIdList = []
	page = BS( content, 'html.parser' )

	main = page.find(id='main')
	if main is not None:
		lister_items = main.findAll('div', class_='lister-item')
		print( len(lister_items) )
		for item in lister_items:
			lister_item_content = item.find('div', class_='lister-item-content')
			itemHeader = lister_item_content.find('h3', class_='lister-item-header')
			link = itemHeader.find('a', href=True)
			_id = get_title_id( link['href'] )
			print(year, _id)
			if _id != '-':
				movieSynopsis = IMDB_EXRACT_SYNOPSIS( _id )
				content = movieSynopsis.extract()
				save_synopsis( _id, content )
				time.sleep(0.001)
	return movieIdList

def get_movie_list_for_page( page ):
	"""GET MOVIE FOR YEAR"""
	print(defaultRating, page)
	initURL = reqURL.format( pagination=page )
	dataset = extract_movies( initURL, page )
	save_datafile( page, dataset )
	time.sleep(0.001)

def get_movie_synopsis(page):
	"""GET MOVIE FOR YEAR"""
	print(defaultRating, page)
	initURL = reqURL.format( pagination=page )
	dataset = extract_movie_ids( initURL, page )
	print( dataset )

if __name__ == '__main__':
	#get movie by pagination, based on us ratings
	for rate in urls:
		defaultRating = rate
		details = urls[rate]
		maxCount = details['count']
		reqURL   = details['url']
		for page in range(0, maxCount, 250 ):
			padding = page + 1

			# if defaultRating == 'PG-13' and padding < 3000:
			# 	continue

			#get_movie_list_for_page(padding)
			get_movie_synopsis( padding )
