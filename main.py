import os
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
import pysolr
import spacy
import string
import json
import csv
import sys
import feature_extraction
from nlp_features import NLPFeatures
from nltk.tag import pos_tag
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

def processQueries(question_path):
    file_path = os.path.join(os.getcwd(), question_path)
    with open(file_path, encoding="utf8") as f:
        question_list = f.read().splitlines()

        for question in question_list:
            #print("\nQuestion: {0}".format(question))

            entity_type = []
            question_LC = question.lower()

            if "who" in question_LC:
                entity_type.extend(["\"PERSON\"","\"ORG\""])
                clue1="PERSON"
                clue2="ORG"

            elif "when" in question_LC:
                entity_type.extend(["\"DATE\"","\"TIME\""])
                clue1="DATE"
                clue2="TIME"

            question_words = word_tokenize(question)
            questionwords_withoutStopwords = [w for w in question_words if not w in stopword_set]
            modified_question = " ".join(questionwords_withoutStopwords)

            features = feature_extraction.get_features('', modified_question)
            words = ",".join(features.words) if len(features.words) != 0 else "*"
            lemmas = ",".join(features.lemmas) if len(features.lemmas) != 0 else "*"
            hypernyms = ",".join(features.hypernyms) if len(features.hypernyms) != 0 else "*"
            hyponyms = ",".join(features.hyponyms) if len(features.hyponyms) != 0 else "*"
            meronyms = ",".join(features.meronyms) if len(features.meronyms) != 0 else "*"
            holonyms = ",".join(features.holonyms) if len(features.holonyms) != 0 else "*"
            stems = ",".join(features.stems) if len(features.stems) != 0 else "*"
            synonymns = ",".join(features.synonymns) if len(features.synonymns) != 0 else "*"
            rootOfSentence = ",".join(features.rootOfSentence) if len(features.rootOfSentence) != 0 else "*"
            entities = ",".join(features.entities) if len(features.entities) != 0 else "*"
            entity_labels = ",".join(features.entity_labels) if len(features.entity_labels) != 0 else "*"

            if "what" in question_LC:
                query = "((words:"+words+")^20 OR (lemmas:"+ lemmas+")^10 OR (synonymns:"+synonymns+")^10 OR \
                    (hypernyms:"+hypernyms+") OR (hyponyms:"+hyponyms+") OR (meronyms:"+meronyms+") OR (rootOfSentence:"+rootOfSentence+") OR \
                    (hyponyms:"+hyponyms+") OR (stems:"+stems+")^10 AND (entities:"+entities+")^20)"
            else:
                query = "entity_labels:("+",".join(entity_type)+" )^20 AND "

                query += "((words:"+words+")^20 OR (lemmas:"+ lemmas+")^10 OR (synonymns:"+synonymns+")^10 OR \
                    (hypernyms:"+hypernyms+") OR (hyponyms:"+hyponyms+") OR (meronyms:"+meronyms+") OR (rootOfSentence:"+rootOfSentence+") OR \
                    (hyponyms:"+hyponyms+") OR (stems:"+stems+")^10 AND (entities:"+entities+")^20)"

            results = solr.search(q=query,start=0, rows=10)

            #print("Saw {0} result(s).".format(len(results)))
            #for result in results:
            #    print("Answer sentence: {0}".format(result["sentence"]))
            #    print("The article's id is '{0}'.\n".format(result["id"].split("_")[0]))

            with open("result.csv", "a", newline='', encoding='utf8') as csvFile:
                if len(results) != 0:
                    wr = csv.writer(csvFile)
                    wr.writerow([question, list(results)[0]["sentence"][0], str(list(results)[0]["id"].split("_")[0])])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("""
        Usage: main.py <question_file_path>
        """, file=sys.stderr)
        sys.exit(-1)

    path = sys.argv[1]

    processQueries(path)