import nltk
import spacy
import string
import en_core_web_sm
from nlp_features import NLPFeatures
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import word_tokenize

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
en_nlp = spacy.load('en_core_web_sm')
stopword_set = set(stopwords.words()) | set(string.punctuation)
article_features = []

def get_features(type, id, sentence):
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

    #Finding root of sentence
    sentence_root= list(doc.sents)
    for s in sentence_root:
        rootOfSentence = s.root.text

    synonymns = []
    hypernyms = []
    hyponyms = []
    meronyms = []
    holonyms = []

    for word in words:
        for synset in wn.synsets(word):

            synonymns.extend(wn.synset(synset.name()).lemma_names())
            for s in synset.hypernyms():
                hypernyms.extend(s.lemma_names())
            for s in synset.hyponyms():
                hyponyms.extend(s.lemma_names())
            for s in synset.part_meronyms():
                meronyms.extend(s.lemma_names())
            for s in synset.part_holonyms():
                holonyms.extend(s.lemma_names())

    #Finding Named Entity
    entities = []
    entity_labels = []
    nlp = en_core_web_sm.load()
    doc = nlp(sentence)
    for name in doc.ents:
        entities.append(name.text)
        entity_labels.append(name.label_)

    return NLPFeatures(type, id, words, sentence, lemmas, stems, tags, dependency_parse_tree, hypernyms, hyponyms, meronyms, holonyms, synonymns, rootOfSentence, entities, entity_labels)
