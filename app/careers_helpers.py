import pandas as pd
import nltk
import re

nltk.download('stopwords')
nltk.download('wordnet')

DATA_URL = 'https://career-path-analyzer.s3.amazonaws.com/f-linkedin-profile.csv'


def load_data(n_rows: int):
    data = pd.read_csv(DATA_URL, nrows=n_rows)
    return data


def get_freq_industry(industry_col: [str]) -> [str]:
    dup_item = dict()
    freq = 1
    for i, item in enumerate(industry_col):
        if item not in dup_item:
            dup_item[item] = freq
        else:
            dup_item[item] += freq

    industry_item = ['' for _ in dup_item]
    frequency = [0 for _ in dup_item]

    for i, item in enumerate(dup_item):
        frequency[i] = dup_item[item]
        industry_item[i] = item
    return industry_item, frequency


def transform_profession(data_top, data):
    all_profiles = [['' for _ in range(0, 13)] for _ in range(len(data))]
    profiles_profession = list()

    for top in range(len(data_top)):
        value = data.get(data_top[top]).values
        for idx in range(len(value)):
            all_profiles[idx][top] = value[idx]

    for col in range(len(all_profiles)):
        role = ""

        job_title = all_profiles[col][5] if type(all_profiles[col][5]) is str else ""
        is_space_in_job_title = True if " " in job_title else False
        headline = all_profiles[col][0]

        for i in range(len(all_profiles[col])):
            employed = all_profiles[col][7]
            if employed is not None:
                if type(employed) is str:
                    # check if the profile is in fact employed if true then we take the job_title col
                    if str(employed).find('Present') != -1:
                        # we check if there is a space if so grab the Headline instead to get more info
                        if is_space_in_job_title is False:
                            role = all_profiles[col][0]
                        else:
                            role = job_title
                    else:
                        role = headline
                else:
                    role = headline

        profiles_profession.append(role)

    return profiles_profession


def remove_unused_columns(data_columns):
    columns = list()
    for i, item in enumerate(data_columns):
        if item != 'Activities-and-Societies-1' \
                and item != 'Activities-and-Societies--1' \
                and item != 'skills' and item != 'Activities-and-Societies-2' \
                and item != 'Activities-and-Societies--2':
            columns.append(item)
    return columns


# This function will preprocess our professions into one single list.
def preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    # remove all punctuations and mark as lowercase
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    # convert our strings into a list.
    list_text = text.split()
    # remove any stop-words
    list_text = [word for word in list_text if word not in lst_stopwords] if lst_stopwords is not None else ''

    if flg_stemm:
        ps = nltk.stem.porter.PorterStemmer()
        list_text = [ps.stem(word) for word in list_text]

    if flg_lemm:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        list_text = [lem.lemmatize(word) for word in list_text]

    text = " ".join(list_text)

    return text


def spacing(st, num_of_spacing):
    for i in range(0, num_of_spacing):
        st.text('\n')
