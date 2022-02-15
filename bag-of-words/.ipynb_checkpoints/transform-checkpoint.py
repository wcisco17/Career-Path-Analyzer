import csv
import logging
import os
from typing import List

import gensim


def read_file() -> List[str]:
    items = []
    with open("excel-data/word-to-vec-exp.csv", "r") as file:
        reader = csv.reader(file)
        for row in (reader):
            if row[0] != 'Headline':
                items.append(row[0])
    return items


def read_input(items: List[str]):
    for i, line in enumerate(items):
        if i % 10000 == 0:
            logging.info("read {0} headline".format(i))
        yield gensim.utils.simple_preprocess(line)


if __name__ == "__main__":
    abspath = os.path.dirname(os.path.abspath(__file__))

    # initialize the reading process
    items = read_file()
    documents = list(read_input(items))
    logging.info("Done reading file")
    # Build the vocabulary and train our model
    model = gensim.models.Word2Vec(documents, min_count=2)
    model.train(documents, total_examples=len(documents), epochs=10)
    # model.wv.save(os.path.join(abspath, 'vectors'))

    w1 = "engineer"
    resultW1 = model.wv.most_similar(positive=w1)
    # print(f"The most similar word {w1} is similar to: {resultW1}")

    print("\n-------------------------------- ")

    w2 = ["machine"]
    resultW2 = model.wv.most_similar(positive=w2, topn=6)
    # print(f"The top most similar word to {w2} is similar to: {resultW2}")
