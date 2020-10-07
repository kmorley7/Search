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

    #we use a list to build the mapping file
    mappings = []

    #Loop over all files in the given directory
    for file in files:
        if file.endswith(".html"):
            inputFile = os.path.join(inputDir,file)

            m.parse(inputFile) #the tokenization happens inside this function

            mappings.append((m.doc_num, inputFile))

            end = time.time()
            elapsed_time.append(end - start)

    #write out all the output files
    dict_file = {}
    with open(os.path.join(outputDir, "postings.txt"), "w") as f:
        for w in m.index:
            #count the number of entries and get the offset of the inverted index file we are writing to
            num_docs = len(m.index[w])
            offset = f.tell()
            dict_file[w] = (num_docs, offset)
            for x in m.index[w]:
                f.write("{} {}\n".format(x[0], x[1]))

    with open(os.path.join(outputDir, "dictionary.txt"), "w") as f:
        for w in sorted(dict_file):
            f.write("{}, {}, {}\n".format(w, dict_file[w][0], dict_file[w][1]))

    #write out the mappings file
    with open( os.path.join(outputDir, "mappings.txt"), "w") as f:
        for w in mappings:
            f.write("{} {}\n".format(w[0], w[1]))

    print("Ran in {} seconds.".format(elapsed_time[-1]))



def search(token, outputDir):
    num_files = 0
    offset = 0
    with open(os.path.join(outputDir, "dictionary.txt"), "rt") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if token == row[0]:
                num_files = int(row[1])
                offset = int(row[2])
                print(row)

    docs = []
    if num_files != 0:
        with open(os.path.join(outputDir, "postings.txt"), "r") as f:
            reader = csv.reader(f, delimiter=" ")
            f.seek(offset)
            for i in range(num_files):
                line = next(reader)
                print(line)
                docs.append(line[0])
    else:
        print("No files found with keyword: {}".format(token))
        return

    with open(os.path.join(outputDir, "mappings.txt"), "r") as f:
        reader = csv.reader(f, delimiter=" ")
        for row in reader:
            if row[0] in docs:
                print(row)

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

    search("watchdog", outputDir)



