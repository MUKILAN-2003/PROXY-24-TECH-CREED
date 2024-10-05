import fasttext
import os

# Text Lang Detection
pretrained_lang_model = "models/supportFile/lid218e.bin" # Path of model file
modelTextDetection = fasttext.load_model(pretrained_lang_model)

def dectLang(text):
    predictions = modelTextDetection.predict(text, k=1)
    input_lang = predictions[0][0].replace('__label__', '')
    return input_lang

print(dectLang("صباح الخير، الجو جميل اليوم والسماء صافية."))