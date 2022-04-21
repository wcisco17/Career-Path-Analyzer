import csv

from clean_html import (get_education_list, get_experience, get_headline,
                        get_industry, get_skills)
from helper import check_null, extract_values
from html_test import profile_u_1, profile_u_8, profile_1, profile_2, profile_3, profile_6

employment_type = ["Please select", "Full-time", "Part-time", "Self-employed", "Freelance", "Contract", "Internship",
                   "Apprenticeship", "Seasonal"]


def education_list_structure(profile):
    education_list = get_education_list(profile)
    constant_values = {}

    for i, all_edu in enumerate(education_list):
        for edu in all_edu:
            i = i + 1
            constant_values[f'College-Name-{i}'] = all_edu[0][0]
            constant_values[f'Degree-Name-{i}'] = all_edu[0][1]

            constant_values[f'Field-Of-Study-{i}'] = all_edu[0][1]
            constant_values[f'Activities-and-Societies-{i}'] = ''
            constant_values[f'Activities-and-Societies--{i}'] = ''
            for e in edu:
                if e.__contains__('societies:') or e.__contains__('Societies:'):
                    is_exist = e.find(':')
                    if is_exist:
                        constant_values[f"{'Activities-and-Societies-'}-{i}"] = e[is_exist + 1:]

    return constant_values


def delete_empty_values(data: [[str]]) -> [[str]]:
    empty_nest = []
    for value in data:
        if len(value) > 1:
            empty_nest.append(value)
    return empty_nest


def experience_structure(profile: str) -> dict:
    experiences, more_exp = get_experience(profile)
    merge_experience: [[str]] = experiences + more_exp
    merge_experience = delete_empty_values(merge_experience)

    constant_values = {}
    for i, all_experience in enumerate(merge_experience):
        value = i + 1

        if all_experience.__contains__('experience'):
            if len(all_experience) >= 3:
                date_idx = all_experience[3].find('-')
                point_idx = all_experience[3].find('·')

                constant_values[f'Job-Title-{value}'] = all_experience[1]
                constant_values[f'Company-Name-{value}'] = all_experience[2]

                if date_idx != -1:
                    constant_values[f'Dates-Employed-{value}'] = all_experience[3][:point_idx - 1]
                else:
                    constant_values[f'Dates-Employed-{value}'] = ""

                if point_idx != -1:
                    constant_values[f'Employment-Duration-{value}'] = all_experience[3][point_idx + 1:].strip()
                else:
                    constant_values[f'Employment-Duration-{value}'] = all_experience[3]

                constant_values[f'Location-{value}'] = ""
            else:
                constant_values[f'Job-Title-{value}'] = ""
                constant_values[f'Company-Name-{value}'] = ""
                constant_values[f'Dates-Employed-{value}'] = ""
                constant_values[f'Employment-Duration-{value}'] = ""
                constant_values[f'Location-{value}'] = ""

            if len(all_experience) >= 6:
                constant_values[f'Location-{value}'] = all_experience[4]

        if all_experience.__contains__('more-experience'):
            if len(all_experience) >= 6:
                exp: str = all_experience[5]
                constant_values[f'Company-Name-{value}'] = all_experience[1]
                constant_values[f'Job-Title-{value}'] = all_experience[4]
                is_one_employment_type: bool = employment_type.__contains__(all_experience[5])

                if is_one_employment_type:
                    constant_values[f'Dates-Employed-{value}'] = all_experience[6]
                else:
                    constant_values[f'Dates-Employed-{value}'] = all_experience[5]

                if exp.find('·') != -1:
                    exp = exp[exp.find('·') + 1:]
                else:
                    exp = all_experience[2]

                constant_values[
                    f'Employment-Duration-{value}'
                ] = exp

                constant_values[f'Location-{value}'] = all_experience[3]
            else:
                constant_values[f'Job-Title-{value}'] = ""
                constant_values[f'Company-Name-{value}'] = ""
                constant_values[f'Dates-Employed-{value}'] = ""
                constant_values[f'Employment-Duration-{value}'] = ""
                constant_values[f'Location-{value}'] = ""

    return constant_values


def skills_structure(profile):
    skills = get_skills(profile)
    return {"skills": skills}


def generate_col(end):
    csv_col = list()
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


def merge(dict1, dict2, dict3, dict4, dict5):
    res = {**dict1, **dict2, **dict3, **dict4, **dict5}
    return res


def merge_structures(profile):
    industry = get_industry()
    edu = education_list_structure(profile)
    headline = get_headline(profile)
    experience = experience_structure(profile)
    skills = skills_structure(profile)
    all_profiles = merge(industry, headline, edu, experience, skills)
    return all_profiles


"""
    @TEST DATA EXCEL
"""


def merge_structures_test_file(test_profiles):
    col = generate_col(14)
    all_profile = {}
    with open('../excel-data/test-profile-1.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=col)
        writer.writeheader()
        for profile in test_profiles:
            industry = {"Industry": "Software Engineer"}
            headline = get_headline(profile)
            edu = education_list_structure(profile)
            experience = experience_structure(profile)
            skills = skills_structure(profile)
            all_profile = merge(industry, headline, edu, experience, skills)
            writer.writerow(all_profile)


profi = [
    profile_6,
    profile_3,
    profile_1,
    profile_2,
    profile_u_8,
    profile_u_1
]

merge_structures_test_file(profi)
