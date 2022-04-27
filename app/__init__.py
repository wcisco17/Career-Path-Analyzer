from typing import List

import streamlit as st
import pandas as pd
from pandas import DataFrame

from bag_of_words import clean_data_set, apply_prediction_linear_svc
from careers_helpers import load_data, get_freq_industry, spacing
from predictions import filter_members_by_industry, get_average_length_industry, filter_members_by_job_title, \
    get_type_of_college_percentage

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

    # job_title = col2.text_input('Exp: Cloud Engineer, Sales Associate, Business Analysis')
    job_title = 'Product Manager'

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

    col1.metric("Members Count", f"{len(data)} members")
    col2.metric("Average duration in the industry", f"{round(average_length, 1)} years")
    spacing(st, 3)

    get_type_of_college_percentage(data)


def main_page():
    st.header('Career Path Analysis')

    st.text(r'''
        The purpose of this research is to provide working professionals and soon to be 
        college graduates a clear layout of the requirements and skills needed to be ready 
        for the current market.
    ''')

    if st.checkbox('Toggle to view the full introduction about the project'):
        showcase_data_set()

    # showcasing input data for prediction
    showcase_input_data_set()


if __name__ == '__main__':
    main_page()
