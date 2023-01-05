import googleapiclient.discovery
import nltk
import re

# Replace YOUR_API_KEY with your actual API key
api_key = "AIzaSyCpSapkKTdQ-WtfW-Di6AlEN_uMzRGLd_w"

# Set the ID of the video for which you want to retrieve comments
video_id = "YbJOTdZBX1g"

# Use the YouTube API to retrieve the comments for the video
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText")
response = request.execute()

# Extract the comments from the API response
comments = []
for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    comments.append(comment)

# Use NLTK to calculate the sentiment of each comment
nltk.download("vader_lexicon")
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
sentiments = []
for comment in comments:
    sentiment = sid.polarity_scores(comment)
    sentiments.append(sentiment)

# Calculate the overall sentiment of the comments
overall_sentiment = sum(sentiment["compound"] for sentiment in sentiments) / len(sentiments)

# Determine whether the video is "good" based on the overall sentiment of the comments
if overall_sentiment > 0:
    print("This video is good based on the comments.")
else:
    print("This video is not good based on the comments.")
