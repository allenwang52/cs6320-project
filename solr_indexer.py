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
   print('Solr is running')

path = os.path.join(os.getcwd(), "articles")
os.chdir(path)

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
en_nlp = spacy.load('en_core_web_sm')
stopword_set = set(stopwords.words()) | set(string.punctuation)

article_features = []
for file in os.listdir():
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        with open(file_path, encoding="utf8") as f:
            id = file.split(".")[0]
            article = sent_tokenize(f.read())
            for sentence in article:
                features = feature_extraction.get_features(id, sentence)
                article_features.append(NLPFeatures(features.id, features.words, features.sentences, features.lemmas, features.stems, features.tags, features.parse_tree, features.hypernyms, features.hyponyms, features.meronyms, features.holonyms))
    break

article_info = [dict() for x in range(len(article_features))]
for i, article in enumerate(article_features):
    article_info[i]["id"] = article.id + "_" + str(i)
    article_info[i]["words"] = article.words
    article_info[i]["sentences"] = article.sentences
    article_info[i]["lemmas"] = article.lemmas
    article_info[i]["stems"] = article.stems
    article_info[i]["tags"] = article.tags
    article_info[i]["parse_tree"] = article.parse_tree
    article_info[i]["hypernyms"] = article.hypernyms
    article_info[i]["hyponyms"] = article.hyponyms
    article_info[i]["meronyms"] = article.meronyms
    article_info[i]["holonyms"] = article.holonyms

solr.add(article_info, commit=True)
