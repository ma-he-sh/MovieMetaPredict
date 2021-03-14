#!/usr/bin/bash python3
# -*- coding: utf-8 -*-
"""
IMDB API Connector
"""
"""
Code source  :: https://github.com/ma-he-sh/ENGR_5775G_Assignment/blob/main/ENGR_5775G_assignment1/imdb/imdb_api.py
"""

from bs4 import BeautifulSoup as BS
import requests
import time
import re

class REST():
    site_url = 'https://imdb.com'

    def do_request(self, url):
        r = requests.get( url )
        if r.status_code == 200:
            return r.content
        raise Exception('Failed to get content')

    def get_list_url(self, list_id):
        return self.site_url + '/list/' + list_id

    def get_title_url(self, title_id):
        return self.site_url + '/title/' + title_id

    def get_known_url(self, link):
        return self.site_url + link

    def get_page_html(self, page):
        return BS(page, 'html.parser')

class IMDB_MOVIE():
    pagecontent = 'pagecontent'
    detect_txt_seemore = 'See more'

    def __init__(self, _id):
        self.movie = {}
        self.title_id = _id

        rest = REST()
        self.reqURL = rest.get_title_url( self.title_id )
        print( self.reqURL )

        self.movie['id'] = _id
        self.movie['url'] = self.reqURL
        self.movie['meta'] = {}

    def cast_data(self, page):
        if not page.find( id='titleCast' ):
            return Exception('Cast not found')
        # ====================================================================
        # cast data
        # ====================================================================
        title_cast_wrapper = page.find(id='titleCast')
        if title_cast_wrapper is not None:
            cast_list_table = title_cast_wrapper.find('table', class_='cast_list')
            cast_list = []
            if cast_list_table is not None:
                cast_items = cast_list_table.findAll('tr')
                for tr in cast_items:
                    tditem = tr.findAll('td')
                    name = {}

                    # cast consist of 4 td :: image, name, ellipsis, character
                    if len(tditem) == 4:
                        actor = tditem[1].find('a', href=True)
                        name['actor'] = actor.text.strip()
                        name['actor_link'] = actor['href']

                        character_name = tditem[3].find('a', href=True)
                        if character_name is not None:
                            name['character'] = character_name.text.strip()
                            name['character_link'] = character_name['href']
                            cast_list.append( name )

                self.movie['meta']['cast'] = cast_list

    def story_line_data( self, page ):
        if not page.find( id='titleStoryLine' ):
            return Exception('Storyline not found')
        # =====================================================================
        # storyline
        # =====================================================================
        storyline_wrapper = page.find(id='titleStoryLine')
        if storyline_wrapper is not None:
            storyline_content = storyline_wrapper.find('div', class_='inline')
            if storyline_content is not None:
                self.movie['meta']['storyline'] = storyline_content.text.strip().replace('\n', '').replace('\r', '')

            text_blocks = storyline_wrapper.findAll('div', class_='txt-block')
            if text_blocks is not None and len( text_blocks ) > 0:
                # these blocks contain Certificate
                for block in text_blocks:
                    b_headling = block.find('h4', class_='inline')
                    b_content  = block.find('span')

                    if b_headling is not None:
                        if 'Certificate' in b_headling.text.strip():
                            self.movie['meta']['rating'] = b_content.text.strip()

    def get_a_tags_arr(self, b_heading, block):
        if block is None:
            return None

        tags = None
        atags = block.findAll('a')
        if atags is not None and len(atags) > 0:
            firstTagCheck = atags[0].text.strip()
            if firstTagCheck != self.detect_txt_seemore:
                tags = []
                for atag in atags:
                    if atag.text.strip() != self.detect_txt_seemore:
                        tags.append( atag.text.strip() )
                return tags

        content = block.text.strip()
        tags = content.replace(str(b_heading), '').replace(self.detect_txt_seemore, '').replace('\n', '').replace('\u00a0', '').replace('\u00bb', '').strip()
        return tags

    def title_detail_data(self, page):
        # =====================================================================
        # title details
        # =====================================================================
        title_details = page.find(id='titleDetails')
        if title_details is not None:
            # this block contain country, language, release date, filming location, other meta, box office, company credits, technical specs
            text_blocks = title_details.findAll('div', class_='txt-block')
            if text_blocks is not None and len( text_blocks ) > 0:
                retrieve_blocks = [ 'Country:', 'Language:', 'Release Date:', 'Also Known As:', 'Filming Locations:', 'Budget:', 'Opening Weekend USA:', 'Gross USA:', 'Cumulative Worldwide Gross:', 'Production Co:', 'Runtime:', 'Sound Mix:', 'Color:', 'Aspect Ratio:' ]
                for block in text_blocks:
                    b_heading = block.find('h4', class_='inline')
                    if b_heading is not None and b_heading.text.strip() in retrieve_blocks:
                        heading_text = b_heading.text.strip()
                        self.movie['meta'][heading_text] = self.get_a_tags_arr( heading_text, block )

    def parse(self, page=None):
        if page is None:
            rest = REST()
            pageContent = rest.do_request( self.reqURL )
            page = rest.get_page_html( pageContent )
        if not page.find(id=self.pagecontent):
            return Exception('Title not found')

        result = page.find(id=self.pagecontent)
        main_top_section = result.find('div', id='main_top')
        main_bottom_section = result.find('div', id='main_bottom')

        title_bar_wrapper = main_top_section.find('div', class_='title_bar_wrapper')
        plot_summary_section = main_top_section.find('div', class_='plot_summary_wrapper')
        plot_summary = plot_summary_section.find('div', class_='plot_summary')

        title_wrapper = title_bar_wrapper.find('div', class_='title_wrapper')
        movie_title = title_wrapper.find('h1').text.strip().replace(u'\xa0', u':').split(':')

        self.movie['title'] = movie_title[0]
        self.movie['year']  = movie_title[1]
        self.movie['description'] = plot_summary.find('div', 'summary_text').text.strip()

        self.cast_data(main_bottom_section)

        self.title_detail_data( main_bottom_section )

        self.story_line_data( main_bottom_section )

        return self.movie

