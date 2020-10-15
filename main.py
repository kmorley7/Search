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



def search(token, outputDir):


    num_files = 0
    offset = 0

    with open(os.path.join(outputDir, "dictionary.txt"), "rt") as f:
        reader = csv.reader(f, delimiter=",")

        read = False
        i = 0
        while not read and i < 38000:
            h = self.hash(token, i) * self.line_length
            f.seek(h)
            line = f.readline()
            if line[0:12] == "{:12.12}".format(token):
                return line.split()
            else:
                i = i+1

        if not read:
            print("Record not found")




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







