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
# youtube_video = "https://www.youtube.com/watch?v=OmKbGOARXao"
# video_id = youtube_video.split("=")[1]
result="""EY Technology Consulting is a part of the EY Consulting practice, leveraging key technologies, and 
committed to solving clients’ most challenging issues and addressing their priorities. Through our 
immense talent, technology tools as well as innovative solutions, we work with our clients to 
transform their business and help them navigate through the next wave of technology trends and 
ambitions."""
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
def summarize(text, per):
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
def punct(result):
    model = PunctuationModel()
    output= model.restore_punctuation(result)
    return output
def translate(output,desired):
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

def summarizeText(language,result,percentage):

    result=beautifyText(result)
    output=summarize(result,percentage)
    try:
        punc_output=punct(output)
    except:
        return
    tran_output=translate(punc_output,language)
    return tran_output
