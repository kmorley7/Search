import string
import sys
import os
from HTMLLexer import HTMLLexer
import shutil
#a directory of all tokenized documents (one output file per input file)
#a file of all tokens and their frequencies sorted by token
#a file of all tokens and their frequencies sorted by frequency


if __name__ == "__main__":

    m = HTMLLexer()
    m.build()

    m.test(" <html>\n <head><title>Another test file</title></head>\n <body> ")
    directory = os.path.join(os.getcwd(), "testfiles")
    files = os.listdir(directory)


    if os.path.exists('output'):
        shutil.rmtree('output')

    if not os.path.exists('output'):
        os.makedirs('output')


    for file in files:
        if file.endswith(".html"): #might have to change to "b.html" on linux systems
            inputFile = os.path.join(directory,file)
            outputFile = os.path.join(os.getcwd(), "output/" + str(file)[:-5] + "_tokenized.txt")

            m.tokenizeFile(inputFile, outputFile)


    m.finish()
    #todo build a file that has counts of all the tokens, then build a file that has all the tokens sorted

"""
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".html"):
            with open(os.path.join(directory, filename), 'r') as f:
                print("made it")

"""




    #run a tokenizer task
    #send to a reducer to count the occurrences of each token
    #sort by both token and frequency