import sys
import time
from HTMLLexer import HTMLLexer
from DictionaryHandler import DictionaryHandler
from Stopwords import Stopwords


if __name__ == "__main__":
    start = time.time()

    if len(sys.argv) > 1:
        words = str(sys.argv[1:])
    else:
        print("You must enter a word to search for.")
        quit()

    # use the tokenizer on our input words
    lexer = HTMLLexer()
    lexer.build()
    tokens = lexer.tokenize(words)

    # Open the dictionary file for reading from
    dictionary = DictionaryHandler()
    dictionary.openFile("output/dictionary.txt")

    accumulator = {}

    # Query processing algorithm
    for token in tokens:
        if token in Stopwords:
            break

        w, num_docs, offset = dictionary.getEntry(token)

        if w is not None:  # w is None when the token does not exist in the dictionary
            with open("output/postings.txt", "r") as f:
                f.seek(offset)

                for i in range(num_docs):
                    doc_id, wt = f.readline().split()

                    # add the weight to the accumulator
                    if int(doc_id) in accumulator.keys():
                        accumulator[int(doc_id)] = accumulator[int(doc_id)] + float(wt)
                    else:  # for the first time we come across the document, we must initialize the value of accumulator
                        accumulator[int(doc_id)] = float(wt)

    # Sort the accumulator
    results = []
    weights = []
    for i in sorted(accumulator, key =accumulator.get, reverse=True):
        if accumulator[i] > 0:
            results.append(i)
            weights.append(accumulator[i])

    if len(results) == 0:
        print("No files found.")

    # display the top 10 documents
    with open("output/mappings.txt", "r") as f:
        for i in range(10):
            if i >= len(results):
                break

            file_number = results[i]
            f.seek((file_number-1)*69)
            print("{}: {} {} {}".format(i+1, results[i], f.readline()[4:68].strip(), weights[i]))


    end = time.time()
    print("Ran in {:f} seconds.".format(end-start))
