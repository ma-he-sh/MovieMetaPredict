from bs4 import BeautifulSoup as BS
import requests
import time
import re

class REST():
    site_url = 'https://imdb.com'

    def do_request(self, url):
        try:
            r = requests.get( url )
            if r.status_code == 200:
                return r.content
        except Exception as ex:
            print('Connection Failed')

    def get_list_url(self, list_id):
        return self.site_url + '/list/' + list_id

    def get_title_url(self, title_id):
        return self.site_url + '/title/' + title_id

    def get_known_url(self, link):
        return self.site_url + link

    def get_page_html(self, page):
        return BS(page, 'html.parser')

class IMDB_EXRACT_SYNOPSIS():
    mainContent = 'main'

    def __init__(self, _id):
        self.content = ''
        self.title_id = _id

        rest = REST()
        self.reqURL = rest.get_title_url( _id ) + '/plotsummary'
    
    def extract(self, page=None):
        if page is None:
            rest = REST()
            pageContent = rest.do_request( self.reqURL )
            page = rest.get_page_html( pageContent )
        if not page.find( id=self.mainContent ):
            return Exception('Summary Not Found')

        result = page.find(id=self.mainContent)
        content = result.find(id='plot-synopsis-content')
        if content is not None:
            synopsis = content.get_text()
            return synopsis
        else:
            return ''

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
                        #name['actor_link'] = actor['href']

                        character_name = tditem[3].find('a', href=True)
                        if character_name is not None:
                            name['character'] = character_name.text.strip()
                            #name['character_link'] = character_name['href']
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
                self.movie['meta']['storyline'] = storyline_content.get_text().replace('\n', '').replace('\r', '').strip()

            text_blocks = storyline_wrapper.findAll('div', class_='txt-block')
            if text_blocks is not None and len( text_blocks ) > 0:
                # these blocks contain Certificate
                for block in text_blocks:
                    b_headling = block.find('h4', class_='inline')
                    b_content  = block.find('span')
                    if b_headling is not None:
                        if 'Certificate' in b_headling.text.strip():
                            self.movie['meta']['rating'] = b_content.text.strip().split()[0]

    def money_format(self, str):
        try:
            formatted = float(str.replace('$', '').replace(',', ''))
        except:
            formatted = str
        finally:
            return formatted


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
        if b_heading == 'Cumulative Worldwide Gross:':
            tags = self.money_format( tags )
        if b_heading == 'Budget:':
            tags = self.money_format( tags.split()[0] )
        if b_heading == 'Gross USA:':
            tags = self.money_format( tags.split()[0] )
        if b_heading == 'Opening Weekend USA:':
            tags = self.money_format( tags.split()[0] )
        if b_heading == 'Runtime:':
            tags = float(tags.split()[0])
        if b_heading == 'Aspect Ratio:':
            tags = tags.strip()

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

        #self.movie['title'] = movie_title[0]
        #self.movie['year']  = int(movie_title[1].replace('(','').replace(')', ''))
        #self.movie['description'] = plot_summary.find('div', 'summary_text').text.strip()

        self.cast_data(main_bottom_section)

        self.title_detail_data( main_bottom_section )

        self.story_line_data( main_bottom_section )

        return self.movie