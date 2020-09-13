import string
import sys
import os
from HTMLLexer import HTMLLexer
import time
import shutil

if __name__ == "__main__":

    m = HTMLLexer()
    m.build()

    m.test(" 123,123,212,232,332,132,212 Ph.d.")
    directory = os.path.join(os.getcwd(), "files")
    files = os.listdir(directory)

    #delete and then create the directory for our tokenized files
    if os.path.exists('output'):
        shutil.rmtree('output')
    if not os.path.exists('output'):
        os.makedirs('output')

    elapsed_time = []
    start = time.time()

    #Loop over all files and tokenize them
    for file in files:
        if file.endswith(".html"):
            inputFile = os.path.join(directory,file)
            outputFile = os.path.join(os.getcwd(), "output/" + str(file)[:-5] + "_tokenized.txt")

            m.tokenizeFile(inputFile, outputFile)
            end = time.time()

            elapsed_time.append(end - start)


        #write the elapsed time to make a graph out of
        with open("timings.txt", 'w') as f:
            for x in elapsed_time:
                f.write("%f, " % x)

