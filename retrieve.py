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
    dictionary.openFile("/home/kem021/Info/Tokenizer/output/dictionary.txt")

    accumulator = {}

    # Query processing algorithm
    for token in tokens:
        if token in Stopwords:
            break

        w, num_docs, offset = dictionary.getEntry(token)

        if w is not None:  # w is None when the token does not exist in the dictionary
            with open("/home/kem021/Info/Tokenizer/output/postings.txt", "r") as f:
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
        quit()

    end = time.time()
    print("Found {} results in {:f} seconds.".format(len(results), end-start))


    # display the top 10 documents
    with open("/home/kem021/Info/Tokenizer/output/mappings.txt", "r") as f:
        for i in results:
            f.seek((i-1)*69)
            print("http://www.csce.uark.edu/~sgauch/{}".format(f.readline()[29:68].strip()))


