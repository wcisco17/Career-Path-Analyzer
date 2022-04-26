from nltk.corpus import stopwords
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from careers_helpers import remove_unused_columns, transform_profession, preprocess_text
from sklearn.svm import LinearSVC
from sklearn import metrics

"""
    clean_data_set():
        We first clean the data-set by categorizing the data-set into section 
        [category_id, categories, profession, clean_text_profession] we also 
        remove any stop words from the profession table which we then return as
        the clean_text_profession.  
"""


def clean_data_set(data_csv):
    data_top = remove_unused_columns(data_csv)[0:13]

    # Get our columns into lists
    headline_categories = list(data_csv['Industry'])
    profession = transform_profession(data_top, data=data_csv)
    category_list = data_csv['Headline']
    category_id = [i for i in range(len(category_list))]

    # Initialize our columns into a dataframe
    dtf = pd.DataFrame()
    dtf['category_id'] = category_id
    dtf['categories'] = headline_categories
    dtf['profession'] = profession

    # Clean your data set first remove unwanted words like: "I", "me", "you"
    list_stop_of_words = stopwords.words('english')
    dtf['clean_text_profession'] = dtf['profession'].apply(
        lambda x: preprocess_text(x, flg_stemm=False, flg_lemm=True, lst_stopwords=list_stop_of_words)
    )

    return dtf


"""
    vectorize_data_set():
        Transform our data-set by applying TFIDF and CountVector  
"""


def vectorize_data_set(dtf):
    # split our data set into two training and testing
    x_train, x_test, y_train, y_test = train_test_split(dtf['clean_text_profession'], dtf['categories'], test_size=0.4)

    # transform our data-set by applying TFIDF
    count_vect = CountVectorizer()
    x_train_counts = count_vect.fit_transform(x_train)
    tfidf_transformer = TfidfTransformer()
    x_train_tfidf = tfidf_transformer.fit_transform(x_train_counts)

    return x_train_counts, x_train_tfidf, y_train, count_vect, y_test, x_test


"""
    predict_headline():
        Returns a prediction based on the general input
"""


def predict_headline(cl, item, count_vect) -> str:
    return cl.predict(count_vect.transform([item]))[0]


"""
    apply_prediction_linear_svc():
        Applying prediction using Linear SVC (our best performing model)
"""


def apply_prediction_linear_svc(dtf, profession):
    x_train_counts, x_train_tfidf, y_train, count_vect, y_test, x_test = vectorize_data_set(dtf)
    clf = LinearSVC()
    linear_svc = clf.fit(x_train_tfidf, y_train)
    linear_svc_prediction = linear_svc.predict(count_vect.transform(x_test))
    accuracy_score = metrics.accuracy_score(y_test, linear_svc_prediction)

    result = predict_headline(linear_svc, profession, count_vect) if len(profession) >= 0 else None

    return result, accuracy_score
