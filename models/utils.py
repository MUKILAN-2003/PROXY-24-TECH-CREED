import fasttext
import os

# libraries for multilanguage translation
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# Language TRanslation
checkpoint = 'facebook/nllb-200-distilled-600M'

# Text Lang Detection
pretrained_lang_model = "models/supportFile/lid218e.bin" # Path of model file
modelTextDetection = fasttext.load_model(pretrained_lang_model)

model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

def dectLang(text):
    predictions = modelTextDetection.predict(text, k=1)
    input_lang = predictions[0][0].replace('__label__', '')
    return input_lang

def text2textTranslation(source,target,text):
    translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang=source, tgt_lang=target, max_length = 400)
    output = translator(text)
    translated_text = output[0]['translation_text']

    return translated_text

# path of the audiofile with filename
def englishaudio_englishtext(path,target):
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
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
                source = dectLang(text)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                whole_text += text2textTranslation(source,target,text)
    
    # return the text for all chunks detected
    return whole_text

# print(dectLang("صباح الخير، الجو جميل اليوم والسماء صافية."))
print(text2textTranslation(source='arb_Arab',target='eng_lat', text="صباح الخير، الجو جميل اليوم والسماء صافية."))
