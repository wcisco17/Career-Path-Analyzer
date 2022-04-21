import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('wordnet')


def remove_unused_columns(data_columns):
    columns = list()
    for i, item in enumerate(data_columns):
        if item != 'Activities-and-Societies-1' \
                and item != 'Activities-and-Societies--1' \
                and item != 'skills' and item != 'Activities-and-Societies-2' \
                and item != 'Activities-and-Societies--2':
            columns.append(item)
    return columns


def is_fine(st: str) -> str:
    item = ""
    if type(st) is str:
        item = st
    else:
        item = " Not Applicable"

    return item


def transform_profession(data_top, data):
    profiles = [['' for i in range(0, 13)] for i in range(len(data))]
    profiles_profession = list()

    for top in range(len(data_top)):
        value = data.get(data_top[top]).values
        for idx in range(len(value)):
            profiles[idx][top] = value[idx]

    for col in range(len(profiles)):
        role = ""

        job_title = profiles[col][5] if type(profiles[col][5]) is str else ""
        is_space_in_job_title = True if " " in job_title else False
        headline = profiles[col][0]

        for i in range(len(profiles[col])):
            employed = profiles[col][7]
            if employed is not None:
                if type(employed) is str:
                    # check if the profile is in fact employed if true then we take the job_title col
                    if str(employed).find('Present') != -1:
                        # we check if there is a space if so grab the Headline instead to get more info
                        if is_space_in_job_title is False:
                            role = profiles[col][0]
                        else:
                            role = job_title
                    else:
                        role = headline
                else:
                    role = headline

        profiles_profession.append(role)

    return profiles_profession


# This function will preprocess our professions into one single list.
def preprocess_text(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    # remove punctuations and mark as lowercase
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


def transform_text():
    data = pd.read_csv('../excel-data/1_update-linkedin.csv')
    data_top = remove_unused_columns(data)[0:13]
    all_profiles = [['' for i in range(0, 13)] for i in range(len(data))]
    profiles_intro_text = list()

    for top in range(len(data_top)):
        value = data.get(data_top[top]).values
        for idx in range(len(value)):
            all_profiles[idx][top] = value[idx]

    for col in range(len(all_profiles)):
        text = ""
        role = ""
        edu = ""
        other_studies = ""
        for _ in range(len(all_profiles[col])):
            employed = all_profiles[col][7]
            college = all_profiles[col][2]
            field_of_study = all_profiles[col][4]
            master_college_name = all_profiles[col][10]
            master_field_study = all_profiles[col][12]

            if master_college_name is not None or master_field_study is not None:
                other_studies = f"masters at {is_fine(master_college_name)} in {is_fine(master_field_study)}."

            if college is not None or field_of_study is not None:
                edu = f"I studied {is_fine(field_of_study)} at {is_fine(college)}"

            if employed is not None:
                if type(employed) is str:
                    if str(employed).find('Present') != -1:
                        role = "I currently am in the" + all_profiles[col][5] + " working for " + is_fine(
                            all_profiles[col][6])
                    else:
                        role = "I currently am a " + all_profiles[col][0] + " working for " + is_fine(
                            all_profiles[col][6])
                else:
                    role = "I currently am a " + all_profiles[col][0] + is_fine(all_profiles[col][6])

            text = f"Hello my name is Profile_{col} {role} " \
                   f"{edu} and have a {other_studies} "
        profiles_intro_text.append(text)

    x_train = list()
    x_test = list()
    for i in range(0, 70):
        x_test.append(profiles_intro_text[i])

    for i in range(len(profiles_intro_text)):
        x_train.append(profiles_intro_text[i])

    return x_train, x_test


def main():
    file = '../excel-data/all-data-linkedin.csv'
    data_csv = pd.read_csv(file)
    data_top = remove_unused_columns(data_csv)[0:13]
    tr = transform_profession(data_top, data_csv)
    # list_stop_word = preprocess_text(tr[0], flg_stemm=False, flg_lemm=True, lst_stopwords=stopwords)
