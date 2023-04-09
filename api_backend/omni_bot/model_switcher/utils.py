import unicodedata
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import pickle

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
    with open('/Users/raghukapur/private-projects/final_project_733/OmniBot/api_backend/omni_bot/model_switcher/model_weights/prompt_classification.pkl', 'rb') as f:
        model = pickle.load(f)
    predicted_category = model.predict([prompt])[0]
    return predicted_category