"""
    Predictions
"""
import re
from typing import List

from pandas import DataFrame

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


def get_average_length_industry(data: DataFrame) -> int:
    length_industry = 0
    col_length: str = list(data.columns)[:-2][-1]

    # noinspection PyTypeChecker
    col_length = int(col_length[col_length.find('-') + 1:])
    # noinspection PyTypeChecker
    employment_duration = [f"Employment-Duration-{col + 1}" for col in range(col_length)]
    employment_rows = [employment_duration for _ in range(len(data))]
    duration = [['' for _ in employment_duration] for _ in range(len(data))]

    for i, value in enumerate(employment_rows):
        for j, item in enumerate(value):
            duration[i][j] = list(data.get(item))[i]

    d = {}

    for i, value in enumerate(duration):
        res_m = 0
        res_y = 0
        for item in value:
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

        d[i] = (res_y, res_m)

    # get average by month ()
    # get average by year ()

    return length_industry


"""
    get_bachelor_percentage():
        Gets the percentage of profiles that have a Bachelors degree. (Based on the prediction)
        - returns the % of bachelor degree
        - should also return the colleges they went for their masters degree.
"""


def get_bachelor_percentage(data: List):
    pass


"""
    get_masters_percentage():
        Gets the percentage of the profiles that have a masters degree. (Based on the prediction)
        - should return the percentage masters degree
        - should also return the colleges they went for their masters degree.
"""


def get_masters_percentage(prediction: str):
    pass


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
