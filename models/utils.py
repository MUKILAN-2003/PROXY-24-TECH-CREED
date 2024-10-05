# libraries for text to audio 
from gtts import gTTS
import fasttext
import pytube

# libraries for extract a audio from video and merge audio to video
# https://www.codespeedy.com/extract-audio-from-video-using-python/
# pip install ffmpeg moviepy
from moviepy.editor import *
import os

# libraries for audio to english text
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
# pip3 install SpeechRecognition pydub
# https://www.arxiv-vanity.com/papers/1710.08969/

import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# libraries for multilanguage translation
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# libraries for extract transcript from youtube link
from youtube_transcript_api import YouTubeTranscriptApi

# library for transliteration
from ai4bharat.transliteration import XlitEngine

# load a transliteration models
english2vernacular = XlitEngine(src_script_type="roman", beam_width=10, rescore=False)
vernacular2english = XlitEngine(src_script_type="indic", beam_width=10, rescore=False)

# Text Lang Detection
pretrained_lang_model = "models/supportFile/lid218e.bin" # Path of model file
modelTextDetection = fasttext.load_model(pretrained_lang_model)

# Language TRanslation

checkpoint = 'facebook/nllb-200-distilled-600M'
# checkpoint = ‘facebook/nllb-200–1.3B’
# checkpoint = ‘facebook/nllb-200–3.3B’
# checkpoint = ‘facebook/nllb-200-distilled-1.3B’

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

captioner = pipeline("image-to-text",model="Salesforce/blip-image-captioning-base")

common_language = {
    "Bengali": "ben_Beng",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Nepali": "npi_Deva",
    "Sinhala": "sin_Sinh",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab",
    "English": "eng_Latn"
}

def dectLang(text):
    predictions = modelTextDetection.predict(text, k=1)
    input_lang = predictions[0][0].replace('__label__', '')
    return input_lang

def text2textTranslation(source,target,text):
    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target, max_length = 400)
    output = translator(text)
    translated_text = output[0]['translation_text']
    print(translated_text)
    return translated_text

# print(dectLang("صباح الخير، الجو جميل اليوم والسماء صافية."))
# print(text2textTranslation(source='arb_Arab',target='eng_lat', text="صباح الخير، الجو جميل اليوم والسماء صافية."))\

# path - folder path with a file name
def text_audio(translation_text, language,path):
    language_code = {
    "Bengali": "bn",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Urdu": "ur",
    "Tamil": "ta",
    "Telugu": "te",
    "Nepali": "ne",
    "Sinhala": "si",
    "English": "en"
}
    lan = language_code[language]
    myobj = gTTS(text=translation_text, lang=lan, slow=False)
    myobj.save(path)
    return path


# path of the audiofile with filename
def englishaudio_englishtext(path,target):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    path = sys.path[0] + "/static/uploads/audio/{0}".format(path)
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.WavFile(chunk_filename) as source:              # use "test.wav" as the audio source
            audio_listened = r.record(source)                        # extract audio data from the file

        try:
            list_pred = r.recognize(audio_listened,True)                  # generate a list of possible transcriptions
            print("Possible transcriptions:")
            for prediction in list_pred:
                print(" " + prediction["text"] + " (" + str(prediction["confidence"]*100) + "%)")
        
            source = dectLang(text)
        
            text = f"{text.capitalize()}. "
            whole_text += text2textTranslation(source,target,text)
            
            # return the text for all chunks detected
            print(whole_text)
            return whole_text

        except LookupError:                                 # speech is unintelligible
            print("Could not understand audio")


def englishaudio_trans(path,target):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    path = sys.path[0] + "/static/uploads/audio/{0}".format(path)
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.WavFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += englishtovernacular(lang=target,text=text)
    # return the text for all chunks detected
    print(whole_text)
    return whole_text

# transliteration 

language = {
    "Bengali": "bn",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Sinhala": "si",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}