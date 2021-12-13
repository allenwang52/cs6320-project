# CS6320_Project
Team Name:\
Entropy

Team Members:\
Shanjida Khatun (sxk200130@utdallas.edu)\
Allen Wang (axw161630@utdallas.edu)

How to access project demo:\
$ pip install nltk\
$ pip install pysolr\
$ pip install --user -U pip setuptools wheel\
$ pip install spacy\
$ python -m spacy download en_core_web_sm

Manually install Apache Solr: https://archive.apache.org/dist/lucene/solr/8.0.0/ \
cd to the installed directory\
$ bin\solr start\
$ bin\solr create -c entropy -p 8983

To populate Apache Solr with entries:\
$ py solr_indexer.py\
To start querying on questions:\
$ py main.py <question_file_path>

Once done:\
$ bin\solr stop -all\
$ bin\solr delete -c entropy
