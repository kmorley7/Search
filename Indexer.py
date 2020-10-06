from HTMLLexer import HTMLLexer

class Indexer:

    #This class will contain our inverted index in memory
    class InvertedIndex(dict):
        def addToIndex(self, key, item):
            if key in self.keys():
                self[key] = self[key] + [item]
            else:
                self[key] = [item]

    def __init__(self):
        self.index = self.InvertedIndex()
        self.doc_num = 0
        self.lexer = HTMLLexer()
        self.lexer.build()

    def parse(self, doc):
        self.doc_num = self.doc_num + 1
        tokens = self.lexer.tokenizeFile(doc)

        for x in tokens.keys():
            self.index.addToIndex(x, (self.doc_num, tokens[x]))


    def finish(self):

        #here is where i should make the dict file: term, num docs, start
        dict_file = {}
        with open("postings.txt", "w") as f:
            for w in self.index:
                #count the number of entries and get the line number of the inverted index file we are writing to
                num_docs = len(self.index[w])
                offset = f.tell()
                dict_file[w] = (num_docs, offset)
                for x in self.index[w]:
                    f.write("{} {}\n".format(x[0], x[1]))

        with open("dictionary.txt", "w") as f:
            for w in sorted(dict_file):
                f.write("{}, {}, {}\n".format(w, dict_file[w][0], dict_file[w][1]))