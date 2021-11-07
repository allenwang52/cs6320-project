import os
import nltk
import pysolr
import spacy
import json
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
#from elasticsearch import Elasticsearch
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class ArticleInformation:
    def __init__(self, id, words, sentences, lemmas, stems, tags, parse_tree, hypernyms, hyponyms, meronyms, holonyms):
        # Need parse tree, wordnet features
        self.id = id
        self.words = words
        self.sentences = sentences
        self.lemmas = lemmas
        self.stems = stems
        self.tags = tags
        self.parse_tree = parse_tree
        self.hypernyms = hypernyms
        self.hyponyms = hyponyms
        self.meronyms = meronyms
        self.holonyms = holonyms

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

article_features = []
for file in os.listdir():
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        with open(file_path, encoding="utf8") as f:
            id = file.split(".")[0]
            article = f.read()

            # TODO Remove stopwords
            words = word_tokenize(article)
            sentences = sent_tokenize(article)

            lemmas = []
            stems = []
            for word in words:
                lemmas.extend(lemmatizer.lemmatize(word))
                stems.extend(stemmer.stem(word))

            tags = []
            dependency_parse_tree = []
            for sentence in sentences:
                tags.extend(pos_tag(sentence.split()))
                doc = en_nlp(sentence)
                dependency_parse_tree.append(doc)

            hypernyms = []
            hypernyms_list = []
            hyponyms = []
            meronyms = []
            holonyms = []
            for word in words:
                for synset in wn.synsets(word):
                    hypernyms.extend([s.lemma_names() for s in synset.hypernyms()])
                    hyponyms.extend([s.lemma_names() for s in synset.hyponyms()])
                    meronyms.extend([s.lemma_names() for s in synset.part_meronyms()])
                    holonyms.extend([s.lemma_names() for s in synset.part_holonyms()])

    article_features.append(ArticleInformation(id, words, sentences, lemmas, stems, tags, dependency_parse_tree, hypernyms, hyponyms, meronyms, holonyms))

for article in article_features:
    article_info = [dict()]

    article_info[0]["id"] = article.id

    solr.add(article_info, commit=True)

results = solr.search(q="{!term f=id}181", start=0, rows=10)

print("Saw {0} result(s).".format(len(results)))
for result in results:
    print("The id is '{0}'.".format(result['id']))
