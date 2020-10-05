import string
import sys
import os
from HTMLLexer import HTMLLexer
import time
import shutil
from Indexer import Indexer

if __name__ == "__main__":

    m = Indexer()

    directory = os.path.join(os.getcwd(), "files")
    files = os.listdir(directory)



    #delete and then create the directory for our tokenized files
    if os.path.exists('output'):
        shutil.rmtree('output')
    if not os.path.exists('output'):
        os.makedirs('output')

    #for elapsed time
    elapsed_time = []
    start = time.time()

    mappings = []

    #Loop over all files and tokenize them
    for file in files:
        if file.endswith(".html"):
            inputFile = os.path.join(directory,file)
            outputFile = os.path.join(os.getcwd(), "output/" + str(file)[:-5] + "_tokenized.txt")

            m.parse(inputFile)
            mappings.append((m.doc_num, inputFile))
            end = time.time()

            elapsed_time.append(end - start)

    m.finish()
    with open("mappings.txt", "w") as f:
        for w in mappings:
            f.write("%s %s\n" % (w[0], w[1]))


    print(elapsed_time[-1])

