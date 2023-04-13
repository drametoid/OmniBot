import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import pickle
import spacy
import sys, fitz
import io
import speech_recognition as sr
from model_switcher.scraping_functions import display_summary
from model_switcher.lstm_utlis import LSTM_Predictor
from model_switcher.suduko_helper import solve_suduko
import os
script_dir = os.path.dirname(os.path.abspath(__file__))

def preprocess_prompt(prompt):
    prompt = prompt.lower()

    # Remove non-ASCII characters
    prompt = unicodedata.normalize('NFKD', prompt).encode('ascii', 'ignore').decode('utf-8')

    # Tokenize prompt
    tokens = word_tokenize(prompt)

    # Remove stop words and punctuation from tokens
    stop_words = set(stopwords.words('english'))
    punctuations = set(string.punctuation)
    filtered_tokens = [word for word in tokens if word not in stop_words and word not in punctuations]

    # Create bigrams from filtered tokens
    bigrams = list(nltk.bigrams(filtered_tokens))

    # Join bigrams into strings
    bigram_strings = [' '.join(bigram) for bigram in bigrams]

    # Combine filtered tokens and bigram strings
    features = filtered_tokens + bigram_strings

    # Add prompt and category to lists
    return ' '.join(features)

def get_prompt_category(prompt):
    file_path = os.path.join(script_dir, 'model_weights', 'prompt_classification.pkl')
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    predicted_category = model.predict([prompt])[0]
    return predicted_category

def get_suduko_solver(suduko):
    saved_model_path = os.path.join(script_dir,'..' ,'..', '..', 'SudokuSolver', 'SudokuSolver' , 'model', 'sudoku.h5')
    return solve_suduko('img', suduko, saved_model_path=saved_model_path)

def summarize_article(article_link):
    article_summary, length = display_summary(article_link)
    return article_summary

def get_resume_summarized(resume):
    nlp_model_path = os.path.join(script_dir,'..',  '..', '..', 'models', 'nlp_model')
    nlp_model = spacy.load(nlp_model_path)
    doc = fitz.open(stream=resume.read(), filetype='pdf')
    text = ""
    for page in doc:
        text = text + str(page.get_text())
    tx = " ".join(text.split('\n'))

    doc = nlp_model(tx)
    resume_summary = ""
    for ent in doc.ents:
        resume_summary += f'{ent.label_.upper():{30}}- {ent.text}' + "\n"
    return resume_summary

def get_lstm_prompt_prediction(prompt):
    MODEL_PATH = os.path.join(script_dir, '..', '..', 'switcher','LSTM', 'LSTM.pt')
    predictor = LSTM_Predictor(MODEL_PATH)
    predictor.load_model()
    prediction = predictor.get_prediction(prompt)
    if prediction:
        final_pred = prediction[0]
        if final_pred[0] == "resume_summary_data":
            return "resume"
        elif final_pred[0] == "blog_scrapping":
            return "blog"
        elif final_pred[0] == "audio_to_text_data":
            return "audio_to_text"
        elif final_pred[0] == "suduko_data":
            return "suduko"
        elif final_pred[0] == "random_data":
            return "random"
    return None

def convert_audio_to_text(file):
    r = sr.Recognizer()
    file_content = file.read()
    with sr.AudioFile(io.BytesIO(file_content)) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
    return text
