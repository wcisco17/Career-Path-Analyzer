"""
    Predictions
"""
import re
from typing import List
from bag_of_words import apply_prediction_linear_svc
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
    get_bachelor_percentage():
        Gets the percentage of profiles that have a Bachelors degree. (Based on the prediction)
        - returns the % of bachelor degree
        - should also return the colleges they went for their masters degree.
"""


def get_type_of_college_percentage(filtered_data: DataFrame):
    col_length = get_col_length(filtered_data)
    degree_name = construct_col_values_arr('Company-Name', col_length, filtered_data)
    print(degree_name)


"""
    get_first_role():
        Pulls the first role from each profile and showcases them exp:
        - 30% of the profiles first role was [Junior Software Engineer]
"""


def get_first_role():
    pass


"""
    get_education_percentage():
        Pulls the education percentage based on the LinkedIn group.
        - 40% have a bachelor degree.
        - 60% have a masters degree. 
"""


def get_education_percentage():
    pass


"""
    get_popular_companies():
        Pulls the most frequent companies that appears in the data-set.
        - 40% of the profiles went to Google as one of their first jobs. 
"""


def get_popular_companies():
    pass


"""
    get_first_role_length():
        Gets the length of time one has work at their first job. 
"""


def get_first_role_length():
    pass
