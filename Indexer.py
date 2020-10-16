from HTMLLexer import HTMLLexer
from DictionaryBuilder import DictionaryBuilder
from Stopwords import Stopwords
import os

class Indexer:

    #This class will contain our inverted index in memory
    class InvertedIndex(dict):

        def addToIndex(self, key, item):
            if key in Stopwords:
                return

            if key in self.keys():
                self[key] = self[key] + [item]
            else:
                self[key] = [item]

    def __init__(self):
        self.index = self.InvertedIndex()
        self.doc_num = 0
        self.mappings = []
        self.lexer = HTMLLexer()
        self.lexer.build()

    def parse(self, doc):
        self.doc_num = self.doc_num + 1
        tokens, count = self.lexer.tokenizeFile(doc)

        for x in tokens.keys():
            norm_tf = tokens[x]/count
            self.index.addToIndex(x, (self.doc_num, norm_tf))

    def writeFiles(self, outputDir, N):

        dictionaryBuilder = DictionaryBuilder(len(self.index))

        with open(os.path.join(outputDir, "postings.txt"), "w") as f:
            for w in self.index:
                #count the number of entries and get the offset of the inverted index file we are writing to
                num_docs = len(self.index[w])
                idf = N / num_docs

                offset = f.tell()
                dictionaryBuilder.insert((w, num_docs, offset))
                for x in self.index[w]:
                    f.write("{:3d} {:8.8}\n".format(x[0], str(x[1] * idf)))

                    if w=="algorithm" and x[0]==624:
                        print("{:3d} {:8.8}\n".format(x[0], str(x[1] * idf)))

        dictionaryBuilder.writeFile(filepath=os.path.join(outputDir, "dictionary.txt"))

        #write out the mappings file
        with open( os.path.join(outputDir, "mappings.txt"), "w") as f:
            for w in self.mappings:
                f.write("{:3.3} {:64.64}\n".format(str(w[0]), str(w[1])))
