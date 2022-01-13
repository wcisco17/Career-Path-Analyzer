import csv

from lib.clean_html import (get_education_list, get_experience, get_headline,
                        get_industry, get_skills)
from lib.helper import check_null, extract_values

# from html_test import profile1, profile2, profile3


def education_list_structure(profile):
    all_edu = get_education_list(profile)
    constant_values = {}
    activities = None
    for i, edu in enumerate(all_edu):
        values = i + 1
        colleges = check_null(all_edu[i][0:1][0])

        constant_values[f'College-Name-{values}'] = colleges

        constant_values[f'Degree-Name-{values}'] = ''
        constant_values[f'Field-Of-Study-{values}'] = ''
        constant_values[f'Activities-and-Societies-{values}'] = ''

        if edu.__contains__('Degree Name'):
            extract_values(all_edu, constant_values, i, values,
                           header='Degree Name', headIdx='Degree-Name')

        if edu.__contains__('Field Of Study'):
            extract_values(all_edu, constant_values, i, values,
                           header='Field Of Study', headIdx='Field-Of-Study')

        if edu.__contains__('Activities and Societies:'):
            if activities == []:
                activities = ''
            else:
                extract_values(all_edu, constant_values, i, values,
                               header='Activities and Societies:', headIdx='Activities-and-Societies-')

        # if edu.__contains__('Dates attended or expected graduation'):
        #     constant_values[f'Dates-{values}'] = dates

    return constant_values


def experience_structure(profile):
    experiences = get_experience(profile)
    constant_values = {}
    for i in range(len(experiences)):
        values = i + 1
        title = check_null(experiences[i][0:1][0])

        if title:
            constant_values[f'Job-Title-{values}'] = title

        if experiences[i].__contains__('Title'):
            extract_values(experiences, constant_values,
                           i, values, header='Title', headIdx='Job-Title')

        if experiences[i].__contains__('Company Name'):
            extract_values(experiences, constant_values, i,
                           values, header='Company Name', headIdx='Company-Name')

        if experiences[i].__contains__('Dates Employed'):
            extract_values(experiences, constant_values, i, values,
                           header='Dates Employed', headIdx='Dates-Employed')

        if experiences[i].__contains__('Employment Duration'):
            extract_values(experiences, constant_values, i, values,
                           header='Employment Duration', headIdx='Employment-Duration')

        if experiences[i].__contains__('Location'):
            extract_values(experiences, constant_values,
                           i, values, header='Location', headIdx='Location')

    return constant_values


def skills_structure(profile):
    skills = get_skills(profile)
    a = ','
    return {"skills": a.join(skills)}


def generate_col(end):
    csv_col = []
    csv_col.append('Headline')
    csv_col.append('Industry')
    for i in range(1, end):
        csv_col.append(f"College-Name-{i}")
        csv_col.append(f"Degree-Name-{i}")
        csv_col.append(f"Field-Of-Study-{i}")
        csv_col.append(f"Activities-and-Societies-{i}")
        csv_col.append(f"Activities-and-Societies--{i}")
        # csv_col.append(f"Dates-{i}")

        csv_col.append(f"Job-Title-{i}")
        csv_col.append(f"Company-Name-{i}")
        csv_col.append(f"Dates-Employed-{i}")
        csv_col.append(f"Employment-Duration-{i}")
        csv_col.append(f"Location-{i}")
    csv_col.append("skills")
    return csv_col


def Merge(dict1, dict2, dict3, dict4, dict5):
    res = {**dict1, **dict2, **dict3, **dict4, **dict5}
    return res


def merge_structures(profile):
    industry = get_industry()
    edu = education_list_structure(profile)
    headline = get_headline(profile)
    experience = experience_structure(profile)
    skills = skills_structure(profile)
    all_profiles = Merge(industry, headline, edu, experience, skills)
    return all_profiles


"""
    @TEST DATA EXCEL
"""


# def merge_structures(all):
#     col = generate_col(7)
#     all_profile = None
#     with open('machine-learning.csv', 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=col)
#         writer.writeheader()
#         for profile in all:
#             industry = get_industry()
#             edu = education_list_structure(profile)
#             headline = get_headline(profile)
#             experience = experience_structure(profile)
#             skills = skills_structure(profile)
#             all_profile = Merge(industry, headline, edu, experience, skills)
#             writer.writerow(all_profile)


# profi = [profile1, profile2, profile3]

# merge_structures(profi)
