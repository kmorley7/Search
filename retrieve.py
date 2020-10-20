import sys
import time
from HTMLLexer import HTMLLexer
from DictionaryHandler import DictionaryHandler


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

    #The dictionary
    dictionary = DictionaryHandler()
    dictionary.openFile("output/dictionary.txt")

    accumulator = {}
    for token in tokens:
        w, num_docs, offset = dictionary.getPosting(token)

        if w is not None:  # w is None when the token does not exist in the dictionary
            with open("output/postings.txt", "r") as f:
                f.seek(offset)

                for i in range(num_docs):
                    doc_id, wt = f.readline().split()

                    if int(doc_id) in accumulator.keys():
                        accumulator[int(doc_id)] = accumulator[int(doc_id)] + float(wt)
                    else:
                        accumulator[int(doc_id)] = float(wt)

    # Sort the accumulator
    results = []
    for i in sorted(accumulator, key =accumulator.get, reverse=True):
        if accumulator[i] > 0:
            results.append(i)

    # display the top 10 documents
    with open("output/mappings.txt", "r") as f:
        for i in range(10):
            if i >= len(results):
                break

            file_number = results[i]
            f.seek((file_number-1)*69)
            print("{}: {}".format(i+1 ,f.readline()[4:68]))

    end = time.time()
    print("Ran in {:f} seconds.".format(end-start))
