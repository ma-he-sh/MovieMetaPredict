import os
import json
import pandas as pd

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download()

## Preprocess and clean text data
## Remove stop words
stop_words = stopwords.words("english")
wordnet = WordNetLemmatizer()

def text_preprocess( text ):
	text = text.lower()
	text = ' '.join([word for word in text.split(' ') if word not in stop_words])
	text = text.encode('ascii', 'ignore').decode()
	text = re.sub(r'https*\S+', ' ', text)
	text = re.sub(r'@\S+', ' ', text)
	text = re.sub(r'#\S+', ' ', text)
	text = re.sub(r'\'\w+', '', text)
	text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
	text = re.sub(r'\w*\d+\w*', '', text)
	text = re.sub(r'\s{2,}', ' ', text)
	return text

def save_datafile( file_name, dictionary ):
    with open('./cleaned_data_2/' + file_name, 'w') as f:
        json.dump(dictionary, f, indent=4)

def get_dataset_list( dir_name ):
	file_list = []
	for file in os.listdir( dir_name ):
		if file.endswith('.json'):
			file_list.append( os.path.join( dir_name, file ) )
	return file_list

def get_synopsis( movie_id ):
	with open( './synopsis_2/' + movie_id + '.txt' ) as data_file:
		return data_file.read()

no_data_string = 'It looks like we don'

def get_file_data( file_dir, rating ):
	docs = []
	with open( file_dir ) as data_file:
		data = json.load( data_file )
		for doc in data:
			movie_id = doc['id']

			doc['rating'] = rating
			doc['meta']['rating'] = rating

			try:
				description = doc['description']
				description = text_preprocess(description)
			except:
				description = ''

			try:
				storyline   = doc['meta']['storyline']
				storyline = text_preprocess(storyline)
			except:
				storyline = ''

			try: 
				synopsis = get_synopsis( movie_id )
				if no_data_string in synopsis:
					synopsis = ''
				else:
					synopsis = text_preprocess( synopsis )
			except:
				synopsis = ''

			doc['synopsis'] = synopsis
			doc['clean_description'] = description.strip()
			doc['clean_storyline']   = storyline.strip()
			
			docs.append(doc)
	return docs

def clean_data():
	file_list = get_dataset_list( './dataset_emotions' )
	for file in file_list:
		filename = os.path.basename( file )
		groupname = filename.split('_')
		documents = get_file_data(file, groupname[1] )
		save_datafile( filename, documents )


if __name__ == '__main__':
	clean_data()