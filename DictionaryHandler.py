
class DictionaryHandler:
    '''
    Class that handles both writing a dictionary from memory to file
    and for opening and reading from an existing dictionary file
    '''

    def __init__(self):
        self.line_length = 26
        self.threshold = 2
        self.stopwords = {}

    #Call this function when we want to use this class for writing a dictionary
    def build(self, size):
        self.size = int(size * 0.6 )
        self.dictionary = {}

    #Call this function when we want to read from an already existing dictionary file
    def openFile(self, filepath):
        self.filepath = filepath

        #determine the number of entries in the dictionary file to correctly set self.size for hashing modulo size
        self.file = open(filepath, "r+")
        self.file.seek(0, 2)
        self.size = int(self.file.tell() / self.line_length)

    def hash(self, token, i=0):
        return (hash(token) + i) % self.size

    def insert(self, value):
        #filter out words with low frequencies
        if value[1] < self.threshold:
            return

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


    def getEntry(self, token):
        '''
        Searches the Dictionary file for the Dictionary Entry corresponding to a Token
        :param token: a token to search the dictionary for
        :return: (token, num_docs, posting_offset) or None if token is not in the Dictionary
        '''
        read = False
        i = 0
        while (not read) and (i < self.size):
            offset = self.hash(token, i) * self.line_length
            self.file.seek(offset)
            line = self.file.readline()

            if "{:12.12}".format(line) == "{:12.12}".format(token):  # format the token the same way we did when writing to the dictionary
                posting = line.split()
                return posting[0], int(posting[1]), int(posting[2])

            else:  # linear probe through the dictionary
                i = i+1

        if not read:
            print("Record not found")


    def writeFile(self, filepath):
        with open(filepath, "w+") as f:
            for i in range(self.size):
                if self.dictionary.get(i) is None:
                    f.write("{:25.25}\n".format(''))
                else:
                    f.write("{:12.12} {:3.3} {:8.8}\n".format(self.dictionary[i][0], str(self.dictionary[i][1]), str(self.dictionary[i][2])))

