import nltk
import spacy
import string
from nlp_features import NLPFeatures
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
en_nlp = spacy.load('en_core_web_sm')
stopword_set = set(stopwords.words()) | set(string.punctuation)
article_features = []

def get_features(id, sentence):
    all_words = word_tokenize(sentence)
    words = [w for w in all_words if w not in stopword_set]

    lemmas = []
    stems = []
    for word in words:
        lemmas.extend(lemmatizer.lemmatize(word))
        stems.extend(stemmer.stem(word))

    tags = []
    dependency_parse_tree = []
    tags.extend(pos_tag(sentence.split()))
    doc = en_nlp(sentence)
    for word in doc:
        dependency_parse_tree.append([word.dep_, word.head.text, word.text])

    hypernyms = []
    hyponyms = []
    meronyms = []
    holonyms = []
    for word in words:
        for synset in wn.synsets(word):
            for s in synset.hypernyms():
                if s.lemma_names() not in hypernyms:
                    hypernyms.extend(s.lemma_names())
            for s in synset.hyponyms():
                if s.lemma_names() not in hyponyms:
                    hyponyms.extend(s.lemma_names())
            for s in synset.part_meronyms():
                if s.lemma_names() not in meronyms:
                    meronyms.extend(s.lemma_names())
            for s in synset.part_holonyms():
                if s.lemma_names() not in holonyms:
                    holonyms.extend(s.lemma_names())

    return NLPFeatures(id, words, sentence, lemmas, stems, tags, dependency_parse_tree, hypernyms, hyponyms, meronyms, holonyms)
