import re
import datetime
import calendar
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initializing sentiment class
analyzer = SentimentIntensityAnalyzer()

files = [
    './data/raw_data/IndiaSanofi_data.csv',
    './data/raw_data/SanofiBrasil_data.csv',
    './data/raw_data/sanofiDE_data.csv',
    './data/raw_data/SanofiFR_data.csv',
    './data/raw_data/SanofiUS_data.csv'
]

def weekday_weekends(x):
    date = datetime.datetime.strptime(x, '%Y-%m-%d')
    try:
        day_name = calendar.day_name[date.weekday()]
        if day_name == 'Sunday' or day_name == 'Saturday':
            return 'weekend'
        else:
            return 'weekday'
    except Exception as e:
        print(e)
    
def get_year(x):
    try:
        year = x.split('-')[0]
        return year
    except Exception as e:
        pass

def get_daily(x):
    try:
        month = x.split(' ')[0]
        return month
    except Exception as error:
        pass
    
def get_month(x):
    try:
        month = x.split(' ')[0].split('-')[1]
        return month
    except Exception as error:
        pass

# Cleaning the text column
def clean_tweet(text):
    # Removing all usernames
    text = re.sub(r'@[A-Za-z0-9_]+', '', text)
    # Removing all URLS/LINKS
    text = re.sub(r'https?:\/\/\S+', '', text)
    # Removing all NUMBERS AND PERCENTAGES
    text = re.sub(r'[0-9%?]', '', text)
    # OTHER SPECIAL CHARACTERS LIKE #, @ + ARE REMOVED 
    text = re.sub(r'[#$%^&*()-+]', '', text)
    # REMOVE THE WORD RT
    text = re.sub(r'RT[\s]', '', text)
    # REMOVE NEWLINE AND CARIRIAGE CHARACTERS
    text = re.sub(r'[/\r?\n|\r/]', '' ,text)
    # REMOVE EXTRA WHITESPACES
    text = text.strip()
    # returning the clean text data
    return text

# getting the sentiment polarity scores
def get_polarity_score(tweet_text):
    tweet_polarity = analyzer.polarity_scores(tweet_text)
    polarity_score = tweet_polarity['compound']
    return polarity_score

# Adding lable to the polarity scores
def getsentiment(score):
    if score <= -0.05:
        return 'Negative'
    elif score >= 0.05:
        return 'Positive'
    else:
        return 'Neutral'

def main():
    for file in files:
        name = file.split('/')[3]
        print(f'Processing {name} file')

        df = pd.read_csv(file)

        df['daily'] = df['tweet_created_at'].apply(get_daily)
        df['is_weekday'] = df['daily'].apply(weekday_weekends)
        df['year'] = df['tweet_created_at'].apply(get_year)
        df['user_year'] = df['user_created_at'].apply(get_year)
        df['cleaned_tweet'] = df['text'].apply(clean_tweet)
        # creating a new column 'tweet_polarity_score'
        df['tweet_polarity_score'] = df['cleaned_tweet'].apply(get_polarity_score)
        df['polarity_label'] = df['tweet_polarity_score'].apply(getsentiment)

        df.to_csv(f'./data/clean_data/{name.lower()}', index=False)

if __name__ == '__main__':
    main()