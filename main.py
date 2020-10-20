import sys
import os
import time
import csv
import shutil
from Indexer import Indexer

def main(inputDir, outputDir):

    m = Indexer()
    files = os.listdir(inputDir)

    #for measuring elapsed time
    elapsed_time = []
    start = time.time()


    #Loop over all files in the given directory
    for file in files:
        if file.endswith(".html"):
            inputFile = os.path.join(inputDir,file)

            m.parse(inputFile) #the tokenization happens inside this function
            m.mappings.append((m.doc_num, inputFile))

            end = time.time()
            elapsed_time.append(end - start)


    m.writeFiles(outputDir, N=len(m.mappings))
    print("Ran in {} seconds.".format(elapsed_time[-1]))


if __name__ == "__main__":

    inputDir = sys.argv[1]
    outputDir = sys.argv[2]

    if not os.path.isdir(inputDir):
        raise NotADirectoryError(inputDir + " is not a valid directory for the input files")

    #delete and then create the directory for our tokenized files
    if os.path.exists(outputDir):
        shutil.rmtree(outputDir)
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    main(inputDir, outputDir)







