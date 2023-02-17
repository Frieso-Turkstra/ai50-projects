import nltk
import sys
import os
from nltk.tokenize import word_tokenize
import string
import numpy as np

# nltk.download("stopwords")

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    i = 0 # temp
    while i < 10: #temp
        i += 1
        # Prompt user for query
        query = set(tokenize(input("Query: ")))

        # Determine top file matches according to TF-IDF
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

        # Extract sentences from top files
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens

        # Compute IDF values across sentences
        idfs = compute_idfs(sentences)

        # Determine top sentence matches
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as f:
            text = f.read()
        files[filename] = text
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    return [
        word for word in word_tokenize(document.lower())
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")
    ]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # get all unique words from all documents
    words = {word for words in documents.values() for word in words}

    # calculate idf for each word
    idfs = dict()
    for word in words:
        docs_with_word = sum([1 for document in documents.values() if word in document])
        idfs[word] = np.log(len(documents) / docs_with_word)
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    return sorted(
        files,
        key=lambda x: sum([files[x].count(word) * idfs[word] for word in query if word in files[x]]),
        reverse=True
    )[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # create a list of tuples containing the sentence and its cumulative idf-value
    ranks = [(sentence, sum([idfs[word] for word in query if word in words])) for sentence, words in sentences.items()]

    # bubble sort
    unsorted = True

    while unsorted:
        unsorted = False

        for i in range(len(ranks)-1):

            # if the next is greater than the current, swap
            if ranks[i][1] < ranks[i+1][1]:
                unsorted = True
                ranks[i], ranks[i+1] = ranks[i+1], ranks[i]

            # if they are equal, check their query term densities (qtd)
            elif ranks[i][1] == ranks[i+1][1]:
                qtd_0 = sum([1 for word in sentences[ranks[i][0]] if word in query]) / len(sentences[ranks[i][0]])
                qtd_1 = sum([1 for word in sentences[ranks[i+1][0]] if word in query]) / len(sentences[ranks[i+1][0]])
                # if the next qtd is higher than the current qtd, swap
                if qtd_1 > qtd_0:
                    ranks[i], ranks[i+1] = ranks[i+1], ranks[i]

    # retrieve only the sentences from the tuples in ranks
    results = [ranks[i][0] for i in range(len(ranks)-1)]
    return results[:n]


if __name__ == "__main__":
    main()
