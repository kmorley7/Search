
class DictionaryHandler:

    def __init__(self):
        self.line_length = 26
        self.threshold = 2
        self.stopwords = {}

    def build(self, size):
        self.size = int(size * 1.1)
        self.dictionary = {}


    def openFile(self, filepath):
        self.filepath = filepath

        #determine the number of entries in the dictionary file
        self.file = open(filepath, "r+")
        self.file.seek(0,2)
        self.size = int(self.file.tell() / self.line_length)

    def hash(self, token, i=0):
        return (hash(token) + i) % self.size

    def insert(self, value):
        #filter out words with low frequencies
        if value[1] < self.threshold:
            return

        ''' This block can be uncommented to obtain the stopwords, and calling getStopWords() after writing the dictionary
            if value[1] > 300:
                self.stopwords[value[1]] = value[0]
        '''

        #insert into the hash table
        write = False
        i = 0
        while not write and i < self.size:
            h = self.hash(value[0], i)
            if self.dictionary.get(h) is None:
                self.dictionary[h] = value
                write = True
            else:
                i = i+1

        if not write:
            print("Dictionary is full")

    def getPosting(self, token):
        read = False
        i = 0
        while (not read) and (i < self.size):
            h = self.hash(token, i) * self.line_length
            self.file.seek(h)
            line = self.file.readline()
            if line[0:12] == "{:12.12}".format(token):
                posting = line.split()
                return posting[0], int(posting[1]), int(posting[2])
            else:
                i = i+1

        if not read:
            print("Record not found")

    '''
    Method used to obtain the most frequent words in our dictionary
    '''
    def getStopwords(self):
        for w in sorted(self.stopwords, reverse=True):
            print("\"{}\", ".format(self.stopwords[w]))


    def writeFile(self, filepath):
        with open(filepath, "w+") as f:
            for i in range(self.size):
                if self.dictionary.get(i) is None:
                    f.write("{:25.25}\n".format(''))
                else:
                    f.write("{:12.12} {:3.3} {:8.8}\n".format(self.dictionary[i][0], str(self.dictionary[i][1]), str(self.dictionary[i][2])))

