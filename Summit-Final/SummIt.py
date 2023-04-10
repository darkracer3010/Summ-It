from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from deepmultilingualpunctuation import PunctuationModel
from googletrans import Translator
from languages import languages1,languages
import googleapiclient.discovery
import nltk
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer

languages=None
desired=None


def text_extract(video_id):
    lang_trans=YouTubeTranscriptApi.list_transcripts(video_id)
    lang=[]
    for i in lang_trans:
        lang=i.translation_languages
    languages={}
    for i in lang:
        languages[i['language']]=i['language_code']

    languages1.update(languages)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    for i in transcript_list:
        lang=i.language
        break
    split_lang=lang.split(" ")
    lang1=split_lang[0]
    if(len(split_lang)>1 and split_lang[1]=="(auto-generated)"):
        transcript = transcript_list.find_transcript([languages1[lang1]])
    else:
        try:
            transcript = transcript_list.find_transcript([languages1[lang]])
        except:
            transcript=transcript_list.find_transcript([languages1[lang1]])
    return transcript,languages1
def OriginalText(transcript):
    result = ""
    if(type(transcript)==list):
        for i in transcript:
            result += ' ' + i['text'].replace("\n"," ")
    else:
        for i in transcript.fetch():
            result += ' ' + i['text'].replace("\n"," ")
    return (result)
def beautifyText(result):
    result=result.lower()
    result=re.sub("what's","what is ",result)
    result=re.sub("it's","it is ",result)
    result=re.sub("\'ve"," have ",result)
    result=re.sub("i'm","i am ",result)
    result=re.sub("\'re"," are ",result)
    result=re.sub("won't"," will not ",result)
    result=re.sub("n't"," not ",result)
    result=re.sub("\'d"," would ",result)
    result=re.sub("\'s","s",result)
    result=re.sub("\'ll"," will ",result)
    result=re.sub("can't"," cannot ",result)
    result=result.replace('\n',' ')
    return result
def summarizeData(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary
def punctuate(result):
    model = PunctuationModel()
    output= model.restore_punctuation(result)
    return output
def translate(output):
    translator = Translator()
    o=output.split(".")
    output_text=""
    for i in range(len(output)):
        try:
            output_text+=(translator.translate(o[i],dest=languages[desired]).text).capitalize()
            output_text+="."
        except:
            pass
    return output_text[:-1]

def recommendVideo(id):
    api_key = "AIzaSyBWYZ-6MebgvdLWEbhNN_x_u5FbhREj8VM"
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
    request = youtube.commentThreads().list(part="snippet", videoId=id, textFormat="plainText")
    try:
        response = request.execute()
    except:
        return ""
    comments = []
    for item in response["items"]:
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)

    nltk.download("vader_lexicon")
    sid = SentimentIntensityAnalyzer()
    sentiments = []
    for comment in comments:
        sentiment = sid.polarity_scores(comment)
        sentiments.append(sentiment)
    overall_sentiment = sum(sentiment["compound"] for sentiment in sentiments) / len(sentiments)
    verdict=""
    if overall_sentiment > 0:
       verdict="This video is good based on the comments."
    else:
        verdict="This video is not good based on the comments."
    return verdict

def summarizeDataComplete(url,language,percent):
    global languages,desired
    desired=language
    video_id=url.split("=")[1]
    try:
        transcript,languages=text_extract(video_id)
    except:
        return "captions"
    result=OriginalText(transcript)
    result=beautifyText(result)
    output=summarizeData(result,float(percent))
    try:
        punc_output=punctuate(output)
    except:
        return "ratio"
    tran_output=translate(punc_output)
    return tran_output
