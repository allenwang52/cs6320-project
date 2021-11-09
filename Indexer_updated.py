import pysolr
import NLPFeatures as fl
import glob
import os
import csv
from spacy import displacy
from nltk.tokenize import sent_tokenize, word_tokenize


solr = pysolr.Solr('http://localhost:8983/solr/entropy', always_commit=True)
path = 'D:/UT Dallas/Courses/Fall 2021/CS6320(NLP)/Project/QA System/articles/*.txt'
docs = []
sent_tokens = []

def readFiles(path):
    files = glob.glob(path)
    n=0
    for name in files:
        nameOfFile = (os.path.basename(name))
        print("Started indexing for ",nameOfFile)
        with open(name,encoding="utf8") as f:

                file = f.read()
                docs.append(file)
                sent_tokens = [] 
                sent_tokens.extend(sent_tokenize(file))
                doc_sentences = [dict() for x in range(len(sent_tokens))]
                
                word_tokens=[]
                lemmatize_word=[]
                rootOfSentence=[]
                synonymns_list=[]
                hypernyms_list=[]
                hyponyms_list=[]
                meronyms_list=[]
                holonyms_list=[]
                entities_list = []
                entity_labels_list = []
                stemmatize_word = []
                dependency_parsed_tree =[]
                POS_tags = []
                
                for i in range(0,len(sent_tokens)):
                    a,b,c,d,e,f,g,h,i1,j,k,l,m = fl.getNLPFeatures(sent_tokens[i])
                    word_tokens.append(a)
                    lemmatize_word.append(b)
                    rootOfSentence.append(c)
                    synonymns_list.append(d)
                    hypernyms_list.append(e)
                    hyponyms_list.append(f)
                    meronyms_list.append(g)
                    holonyms_list.append(h)
                    entities_list.append(i1)
                    entity_labels_list.append(j)
                    stemmatize_word.append(k)
                    dependency_parsed_tree.append(l)
                    POS_tags.append(m)
                indexSolr(nameOfFile,doc_sentences,sent_tokens,word_tokens,lemmatize_word,rootOfSentence,
                          synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list, entities_list, entity_labels_list, stemmatize_word, dependency_parsed_tree, POS_tags)


def indexSolr(name, doc_sentences,sentences, word_tokens,lemmatize_word,rootOfSentence,
              synonymns_list,hypernyms_list,hyponyms_list,meronyms_list,holonyms_list,entities_list, entity_labels_list, stemmatize_word, dependency_parsed_tree, POS_tags):
    

    for i in range(0,len(sentences)):

        doc_sentences[i]["name"] = name
        doc_sentences[i]["sentence"] = sentences[i] 
        doc_sentences[i]["word_tokens"] = word_tokens[i]
        doc_sentences[i]["POS_tags"] = POS_tags[i]
        doc_sentences[i]["lemmatize_word"] = lemmatize_word[i] 
        doc_sentences[i]["rootOfSentence"] = rootOfSentence[i]
        doc_sentences[i]["synonymns_list"] = synonymns_list[i] 
        doc_sentences[i]["hypernyms_list"] = hypernyms_list[i]
        doc_sentences[i]["hyponyms_list"] = hyponyms_list[i] 
        doc_sentences[i]["meronyms_list"] = meronyms_list[i]
        doc_sentences[i]["holonyms_list"] = holonyms_list[i]
        doc_sentences[i]["entities_list"] = entities_list[i]
        doc_sentences[i]["entity_labels_list"] = entity_labels_list[i]
        doc_sentences[i]["stemmatize_word"] = stemmatize_word[i]
        doc_sentences[i]["dependency_parsed_tree"] = dependency_parsed_tree[i]

    solr.add(doc_sentences, commit = True)
    print("Indexing done for the file ",name)      




readFiles(path)
