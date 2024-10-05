# PROXY'24 HACKATHON - TECH CREED
### AUDIO EDU 🏆 Hackathon Event: PROXY'24

## 📘 Overview
Students often struggle to keep up with lectures due to the fast pace, compounded by language barriers that make it difficult to comprehend concepts, especially for non-native speakers. This leads to challenges in understanding complex material, particularly when foundational concepts are not fully understood. 

## Problem Identified
1. Lecture speed: Fast-paced lectures make it hard for some students to follow.
2. Language barrier: Non-native speakers struggle to comprehend content
3. Limited resources: Lack of accessible, simplified resources in multiple languages.
4. Non-native speakers: Often struggle with understanding and pronouncing subject-specific terminology in a foreign script

## Soluation Terminology
1. Lecture speed: Offer recorded lectures or slower-paced options to allow students to review at their own pace.
2. Language barrier: Provide transliteration and translated resources to help non-native speakers understand terminology and concepts.
3. Limited resources: Create or offer supplementary materials in multiple languages and formats.
4. Non0native speakers: Using transliteration to convert subject-specific terminology into the student's native script, enabling easier pronunciation and understanding.

##  Solution Workflow
![image](https://github.com/user-attachments/assets/9be9ecaa-8d6b-45f3-b2e1-dcd20d54d8bf)

## Tech Stack Used
- Programming Language: Python

- Web Framework: Flask

- Speech-to-Text: SpeechRecognition

- Language Identification: FastText

- Text Embedding: Facebook LLaMA Tokenizer

- Translation/Transliteration: LLaMA Model / ai4bharat
  
##  Setting Up on the local Systsm
### Install Prerequisites:
```Ensure you have Python installed (preferably version 3.7 or higher).```

### Clone the Repository::
```
git clone https://github.com/MUKILAN-2003/PROXY-24-TECH-CREED
cd PROXY-24-TECH_CREED
pip install -r requirement.txt
```

### Fasttext AI Model:
```
!wget https://dl.fbaipublicfiles.com/nllb/lid/lid218e.bin

copy the above file inside the models/supportFile/
```

### Run the Flask Server:
```
python main.py
```

## Impoact and Benefits
1. Enhanced Comprehension: The solution enables users to better understand spoken content by providing accurate text translations or transliterations, thus facilitating learning and communication.
2. Support for Multilingual Environments: The solution is particularly beneficial in diverse settings, such as classrooms or workplaces, where individuals speak different languages.
3. Time-Saving: Automated speech-to-text conversion and language identification save users time compared to manual transcription and translation, improving overall productivity.
4. Immediate Audio Capture : Users can upload or stream audio directly into the application, allowing for on-the-fly processing without delays.

# Reseach and References
- https://ai4bharat.iitm.ac.in/
- https://www.codespeedy.com/extract-audio-from-video-using-python/
- https://www.arxiv-vanity.com/papers/1710.08969/
- https://github.com/meta-llama/llama/blob/main/MODEL_CARD.md
- https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
