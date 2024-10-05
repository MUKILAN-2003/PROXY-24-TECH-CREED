from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)
import secrets
import bcrypt

from app import *

from models.utils import *
from shutil import copyfile

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

@app.route('/test')
def test():
    return render_template('imagetotextin.html')

@app.route('/')
def home():
    session["email"] = 'PROXY_TECHCREED'
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/text', methods=["POST", "GET"])
def text():
    if "email" in session:
        if request.method == "POST":
            lag = request.form.get("lag")
            text = request.form.get("text") 
            sourceLang = dectLang(text)
            translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
            return render_template('text.html', translatedText=translatedText,common_language = common_language)
        return render_template('text.html',common_language = common_language)

    else:
        return redirect('/login')

languageCode2Lang = {
  "ben_Beng": "Bengali",
  "guj_Gujr": "Gujarati",
  "hin_Deva": "Hindi",
  "kan_Knda": "Kannada",
  "mal_Mlym": "Malayalam",
  "mar_Deva": "Marathi",
  "npi_Deva": "Nepali",
  "sin_Sinh": "Sinhala",
  "tam_Taml": "Tamil",
  "tel_Telu": "Telugu",
  "urd_Arab": "Urdu",
  "eng_Latn": "English"
}

# input - video file and language
# output - translated audio filepath
@app.route('/video', methods=["POST", "GET"])
def video():
    if "email" in session:
        
        if request.method == "POST":
            file = request.files['file']
            language = request.form['lang']

            if file.filename == '' :
                flash('No image selected for uploading')
                return redirect(request.url)   
    
            else:
                audiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                videofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'video')
                videopath = os.path.join(videofolder, file.filename)
                translatedaudiopath = os.path.join(translatedaudiofolder, file.filename)
                combinedvideopath = os.path.join(app.config['UPLOAD_FOLDER'], 'combinedvideo',file.filename)
                file.save(videopath)
                audiopath = extract_video_audio(videopath,file.filename,audiofolder)
                print(audiopath.split('/')[-1])
                translated_text = englishaudio_englishtext(audiopath.split('/')[-1],language)
                text_audio(translated_text,languageCode2Lang[language],translatedaudiopath)
                combine_audio_video(videopath,translatedaudiopath,combinedvideopath)

                return render_template('video.html', result=True, translated_text=translated_text, audipPath=audiopath.split('/')[-1], videoPath=file.filename, common_language = common_language)

        return render_template('video.html', result=False, translated_text='', videoPath='', audipPath = '', common_language = common_language)

    else:
        return redirect('/login')


# input - audio file and language
# output - translated audio filepath
@app.route('/audio', methods=["POST", "GET"])
def audio():
    if "email" in session:
        
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

    else:
        return redirect('/login')
    

# input - url and language
# output - translated video filepath
@app.route('/youtubevideo', methods=["POST", "GET"])
def youtubevideo():
    if "email" in session:
        
        if request.method == "POST":
            url = ""
            language = ""
            if url == '' :
                flash('No url is selected for translating')
                return redirect(request.url)   
    
            else:
                videofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'video')
                filename = download_youtube_video(url,videofolder)
                audiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                videopath = os.path.join(videofolder, filename)
                translatedaudiopath = os.path.join(translatedaudiofolder, filename)
                combinedvideopath = os.path.join(app.config['UPLOAD_FOLDER'], 'combinedvideo', filename)
                audiopath = extract_video_audio(videopath,filename,audiofolder)
                translated_text = englishaudio_englishtext(audiopath,language)
                text_audio(translated_text,languageCode2Lang[language],translatedaudiopath)
                combine_audio_video(videopath,translatedaudiopath,combinedvideopath)

                return combinedvideopath

        return render_template('video.html')

    else:
        return redirect('/login')
    

transliterationlanguage = {
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

transliterationcodetolanguage = {
    "bn": "Bengali",
    "gu": "Gujarati",
    "hi": "Hindi",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "ne": "Nepali",
    "si": "Sinhala",
    "ta": "Tamil",
    "te": "Telugu",
    "ur": "Urdu",
}

@app.route('/texttran', methods=["POST", "GET"])
def texttran():
    if "email" in session:
        if request.method == "POST":
            lag = request.form.get("lag")
            text = request.form.get("text") 
            translatedText = englishtovernacular(lang=lag, text=text)
            return render_template('texttran.html', translatedText=translatedText,common_language = transliterationlanguage)
        return render_template('texttran.html',common_language = transliterationlanguage)

    else:
        return redirect('/login')


# input - video file and language
# output - translated audio filepath
@app.route('/videotran', methods=["POST", "GET"])
def videotran():
    if "email" in session:
        
        if request.method == "POST":
            file = request.files['file']
            language = request.form['lang']

            if file.filename == '' :
                flash('No image selected for uploading')
                return redirect(request.url)   
    
            else:
                audiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                videofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'video')
                videopath = os.path.join(videofolder, file.filename)
                translatedaudiopath = os.path.join(translatedaudiofolder, file.filename)
                combinedvideopath = os.path.join(app.config['UPLOAD_FOLDER'], 'combinedvideo',file.filename)
                file.save(videopath)
                audiopath = extract_video_audio(videopath,file.filename,audiofolder)
                print(audiopath.split('/')[-1])
                translated_text = englishaudio_trans(audiopath.split('/')[-1],language)
                text_audio(translated_text,transliterationcodetolanguage[language],translatedaudiopath)
                combine_audio_video(videopath,translatedaudiopath,combinedvideopath)

                return render_template('videotran.html', result=True, translated_text=translated_text, audipPath=audiopath.split('\\')[-1], videoPath=file.filename, common_language = transliterationlanguage)

        return render_template('videotran.html', result=False, translated_text='', videoPath='', audipPath = '', common_language = transliterationlanguage)

    else:
        return redirect('/login')
    
@app.route('/audiotran', methods=["POST", "GET"])
def audiotran():
    if "email" in session:
        
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
                translated_text = englishaudio_trans(file.filename,language)
                text_audio(translated_text,transliterationcodetolanguage[language],translatedaudiopath)

                return render_template('audiotran.html',common_language = transliterationlanguage,result=True,  translated_text=translated_text,translatedaudiopath=file.filename)
            

        return render_template('audiotran.html',common_language = transliterationlanguage,result=False,translated_text='',translatedaudiopath='')

    else:
        return redirect('/login')