class IMDB_MOVIE_LIST():
    pagecontent = 'main'
    list = {}

    def __init__(self, _list_id, include_addition_meta=False):
        self.list_id = _list_id
        self.rest = REST()
        self.reqURL = self.rest.get_list_url( self.list_id )
        self.include_addition_meta = include_addition_meta

    def get_title_id( self, title_url ):
        imdb_id = re.search('/ev\d{7}\/\d{4}(-\d)?|(ch|co|ev|nm|tt)\d{7}/', title_url )
        if imdb_id:
            imdb_id = imdb_id.group(0).strip('/')
            return imdb_id
        return '-'

    def parse(self, page=None):
        if page is None:
            pageContent = self.rest.do_request( self.reqURL )
            page = self.rest.get_page_html( pageContent )
        if not page.find(id=self.pagecontent):
            return Exception('List not found')

        lister_items = page.findAll('div', class_='lister-item')
        data = []
        title_ids = []
        for item in lister_items:
            movie = {}

            lister_item_content = item.find('div', class_='lister-item-content')

            # get title and title link
            item_header = lister_item_content.find('h3', class_='lister-item-header')
            item_title  = item_header.find('a', href=True)
            item_year   = item_header.find('span', class_='lister-item-year')

            if item_title is not None:
                imdb_id = self.get_title_id(item_title.get('href'))
                movie['id']  = imdb_id
                movie['href']  = self.rest.get_title_url(imdb_id)
                title_ids.append(imdb_id)

            if item_header is not None:
                movie['title'] = item_title.text.strip()

            if item_year is not None:
                movie['year'] =  item_year.text.strip().replace('(','').replace(')', '')

            movie['meta'] = {}

            # get certificate :: rating
            certificate = lister_item_content.find('span', class_='certificate')
            if certificate is not None:
                movie['meta']['certificate'] = certificate.text.strip()

            # get movie runtime
            runtime     = lister_item_content.find('span', class_='runtime')
            if runtime is not None:
                movie['meta']['runtime'] = runtime.text.strip()

            # get genre
            genre       = lister_item_content.find('span', class_='genre')
            if genre is not None:
                movie['meta']['genre'] = genre.text.strip().split(',')

            # get meta score
            meta_score  = lister_item_content.find('span', class_='metascore')
            if meta_score is not None:
                movie['meta']['meta_score'] = meta_score.text.strip()

            # get movie description
            pcontent = lister_item_content.findAll('p')
            if pcontent is not None:
                if len(pcontent) > 0:
                    # description :: index at 1
                    description = pcontent[1].text.strip()
                    movie['meta']['description'] = description

                    # directors :: index at 2
                    directors = pcontent[2].find('a', href=True)
                    movie['meta']['directors'] = []
                    for director in directors:
                        movie['meta']['directors'].append(director)

                    # votes, gross
                    submeta = pcontent[3].findAll('span')
                    if len(submeta) > 0:
                        collectMeta = ''
                        collectIndex= -1

                        for idx, spans in enumerate(submeta):
                            if collectIndex == idx:
                                movie['meta'][collectMeta] = spans.text.strip()
                            if spans.has_attr('class'):
                                if spans.text.strip() == 'Votes:':
                                    collectMeta = 'votes'
                                    collectIndex= idx + 1
                                if spans.text.strip() == 'Gross:':
                                    collectMeta = 'gross'
                                    collectIndex= idx + 1

            # collect description metas
            list_description    = item.find('div', class_='list-description')
            if list_description is not None:
                movie['meta']['awards'] = {}
                content = list_description.find('p')
                if content is not None:
                    replaceStr = str(content)
                    # keep the original copy
                    parts = replaceStr.replace('*****', '').replace('<p>', '').replace('</p>', '').split('<br/><br/>')
                    if len(parts) > 0:
                        for part in parts:
                            subParts = part.split('\n')
                            if len(subParts) > 0:
                                for sub in subParts:
                                    if sub != '':
                                        textVal = sub.split(':')
                                        movie['meta']['awards'][str(textVal[0])] = str(textVal[1]).strip()

            if self.include_addition_meta:
                movieTitle = IMDB_MOVIE(imdb_id)
                titleData = movieTitle.parse()
                if titleData['meta'] is not None:
                    for key in titleData['meta']:
                        movie['meta'][key] = titleData['meta'][key]

            data.append( movie )

        return data, title_ids
