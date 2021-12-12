# CS6320_Project
Team Name:\
Entropy

Team Members:\
Allen Wang\
Shanjida Khatun

How to access project demo:\
$ pip install nltk\
$ pip install pysolr\
$ pip install --user -U pip setuptools wheel\
$ pip install spacy\
$ python -m spacy download en_core_web_sm

Manually install Apache Solr: https://archive.apache.org/dist/lucene/solr/8.0.0/ \
cd to the installed directory\
$ bin\solr start\
$ bin\solr create -c final1 -p 8983

Run solr_indexer.py to populate Apache Solr with entries\
Run main.py to query
