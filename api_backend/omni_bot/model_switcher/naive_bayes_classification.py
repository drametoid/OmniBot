import json
import string
import unicodedata
import random

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
import pickle

# Load data from a JSON file
with open('data/agg_data.json') as f:
    data = json.load(f)

prompts = []
categories = []

for observation in data:
    prompt = observation['prompt']
    category = observation['category']

    # Convert prompt to lowercase
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
    prompts.append(' '.join(features))
    categories.append(category)

# Combine prompts and categories into list of tuples
data = list(zip(prompts, categories))

# Shuffle data and split into training and testing sets
random.shuffle(data)
train_data = data[:int(len(data)*0.8)]
test_data = data[int(len(data)*0.8):]

train_prompts, train_categories = zip(*train_data)
test_prompts, test_categories = zip(*test_data)

# Create a pipeline to transform prompts into a feature matrix and train a Naive Bayes model
pipeline = Pipeline([
    ('count_vectorizer', CountVectorizer()),
    ('tfidf_transformer', TfidfTransformer()),
    ('naive_bayes', MultinomialNB())
])
model = pipeline.fit(train_prompts, train_categories)

# Save model to file
with open('model_weights/prompt_classification.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load model from file
# with open('path/to/model/file', 'rb') as f:
#     model = pickle.load(f)

# Make a prediction using the loaded model
# prompt = 'This is a positive prompt'
# predicted_category = model.predict([prompt])[0]
# print(predicted_category)

# Make predictions on test data
predicted_categories = model.predict(test_prompts)

# Calculate accuracy
accuracy = accuracy_score(test_categories, predicted_categories)
print('Accuracy: {:.2f}%'.format(accuracy * 100))