class NLPFeatures:
    def __init__(self, id, words, sentences, lemmas, stems, tags, parse_tree, hypernyms, hyponyms, meronyms, holonyms):
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