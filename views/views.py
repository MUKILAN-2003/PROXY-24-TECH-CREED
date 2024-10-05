from flask import Flask, render_template, request, redirect, url_for, flash

from app import *
from models.utils import *

import sys

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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/text', methods=["POST", "GET"])
def text():
    if request.method == "POST":
        lag = request.form.get("lag")
        text = request.form.get("text") 
        sourceLang = dectLang(text)
        translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
        return render_template('text.html', translatedText=translatedText,common_language = common_language)
    return render_template('text.html',common_language = common_language)

# input - audio file and language
# output - translated audio filepath
@app.route('/audio', methods=["POST", "GET"])
def audio():
    if request.method == "POST":
        file = request.files['file']
        language = request.form['lang']
        if file.filename == '' :
            flash('No image selected for uploading')
            return redirect(request.url)   

        else:
            audiopath = os.path.join(app.config['UPLOAD_FOLDER'], 'audio',file.filename)
            translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
            translatedaudiopath = os.path.join(translatedaudiofolder, file.filename)
            file.save(audiopath)
            translated_text = englishaudio_englishtext(file.filename,language)
            text_audio(translated_text,languageCode2Lang[language],translatedaudiopath)

            return render_template('audio.html',common_language = common_language,result=True,  translated_text=translated_text,translatedaudiopath=file.filename)
        

    return render_template('audio.html',common_language = common_language,result=False,translated_text='',translatedaudiopath='')