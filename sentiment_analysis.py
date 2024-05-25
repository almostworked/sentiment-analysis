"""
Daniella Misyura
Sentiment Analysis
November 14, 2023
"""
#  This is the Sentiment Analysis program. All the functions used to determine the overall sentiment report of a set...
# ...of tweets, based on a set of keywords & scores, are defined here. A report is generated and then written with...
# ...all the statistics, in the text file received from the input.


def read_keywords(file_path):  # Function that reads the keywords file
    keywords = {}  # Sets keywords variable as an empty dictionary
    try:
        with open(file_path, 'r') as keywords_file:  # Opens file in read mode
            for line in keywords_file:
                term, sentiment = line.strip().split('\t')  # Separates keywords & value using tab into a list
                keywords[term.lower()] = int(sentiment)  # The lower-case keyword is a key, the sentiment is the value
    except FileNotFoundError:
        keywords = {}  # If something is wrong with the file, keywords remains an empty dictionary
    finally:
        return keywords  # Always returns keywords dictionary


def clean_tweet_text(text):  # Function that cleans the tweet text
    cleaned_text = ''.join(char.lower() if char.isalpha() or char.isspace() else '' for char in text)
    return cleaned_text  # Tweet text is set to lowercase, and checked for symbols/non-alphabetical characters


def calc_sentiment(tweet, keywords):  # Function that calculates the sentiment of a tweet
    cleaned_text = clean_tweet_text(tweet)  # Ensures tweet is cleaned
    sentiment_score = 0  # Sets sentiment score variable
    for word in cleaned_text.split():  # Tweet is split into a list, loop goes through each word
        word = word.lower()
        if word in keywords:
            sentiment_score += keywords[word]  # If the word matches a keyword in the keywords file, the sentiment...
    return sentiment_score                     # ... score gets updated with the keyword's associated value.


def classify(score):  # Functions that classifies whether the sentiment is positive, negative or neutral
    if score > 0:  # Positive scores are positive
        return 'positive'
    elif score < 0:  # Negative scores are negative
        return 'negative'
    else:
        return 'neutral'  # If a score is exactly 0, it is neutral


def convert_field(value, data_type):  # This is an extra function I made to deal with values that are 'NULL'
    if value.upper() == 'NULL':
        return 'NULL'  # It ensures that the string 'NULL' is returned if a value is NULL (specifically for integers)
    else:
        return data_type(value)


def read_tweets(file_path):  # Functions to read tweets and return a dictionary of all the information
    tweet_data = []  # Tweet data is an empty list made to contain each tweet dictionary
    try:
        with open(file_path, 'r') as file:
            for line in file:  # For loop for each line in the tweet file
                fields = line.strip().split(',')  # Splits each comma-separated part of the line into a list
                fields[1] = clean_tweet_text(fields[1])  # Ensures actual tweet text is clean
                tweet = {  # Populates tweet dictionary by indexing each part of each line
                    'date': str(fields[0]),
                    'text': str(fields[1]),
                    'user': str(fields[2]),
                    'retweet': convert_field(fields[3], int),  # convert_field() is used because 'NULL' cannot be...
                    'favorite': convert_field(fields[4], int), # ...converted into an integer.
                    'lang': str(fields[5]),
                    'country': str(fields[6]),
                    'state': str(fields[7]),
                    'city': str(fields[8]),
                    'lat': convert_field(fields[9], float),
                    'lon': convert_field(fields[10], float)
                    }
                tweet_data.append(tweet)  # Tweet data list gets updated with dictionaries for each tweet
    except FileNotFoundError:
        tweet_data = []

    finally:
        return tweet_data  # Whether tweet data has any data, the list is returned


