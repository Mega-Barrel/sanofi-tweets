from plots.weighted_plot import weighted_polarity_line_chart
from plots.polarity_pie import polarity_pie_chart
from plots.polarity_bar import pos_neg_chart
from plots.tweet_trend import tweet_trend_chart
from plots.top_hashtag import plot_hashtag

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title('Sanofi Tweets Analysis')

files = [
    'https://github.com/Mega-Barrel/sanofi-tweets/blob/main/data/clean_data/indiasanofi_data.csv',
    'https://github.com/Mega-Barrel/sanofi-tweets/blob/main/data/clean_data/sanofibrasil_data.csv',
    'https://github.com/Mega-Barrel/sanofi-tweets/blob/main/data/clean_data/sanofide_data.csv',
    'https://github.com/Mega-Barrel/sanofi-tweets/blob/main/data/clean_data/sanofifr_data.csv',
    'https://github.com/Mega-Barrel/sanofi-tweets/blob/main/data/clean_data/sanofius_data.csv'
]

option = st.selectbox(
    'Please slect any 1 file for analysis',
    files
)

@st.cache_data
def read_file(filename):
    df = pd.read_csv(filename)
    return df


if st.button('Generate Analysis'):
    # read file
    df = read_file(option)
    
    file_name = option.split('/')[9].split('.')[0]
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric('Total Tweets', value=len(df))
    col2.metric('Total Contributors', value=len(df['user_id'].unique()))
    col3.metric('Avg Sentiment Score', value=round(df.loc[:, 'tweet_polarity_score'].mean(), 2))
    
    weekday = df.loc[df['is_weekday'] == 'weekday']
    weekend = df.loc[df['is_weekday'] == 'weekend']
    
    col4.metric('Total Weekday Tweets', value=len(weekday))
    col5.metric('Total Weekend Tweets', value=len(weekend))
    
    st.plotly_chart(tweet_trend_chart(df), use_container_width = True)
    
    row1_col1, row1_col2 = st.columns(2)
    row1_col1.plotly_chart(polarity_pie_chart(df), use_container_width=True)
    row1_col2.plotly_chart(weighted_polarity_line_chart(df[['daily', 'tweet_polarity_score']]), use_container_width=True)
    
    row2_col1, row2_col2 = st.columns(2)
    row2_col1.plotly_chart(plot_hashtag(df['text']), use_container_width=True)
    row2_col2.plotly_chart(pos_neg_chart(df), use_container_width = True)
