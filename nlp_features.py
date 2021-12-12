class NLPFeatures:
    def __init__(self, id, words, sentence, lemmas, stems, tags, parse_tree, hypernyms, hyponyms, meronyms, holonyms, synonymns, rootOfSentence, entities, entity_labels):
        self.id = id
        self.words = words
        self.sentence = sentence
        self.lemmas = lemmas
        self.stems = stems
        self.tags = tags
        self.parse_tree = parse_tree
        self.hypernyms = hypernyms
        self.hyponyms = hyponyms
        self.meronyms = meronyms
        self.holonyms = holonyms
        self.synonymns = synonymns
        self.rootOfSentence = rootOfSentence
        self.entities = entities
        self.entity_labels = entity_labels