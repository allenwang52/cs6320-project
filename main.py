import os
import nltk
import pysolr
import spacy
import string
import json
import feature_extraction
from nlp_features import NLPFeatures
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

solr = pysolr.Solr('http://localhost:8983/solr/entropy', always_commit=True)
ping = solr.ping()
resp = json.loads(ping)

if resp.get('status') == 'OK':
       print('Solr is running\n')

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
en_nlp = spacy.load('en_core_web_sm')
stopword_set = set(stopwords.words()) | set(string.punctuation)

file_path = os.path.join(os.getcwd(), "questions.txt")
with open(file_path, encoding="utf8") as f:
    question_list = f.read().splitlines()

    for question in question_list:
        features = feature_extraction.get_features('', question)

'''
query = "entity_labels_list:("+",".join(req_entity_type)+" )^20 AND ((word_tokens:"+word_tokens+")^20 OR (lemmatize_word:"+ lemmatize_word+")^10 OR (synonymns_list:"+synonymns_list+")^10 OR \
        (hypernyms_list:"+hypernyms_list+") OR (hyponyms_list:"+hyponyms_list+") OR (stemmatize_word:"+stemmatize_word+")^10 AND (entities_list:"+entities_list+")^20)"

results = solr.search(q=query,start=0, rows=10)

print("Saw {0} result(s).".format(len(results)))
for result in results:
    print("The article id is '{0}'.".format(result['id']))
'''
