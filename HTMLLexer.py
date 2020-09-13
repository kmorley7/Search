#Rules for our tokenizer

#strip out all content inside html tags<>

from lex import lex
import re

class HTMLLexer(object):

    states = (
        ('tag', 'inclusive'),
        ('meta', 'inclusive'),
        ('content', 'inclusive'),
    )

    tokens = (
        'tag_END',
        'tag_META',
        'tag_NONTEXT',
        'meta_CONTENT',
        'content_END',
        'TEXT_TAG',
        'META',
        'FLOAT',
        'TIME',
        'HYPHENATED',
        'ABBREVIATED',
        'WORD',
        'WHITESPACE',
        'PUNCTUATION',
    )

    def t_tag(self, t):
        r'<'
        t.lexer.tag_start = t.lexer.lexpos
        t.lexer.begin('tag')

    def t_tag_END(self, t):
        r'>'
        t.lexer.begin('INITIAL')

    def t_tag_META(self, t):
        r"meta"
        t.value = "This is a meta tag"
        t.lexer.begin("meta")
        return t

    def t_tag_NONTEXT(self, t):
        r'kdkdkdkd'
        return t

    def t_meta_CONTENT(self, t):
        r"content\s*=\s*\""
        t.lexer.content_start = t.lexer.lexpos
        t.lexer.begin("content")
        return t

    def t_content_END(self, t):
        r"\""
        t.value = t.lexer.lexdata[t.lexer.content_start:t.lexer.lexpos+1]
        t.lexer.begin("meta")
        return t

    def t_TEXT_TAG(self, t):
        r'(\w*<[^>]*>\w*)+'
        t.value = re.sub("<[^>]*>", "", t.value)
        return t



    def t_HYPHENATED(self, t):
        r"(\w+-\w+)+"
        t.value = re.sub("-*", "", t.value)
        return t

    def t_FLOAT(self, t):
        r"[-+]?\d*\.\d+"
        t.value = str(abs(int(float(t.value))))
        return t

    def t_TIME(self, t):
        r"\w+:\w+"
        t.value = re.sub(":*", "", t.value)
        return t


    #words are consisting of only characters
    #we convert the word to all lowercase
    def t_WORD(self, t):
        r'\w+'
        t.value = str(t.value).lower()
        return t


    def t_WHITESPACE(self, t):
        r'\s+'
        pass

    def t_ABBREVIATED(self, t):
        r"(\w+.\w+)+"
        t.value = re.sub(".", "", t.value)
        return t

    def t_PUNCTUATION(self, t):
        r'[!"#$%&\'\(\)\*\+,-./:;<=>?@\[\]^_`{|}~\\]'
        pass

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex(module=self, **kwargs)
        self.frequency = {}

    def updateFrequency(self, freq):
        for key in freq:
            if key in self.frequency:
                self.frequency[key] = self.frequency[key] + freq[key]
            else:
                self.frequency[key] = freq[key]

    def tokenizeFile(self, inputFile, outputFile):

        tokens = []

        with open(inputFile,'r') as f:
            data = f.read()
            self.lexer.input(data)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                tokens.append(tok.value)

        with open(outputFile, 'w') as f:
            for x in tokens:
                f.write("%s\n" % x)


        #Count the frequency of tokens for this file
        freq = {}
        for x in tokens:
            if (x in freq):
                freq[x] += 1
            else:
                freq[x] = 1

        self.updateFrequency(freq)

    def finish(self):

        with open("sorted.txt", "w") as f:
            for w in sorted(self.frequency):
                f.write("%s\n" % w)

        with open("frequency.txt", "w") as f:
            for w in sorted(self.frequency, key=self.frequency.get, reverse=True):
                f.write("%s %d\n" % (w, self.frequency[w]))

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
