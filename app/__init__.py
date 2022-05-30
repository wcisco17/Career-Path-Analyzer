from typing import List

import streamlit as st
import pandas as pd
from pandas import DataFrame
from bag_of_words import clean_data_set, apply_prediction_linear_svc
from careers_helpers import load_data, get_freq_industry, spacing, plot_graph_horizontal
from predictions import filter_members_by_industry, get_average_length_industry, filter_members_by_job_title, \
    get_type_of_college_percentage, get_most_attended_schools, get_popular_companies, get_first_role_length, \
    get_popular_field_of_study, get_popular_skills

RAW_DATA = load_data(185)


def showcase_data_set():
    st.text(r'''
        Furthermore, the plan is to use publicly available data from employees in different 
        industries, analyze their career path, education, current title and make a semi-accurate 
        prediction and see which profiles correlates to theirs the most. The goal is to be 
        able to answer most of these daunting questions one has when looking for a job in the 
        current market, and provide deep analysis using standard machine learning algorithms 
        to make the following prediction as an example: 
    ''')

    st.markdown('***Disclaimer: These should serve as an example of an output from our best performing algorithm.***')

    st.markdown(r'''
        1. 50% of the profiles nearest to you have a master's degree.
        2. 25% of the profiles have 2-3 years of experience.
        3. 25% of the profiles are software engineers.
    ''')

    load_state = st.text('Loading data set...')
    profiles_csv = load_data(5)
    load_state.text('')

    st.subheader('Raw Data (From LinkedIn)')
    st.text(r'''Here's an example of the data set that we'll be using for our project''')
    st.write(profiles_csv)

    st.text(r'''Our labels are in the Industry column, here's an example of the overall figure:''')

    list_data = RAW_DATA
    industry_columns, frequency_item = get_freq_industry(list(list_data['Industry']))

    chart_data = pd.DataFrame(
        [frequency_item],
        columns=industry_columns
    )

    st.bar_chart(chart_data)


def showcase_input_data_set():
    st.subheader('Enter the job title you wish to have after graduation')
    col1, col2 = st.columns(2)

    col1.subheader('I want to work in: ')

    job_title = col2.text_input('Exp: Cloud Engineer, Sales Associate, Business Analysis')

    dtf = clean_data_set(RAW_DATA)
    prediction, accuracy_score = apply_prediction_linear_svc(dtf, job_title)

    if len(job_title) > 0:
        filtered_data = filter_members_by_industry(prediction, RAW_DATA)
        job_titles_industry = filter_members_by_job_title(dtf, filtered_data, prediction)

        spacing(st, 3)
        st.subheader(f"{prediction} Industry with {round(accuracy_score, 2)}% rate")
        spacing(st, 1)

        showcase_metric(filtered_data, job_titles_industry)


def showcase_metric(data: DataFrame, job_titles_industry: [[List]]):
    col1, col2, col3 = st.columns(3)
    average_length = get_average_length_industry(data, job_titles_industry)
    college_count = get_type_of_college_percentage(data)
    frequent_schools = get_most_attended_schools(data)
    length_of_first_role = get_first_role_length(data)
    popular_field_of_study = get_popular_field_of_study(data)

    bachelor_percentage = (round(college_count.get('Bachelor') / len(data), 2))

    col1.metric("Members Count", f"{len(data)} members")
    col2.metric("Average duration in the industry", f"{round(average_length, 1)} years")
    col3.metric("% with a Bachelor", f"{bachelor_percentage}%")
    st.metric('Length of stay in their first job', f"{length_of_first_role} years")
    spacing(st, 3)

    education_section(college_count, frequent_schools, popular_field_of_study)
    industry_section(data)


def industry_section(data: DataFrame):
    st.subheader('Industry Stats')
    with st.expander("Popular Companies"):
        popular_companies = get_popular_companies(data)
        graph_popular_companies = plot_graph_horizontal(
            popular_companies.keys(),
            popular_companies.values(),
            '# of people',
            'Popular Companies',
            10
        )
        st.pyplot(graph_popular_companies)
    with st.expander('Sought after after skills'):
        st.text('Skills')
        skills = get_popular_skills(data)
        for items in skills:
            st.markdown(f"""
                <li>{items}</li>    
            """, unsafe_allow_html=True)


def education_section(college_count: dict, frequent_schools: dict, popular_field_of_study: dict):
    st.subheader('Education Stats')
    spacing(st, 2)
    education, education_count = college_count.keys(), college_count.values()
    schools, schools_count = frequent_schools.keys(), frequent_schools.values()
    field_study, field_study_count = popular_field_of_study.keys(), popular_field_of_study.values()

    graph_college_count = plot_graph_horizontal(
        education,
        education_count,
        '# of people',
        'Showcasing the education level in the current market',
        25
    )

    graph_frequent_schools = plot_graph_horizontal(
        schools,
        schools_count,
        '# of people',
        'School attended in corpus',
        10
    )

    graph_frequent_study = plot_graph_horizontal(
        field_study,
        field_study_count,
        '# of people',
        'School attended in corpus',
        10
    )

    with st.expander("Highest Education level Chart"):
        st.pyplot(graph_college_count)
    with st.expander("Most attended School"):
        st.pyplot(graph_frequent_schools)
    with st.expander('Popular Field of study'):
        st.pyplot(graph_frequent_study)


def main_page():
    st.header('Career Path Analysis')

    st.text(r'''
        The purpose of this research is to provide working professionals and soon to be 
        college graduates a clear layout of the requirements and skills needed to be ready 
        for the current market.
    ''')

    with st.expander('Toggle to view the full introduction about the project'):
        showcase_data_set()

    # showcasing input data for prediction
    showcase_input_data_set()


if __name__ == '__main__':
    main_page()
