"""
Daniella Misyura
Sentiment Analysis
November 14, 2023
"""
# This is the main program for sentiment_analysis. It takes user input for a tab-separated file of keywords and values,
# ...a comma-separated file for tweets, and a text file to write a sentiment analysis report in.

from sentiment_analysis import read_tweets, make_report, write_report, read_keywords  # Imports sentiment_analysis
import traceback  # Importing the traceback module helps with correctly raising exceptions as a Traceback


def main():
    try:
        keywords_file = input("Enter the path to the keywords file (.tsv): ")  # Takes keyword file input
        keywords = read_keywords(keywords_file)  # Sends keywords file to sentiment_analysis read_keywords()
        if not keywords_file.endswith('.tsv'):
            raise ValueError("Must have tsv file extension!")
        tweet_file = input("Enter the path to the tweet file (.csv): ")  # Takes tweet file input
        tweet_data = read_tweets(tweet_file)  # Sends tweet file to sentiment_analysis read_tweets()
        if not tweet_file.endswith('.csv'):
            raise ValueError("Must have csv file extension!")
        output_file = input("Enter the path for the output report file (.txt): ")  # Takes text file for report input
        report = make_report(tweet_data, keywords)  # Creates a report using sentiment_analysis make_report()
        if not output_file.endswith('.txt'):
            raise ValueError("Must have txt file extension!")

        write_report(report, output_file)
        print(f"Report written to {output_file}")  # If all files are valid, the report will be written to the file
    except Exception as e:
        traceback.print_exc()  # Raises exception as traceback
        print(f"{e}")  # Prints whatever the exception may be


main()  # Calls main function so that the program may run