def make_report(tweet_data, keywords):  # Function to make the final report that is to be written
    total_tweets = len(tweet_data)  # Total number of tweets
    overall_sentiment_score = 0  # Setting variables that we are going to use soon
    total_positive = 0
    total_negative = 0
    total_neutral = 0
    favourited_tweets = []  # Setting empty lists to contain favourite & retweeted tweets
    retweeted_tweets = []
    country_sentiments = {}  # Setting empty dictionary for country sentiments, which is a more complex value

    for tweet in tweet_data:  # For loop for every tweet in the list of tweet data
        sentiment_score = calc_sentiment(tweet['text'], keywords)  # Calc sentiment function used for tweet text
        sentiment = classify(sentiment_score)  # Classify function used to determine what sentiment the score is
        tweet['sentiment_score'] = sentiment_score  # Adding sentiment score and sentiment as keys with their...
        tweet['sentiment'] = sentiment              # ...respective values.
        overall_sentiment_score += sentiment_score
        if sentiment == 'positive':
            total_positive += 1
        elif sentiment == 'negative':
            total_negative += 1
        else:
            total_neutral += 1  # Determines total amount of positive, negative and neutral tweets

        if tweet.get('favorite', 0) > 0:  # Amount of favourite tweets gets updated if a tweet has more than one...
            favourited_tweets.append(tweet)  # ...like, and same is done for the amount of retweeted tweets.
        if tweet.get('retweet', 0) > 0:
            retweeted_tweets.append(tweet)

    for tweet in tweet_data:  # Making another loop to make indenting less troubling
        country = tweet.get('country')
        if country:
            score = calc_sentiment(tweet['text'], keywords)
            sentiment = classify(score)  # Retrieves sentiment for a tweet to be added in country sentiments
            if country not in country_sentiments:  # Loops through each unique country
                country_sentiments[country] = {'scores': [score], 'count': 1, 'sentiments': [sentiment]}
            else:  # If the country is now in the list, updates each value for the specific country for sentiment
                country_sentiments[country]['scores'].append(score)
                country_sentiments[country]['count'] += 1
                country_sentiments[country]['sentiments'].append(sentiment)

    average_country_sentiments = {}  # Creates dictionary for average country sentiments
    for country, sentiment_data in country_sentiments.items():
        scores = sentiment_data['scores']
        count = sentiment_data['count']
        average_sentiment = sum(scores) / count if count > 0 else 0  # Avoids zero division error
        average_country_sentiments[country] = {'average_sentiment': average_sentiment, 'sentiments': sentiment_data['sentiments']}
        # Average country sentiments dictionary becomes populated with the average sentiments for each country
    # The countries now get sorted based on highest sentiment, and the top countries get put into a list unless...
    # ... their value happens to be NULL. The list ensures that only the top five countries are inside, and is then...
    # ... concatenated into a single string.
    sorted_countries = sorted(average_country_sentiments.items(), key=lambda x: x[1]['average_sentiment'], reverse=True)
    top_countries = [country for country, _ in sorted_countries if country != 'NULL'][:5]
    top_countries_string = ', '.join(top_countries)
    # The average sentiments for total favourited/retweeted tweets gets calculate, by summing the score of each...
    #  ...liked/retweeted tweet and diving by the total amount of liked/retweeted tweets, so long as that number is > 0.
    average_sentiment_favourited = (sum(tweet['sentiment_score'] for tweet in favourited_tweets) / len(favourited_tweets) if len(favourited_tweets) > 0 else 0)
    average_sentiment_favourited = round(average_sentiment_favourited, 2)
    average_sentiment_retweeted = (sum(tweet['sentiment_score'] for tweet in retweeted_tweets) / len(retweeted_tweets) if len(retweeted_tweets) > 0 else 0)
    average_sentiment_retweeted = round(average_sentiment_retweeted, 2)
    #  The overall sentiment average is calculated by taking the overall score and dividing by total tweets
    overall_average_sentiment = overall_sentiment_score / total_tweets if total_tweets > 0 else 0

    report = {  # Report dictionary containing all the keys and data
        'avg_sentiment': round(overall_average_sentiment, 2),
        'num_tweets': total_tweets,
        'num_positive': total_positive,
        'num_negative': total_negative,
        'num_neutral': total_neutral,
        'num_favorite': len(favourited_tweets),
        'avg_favorite': average_sentiment_favourited,
        'num_retweet': len(retweeted_tweets),
        'avg_retweet': average_sentiment_retweeted,
        'top_five': top_countries_string
    }
    return report


def write_report(report, output_file):  # Function that writes the report to the output (text) file
    with open(output_file, 'w') as file:  # Opens file in write mode
        file.write("\nSentiment Analysis:\n")
        for key, value in report.items():  # For loop for each key & value in report dictionary
            if key == 'top_five':  # Special case for top five countries key
                top_five_countries = value.split(', ')[:5]
                file.write(f"{key.capitalize()}: {', '.join(top_five_countries)}")  # Ensuring format is 100% correct
            else:
                file.write(f"{key.capitalize()}: {value}\n")  # Writes key and value for each part of the dictionary
