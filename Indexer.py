from HTMLLexer import HTMLLexer

class Indexer:

    def __init__(self):
        self.index = {}
        self.doc_num = 0
        self.lexer = HTMLLexer()
        self.lexer.build()


    def parse(self, doc):
        self.doc_num = self.doc_num + 1
        tokens = self.lexer.tokenizeFile(doc)

        for x in tokens.keys():
            if x in self.index.keys():
                self.index[x] = self.index[x] + "{},{};".format(self.doc_num, tokens[x])
            else:
                self.index[x] = "{},{};".format(self.doc_num, tokens[x])

    def finish(self):
        with open("inverted_index.txt", "w") as f:
            for w in self.index:
                f.write("%s %s\n" % (w, self.index[w]))
