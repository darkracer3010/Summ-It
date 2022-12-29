from youtube_transcript_api import YouTubeTranscriptApi
from IPython.display import YouTubeVideo
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from deepmultilingualpunctuation import PunctuationModel
from googletrans import Translator
youtube_video = "https://www.youtube.com/watch?v=OmKbGOARXao"
video_id = youtube_video.split("=")[1]
desired=input("Enter the language:").capitalize()
# YouTubeVideo(video_id)-embed YT link
def text_extract(video_id):
    lang_trans=YouTubeTranscriptApi.list_transcripts(video_id)
    lang=[]
    for i in lang_trans:
        lang=i.translation_languages
    languages={}
    for i in lang:
        languages[i['language']]=i['language_code']
    languages1={
'Afrikans (South Africa)':'af-ZA',
'Albanian (Albania)':'sq-AL',
'Amharic (Ethiopia)':'am-ET',
'Arabic (Algeria)':'ar-DZ',
'Arabic (Bahrain)':'ar-BH',
'Arabic (Egypt)':'ar-EG',
'Arabic (Iraq)':'ar-IQ',
'Arabic (Israel)':'ar-IL',
'Arabic (Jordan)':'ar-JO',
'Arabic (Kuwait)':'ar-KW',
'Arabic (Lebanon)':'ar-LB',
'Arabic (Mauritania)':'ar-MR',
'Arabic (Morocco)':'ar-MA',
'Arabic (Oman)':'ar-OM',
'Arabic (Qatar)':'ar-QA',
'Arabic (Saudi Arabia)':'ar-SA',
'Arabic (State of Palestine)':'ar-PS',
'Arabic (Tunisia)':'ar-TN',
'Arabic (United Arab Emirates)':'ar-AE',
'Arabic (Yemen)':'ar-YE',
'Armenian (Armenia)':'hy-AM',
'Azerbaijani (Azerbaijan)':'az-AZ',
'Basque (Spain)':'eu-ES',
'Bengali (Bangladesh)':'bn-BD',
'Bengali (India)':'bn-IN',
'Bosnian (Bosnia and Herzegovina)':'bs-BA',
'Bulgarian (Bulgaria)':'bg-BG',
'Burmese (Myanmar)':'my-MM',
'Catalan (Spain)':'ca-ES',
'Chinese, Cantonese (Traditional Hong Kong)':'yue-Hant-HK',
'Chinese, Mandarin (Simplified, China)':'zh (cmn-Hans-CN)',
'Chinese, Mandarin (Traditional, Taiwan)':'zh-TW (cmn-Hant-TW)',
'Croatian (Croatia)':'hr-HR',
'Czech (Czech Republic)':'cs-CZ',
'Danish (Denmark)':'da-DK',
'Dutch (Belgium)':'nl-BE',
'Dutch (Netherlands)':'nl-NL',
'English (Australia)':'en-AU',
'English (Canada)':'en-CA',
'English (Ghana)':'en-GH',
'English (Hong Kong)':'en-HK',
'English (India)':'en-IN',
'English (Ireland)':'en-IE',
'English (Kenya)':'en-KE',
'English (New Zealand)':'en-NZ',
'English (Nigeria)':'en-NG',
'English (Pakistan)':'en-PK',
'English (Philippines)':'en-PH',
'English (Singapore)':'en-SG',
'English (South Africa)':'en-ZA',
'English (Tanzania)':'en-TZ',
'English (United Kingdom)':'en-GB',
'English (United States)':'en-US',
'Estonian (Estonia)':'et-EE',
'Filipino (Philippines)':'fil-PH',
'Finnish (Finland)':'fi-FI',
'French (Belgium)':'fr-BE',
'French (Canada)':'fr-CA',
'French (France)':'fr-FR',
'French (Switzerland)':'fr-CH',
'Galician (Spain)':'gl-ES',
'Georgian (Georgia)':'ka-GE',
'German (Austria)':'de-AT',
'German (Germany)':'de-DE',
'German (Switzerland)':'de-CH',
'Greek (Greece)':'el-GR',
'Gujarati (India)':'gu-IN',
'Hebrew (Israel)':'iw-IL',
'Hindi (India)':'hi-IN',
'Hungarian (Hungary)':'hu-HU',
'Icelandic (Iceland)':'is-IS',
'Indonesian (Indonesia)':'id-ID',
'Italian (Italy)':'it-IT',
'Italian (Switzerland)':'it-CH',
'Japanese (Japan)':'ja-JP',
'Javanese (Indonesia)':'jv-ID',
'Kannada (India)':'kn-IN',
'Kazakh (Kazakhstan)':'kk-KZ',
'Khmer (Cambodia)':'km-KH',
'Korean (South Korea)':'ko-KR',
'Lao (Laos)':'lo-LA',
'Latvian (Latvia)':'lv-LV',
'Lithuanian (Lithuania)':'lt-LT',
'Macedonian (North Macedonia)':'mk-MK',
'Malay (Malaysia)':'ms-MY',
'Malayalam (India)':'ml-IN',
'Marathi (India)':'mr-IN',
'Mongolian (Mongolia)':'mn-MN',
'Nepali (Nepal)':'ne-NP',
'Norwegian Bokm책l (Norway)':'no-NO',
'Persian (Iran)':'fa-IR',
'Polish (Poland)':'pl-PL',
'Portuguese (Brazil)':'pt-BR',
'Portuguese (Portugal)':'pt-PT',
'Punjabi (Gurmukhi India)':'pa-Guru-IN',
'Romanian (Romania)':'ro-RO',
'Russian (Russia)':'ru-RU',
'Kinyarwanda (Rwanda)':'rw-RW',
'Serbian (Serbia)':'sr-RS',
'Sinhala (Sri Lanka)':'si-LK',
'Slovak (Slovakia)':'sk-SK',
'Slovenian (Slovenia)':'sl-SI',
'Swati (South Africa)':'ss-latn-za',
'Southern Sotho (South Africa)':'st-ZA',
'Spanish (Argentina)':'es-AR',
'Spanish (Bolivia)':'es-BO',
'Spanish (Chile)':'es-CL',
'Spanish (Colombia)':'es-CO',
'Spanish (Costa Rica)':'es-CR',
'Spanish (Dominican Republic)':'es-DO',
'Spanish (Ecuador)':'es-EC',
'Spanish (El Salvador)':'es-SV',
'Spanish (Guatemala)':'es-GT',
'Spanish (Honduras)':'es-HN',
'Spanish (Mexico)':'es-MX',
'Spanish (Nicaragua)':'es-NI',
'Spanish (Panama)':'es-PA',
'Spanish (Paraguay)':'es-PY',
'Spanish (Peru)':'es-PE',
'Spanish (Puerto Rico)':'es-PR',
'Spanish (Spain)':'es-ES',
'Spanish (United States)':'es-US',
'Spanish (Uruguay)':'es-UY',
'Spanish (Venezuela)':'es-VE',
'Sundanese (Indonesia)':'su-ID',
'Swahili (Kenya)':'sw-KE',
'Swahili (Tanzania)':'sw-TZ',
'Swedish (Sweden)':'sv-SE',
'Tamil (India)':'ta-IN',
'Tamil (Malaysia)':'ta-MY',
'Tamil (Singapore)':'ta-SG',
'Tamil (Sri Lanka)':'ta-LK',
'Telugu (India)':'te-IN',
'Thai (Thailand)':'th-TH',
'Setswana (South Africa)':'tn-latn-za',
'Turkish (Turkey)':'tr-TR',
'Tsonga (South Africa)':'ts-ZA',
'Ukrainian (Ukraine)':'uk-UA',
'Urdu (India)':'ur-IN',
'Urdu (Pakistan)':'ur-PK',
'Uzbek (Uzbekistan)':'uz-UZ',
'Venda (South Africa)':'ve-ZA',
'Vietnamese (Vietnam)':'vi-VN',
'isiXhosa (South Africa)':'xh-ZA',
'Zulu (South Africa)':'zu-ZA'}
    languages1.update(languages)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    for i in transcript_list:
        if(i.is_generated):
            lang=i.language
        else:
            lang=i.language
        break
    try:
        transcript=transcript_list.find_manually_created_transcript([languages1[lang]])
    except:
        split_lang=lang.split(" ")
        lang1=split_lang[0]
        if(split_lang[1]=="(auto-generated)"):
            transcript = transcript_list.find_transcript([languages1[lang1]])
        else:
            print("Sorry Subtitles not Found")
    return transcript,languages1
def OriginalText(transcript):
    result = ""
    for i in transcript.fetch():
        result += ' ' + i['text']
    return(result)
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
def punctuation(result):
    model = PunctuationModel()
    output= model.restore_punctuation(result)
    return output
def translate(output):
    translator = Translator()
    o=output.split(".")
    output_text=""
    for i in range(len(output)):
        try:
            output_text+=(translator.translate(o[i],dest=languages[desired]).text)
        except:
            pass
    return output_text
transcript,languages=text_extract(video_id)
result=OriginalText(transcript)
result=beautifyText(result)
percent=float(input("Enter the percent to be deducted:"))
output=summarize(result,percent)
punc_output=punctuation(output)
tran_output=translate(punc_output)
