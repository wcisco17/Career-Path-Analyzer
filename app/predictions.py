"""
    Predictions
"""
import re
from typing import List

import nltk

from bag_of_words import apply_prediction_linear_svc, preprocess_text
from pandas import DataFrame


def get_col_length(data: DataFrame) -> int:
    col_length: str = list(data.columns)[:-2][-1]

    # noinspection PyTypeChecker
    col_length = int(col_length[col_length.find('-') + 1:])
    # noinspection PyTypeChecker
    return col_length


def construct_col_values_arr(col_name: str, col_length: int, data: DataFrame) -> [[List]]:
    col = [f"{col_name}-{col + 1}" for col in range(col_length)]
    row = [col for _ in range(len(data))]
    row_items = [['' for _ in col] for _ in range(len(data))]

    for i, value in enumerate(row):
        for j, item in enumerate(value):
            row_items[i][j] = list(data.get(item))[i]

    return row_items


"""
    filter_members_by_job_title
    
    :return [['Software Engineer', 'None', '']] 
"""


def filter_members_by_job_title(dtf: DataFrame, filtered_data: DataFrame, prediction_txt: str) -> [[List]]:
    col_length = get_col_length(filtered_data)
    job_titles = construct_col_values_arr('Job-Title', col_length, filtered_data)

    result = [['' for _ in range(col_length)] for _ in range(len(filtered_data))]

    for i, profile_jobs in enumerate(job_titles):
        for j, jobs in enumerate(profile_jobs):
            job = jobs if type(jobs) is str else ''

            pred, _ = apply_prediction_linear_svc(dtf, job)
            if pred != prediction_txt:
                result[i][j] = 'None'
            else:
                result[i][j] = pred

    return result


"""
    filter_members_by_industry():
        Filters member based on their industry
"""


def filter_members_by_industry(prediction_txt: str, data: DataFrame) -> DataFrame:
    data['category_id'] = [i for i in range(len(data.get('Industry')))]

    filtered_data = data.query(f'Industry == @prediction_txt')
    return filtered_data


"""
    get_average_length_industry():
        Gets the average length in the industry (Need to check for each job title)
        
    requirements:
        - if the job title includes the following in the list then add to month []
"""


def get_average_length_industry(data: DataFrame, job_titles_industry: [[List]]) -> float:
    average_by_year = 0
    col_length = get_col_length(data)
    duration = construct_col_values_arr('Employment-Duration', col_length, data)
    d = {}
    for (i, value), (_, jobs) in zip(enumerate(duration), enumerate(job_titles_industry)):
        res_m = 0
        res_y = 0
        for item, job in zip(value, jobs):
            if job != 'None':
                if type(item) is str:
                    y_item = 0
                    m_item = 0
                    nums = re.findall('[0-9]+', item)
                    if len(nums) == 2:
                        y, m = nums
                        m_item += int(m)
                        y_item += int(y)
                    elif len(nums) == 1:
                        if item.find('y') != -1:
                            num = re.findall('[0-9]+', item)
                            num_y = num[0] if len(num) == 1 else 0
                            y_item += int(num_y)
                        elif item.find('m') != -1:
                            num = re.findall('[0-9]+', item)
                            num_m = num[0] if len(num) == 1 else 0
                            m_item += int(num_m)

                    res_y += y_item
                    res_m += m_item
        res_m = round((res_m / 12), 1)
        d[i] = (res_y, res_m)

    # get average by month ()
    # get average by year ()
    count = 0
    for i in range(len(d)):
        year, _ = d[i]
        count += year
    average_by_year = count / len(d)

    return average_by_year


"""
    get_type_of_college_percentage():
        Gets the percentage of profiles that have a Bachelors degree. (Based on the prediction)
        - returns the % of bachelor degree
        - should also return the colleges they went for their masters degree.
"""


