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
        print("\nQuestion: {0}".format(question))
        features = feature_extraction.get_features('', question)
        words = ",".join(features.words)
        lemmas = ",".join(features.lemmas)
        hypernyms = ",".join(features.hypernyms)
        hyponyms = ",".join(features.hyponyms)
        stems = ",".join(features.stems)

        query = "(words:"+words+")^20 OR (lemmas:"+lemmas+")^10 OR \
                (hypernyms:"+hypernyms+")^20 OR (hyponyms:"+hyponyms+")^20 OR (stems:"+stems+")^10"

        results = solr.search(q=query,start=0, rows=10)

        print("Saw {0} result(s).".format(len(results)))
        for result in results:
            print("Answer sentence: {0}".format(result["sentence"]))
            print("The article's id is '{0}'.\n".format(result["id"].split("_")[0]))
