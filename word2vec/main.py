import csv
import pandas as pd

"""The following py file is using SKIP-GRAM model which predicts the context of the word given the word itself. The 
context of the word can be represented through a SKIP-GRAM pairs of (target_word, context_word). Where (context_word) 
appears in the neighboring context of (target_word). 
    
    The goal of this file is to utilize the word2vec algo using the SKIP-GRAM model and generate a 
    - [target]  
    - [context]
    - [label]  
    The result of this will give us a training example from a sentence.
    
    The next steps are to combine our dataset all together and put all all sentences into a single training list().
    We'll then classify words by their similarities using Word2vec and calculate the accuracy score.
    --
    We wrap this up by combining the groups by categories based on the [Industry] column.  
    
    - having rules
        - all the rule stuff down to the feature level
    - hybrid approach [classifying]
    - the combination of both (word2vec).
    - use a range of valuation
        - combine outputs ()
        - Look into -> SVM works well with dimensionality
        - Feature enrichment is crucial (maybe get more data?)
        - transformer model that are (pretrained) - (wikipedia).
    
    - [FINAL_combination] set the own baseline
"""

sentence = """
Hello my name is Profile_1 I am a [Business Analyst] and my previous role was as a [Software Engineer at Google]. 
I studied Computer Science at Middlesex University and have a master in Machine Learning / AI at Carnegie Mellon.
"""

# tokenizing the sentence
tokens = list(sentence.lower().replace('/', '').split())
print(tokens)

# save the mappings to integers indexes

# def read_file():
#     # read in our data set
#     data = pd.read_csv('../excel-data/all-data-linkedin.csv')
#     print(data.get('Headline'))
#     print(data.keys())


# if __name__ == '__main__':
#     read_file()
