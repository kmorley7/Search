
class DictionaryBuilder:

    def __init__(self, size):
        self.size = int(size * 1.3)
        self.dictionary = {}
        self.line_length = 26


    def hash(self, token, i=0):
        return (hash(token) + i) % self.size

    def insert(self, value):
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

    def get(self, token, filepath):
        with open(filepath, "r+") as f:
            read = False
            i = 0
            while not read and i < self.size:
                h = self.hash(token, i) * self.line_length
                f.seek(h)
                line = f.readline()
                if line[0:12] == "{:12.12}".format(token):
                    return line.split()
                else:
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