def get_type_of_college_percentage(filtered_data: DataFrame) -> dict:
    col_length = get_col_length(filtered_data)
    degree_name = construct_col_values_arr('Degree-Name', col_length, filtered_data)
    institutions = construct_col_values_arr('College-Name', col_length, filtered_data)
    results = dict(
        {'Bachelor': 0, 'Masters': 0, 'PHD': 0, 'Juris-Doctor': 0, 'Certificate': 0, 'High-School': 0, 'Associate': 0})
    for degrees, institution in zip(degree_name, institutions):
        for i in range(len(degrees)):
            if type(degrees[i]) is str and type(institution[i]) is str:
                degree = re.sub(r'[^\w\s]', '', degrees[i].lower())
                uni = re.sub(r'[^\w\s]', '', institution[i].lower())

                # bachelors
                if degree.find('bache') != -1 or (degree == 'ba' and uni.find('uni') != -1):
                    results['Bachelor'] += 1

                # masters
                elif degree.find('master') != -1 or degree == 'mba' or degree.find('mba') != -1:
                    results['Masters'] += 1

                # phd
                elif degree.find('phd') != -1:
                    results['PHD'] += 1

                # judicial
                elif degree.find('juris') != -1 or degree.find('jd') != -1:
                    results['Juris-Doctor'] += 1

                # certificate
                elif degree.find('certi') != -1 or degree.find('academ') != -1 or uni.find('school') != -1 or uni.find(
                        'assembly') != -1:
                    results['Certificate'] += 1

                # high-school
                elif degree.find('high') != -1:
                    results['High-School'] += 1

                # associate
                elif degree.find('asso') != -1:
                    results['Associate'] += 1
    return results


"""
    get_most_attended_schools():
        Most attended schools 
"""


def get_most_attended_schools(filtered_data: DataFrame) -> dict:
    freq_schools = dict()
    col_length = get_col_length(filtered_data)
    colleges = construct_col_values_arr('College-Name', col_length, filtered_data)
    for ko in colleges:
        for college in ko:
            if type(college) is str:
                if college not in freq_schools:
                    freq_schools[college] = 1
                else:
                    freq_schools[college] += 1
    res = {}
    for value in freq_schools:
        if freq_schools[value] >= 2:
            res[value] = freq_schools[value]
    return res


"""
    get_first_role():
        Pulls the first role from each profile and showcases them exp:
        - 30% of the profiles first role was [Junior Software Engineer]
"""


def get_first_role():
    pass


"""
    get_popular_companies():
        Pulls the most frequent companies that appears in the data-set.
        - 40% of the profiles went to Google as one of their first jobs. 
"""


def get_popular_companies(filtered_data: DataFrame) -> dict:
    col_length = get_col_length(filtered_data)
    companies = construct_col_values_arr('Company-Name', col_length, filtered_data)
    all_company = dict()
    for comp in companies:
        for company in comp:
            if type(company) is str:
                clean_company = preprocess_text(
                    re.sub(
                        r'[^\w\s]', '',
                        company.replace('.com', '').lower()
                    )
                ).replace('fulltime', '').strip()
                if clean_company not in all_company:
                    all_company[clean_company] = 1
                else:
                    all_company[clean_company] += 1

    for i in all_company:
        if all_company[i] == 1:
            for item in i.split():
                if item in all_company:
                    all_company[item] += 1
    res = {}

    for i in all_company:
        if all_company[i] >= 3:
            res[i] = all_company[i]

    return res


"""
    get_first_role_length():
        Gets the length of time one has work at their first job. 
"""


def get_first_role_length(filtered_data: DataFrame) -> float:
    col_length = get_col_length(filtered_data)
    duration = construct_col_values_arr('Employment-Duration', col_length, filtered_data)
    duration = [[value if type(value) is str else '' for value in dates] for dates in duration]
    result = []
    # re.findall('[0-9]+', item)
    for value in duration:
        end = len(value) - 1
        while end >= 0:
            if len(value[end]) <= 0:
                end -= 1
            else:
                result.append(value[end])
                break
    freq_by_year = 0
    total_year = 0
    total_month = 0
    for res in result:
        if res.find('y') != -1:
            freq_by_year += 1
            nums = re.findall('[0-9]+', res)
            if len(nums) == 2:
                y, m = nums
                total_year += int(y)
                total_month += int(m)
            elif len(nums) == 1:
                total_year += int(nums[0])
        elif res.find('m') != -1:
            nums = re.findall('[0-9]+', res)
            num = int(nums[0]) if len(nums) == 1 else 0
            total_month += num

    return round(total_year / freq_by_year, 1)


def get_popular_field_of_study(filtered_data: DataFrame) -> dict:
    col_length = get_col_length(filtered_data)
    field_of_study = construct_col_values_arr('Field-Of-Study', col_length, filtered_data)
    study_items = dict()

    for studies in field_of_study:
        for study in studies:
            if type(study) is str:
                text = preprocess_text(study)
                if text not in study_items:
                    study_items[text] = 1
                else:
                    study_items[text] += 1
    res = {}
    for value in study_items:
        if study_items[value] >= 2:
            res[value] = study_items[value]

    return res


def get_popular_skills(filtered_data: DataFrame) -> List:
    skills = []
    for item in list(filtered_data['skills']):
        if type(item) is str:
            skills.append(item)

    return skills
