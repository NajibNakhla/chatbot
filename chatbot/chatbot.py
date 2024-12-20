import random
import json
import logging
import pickle
import numpy as np
import os
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

lemmatizer = WordNetLemmatizer()
intents = None  # Define intents globally
words = None  # Define words globally
classes = None  # Define classes globally
model = None  # Define model globally

def load_data():
    global intents, words, classes, model
    intents = json.loads(open('chatbot/intents.json').read())
    words = pickle.load(open('words.pkl','rb'))
    classes = pickle.load(open('classes.pkl','rb'))
    model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    logging.debug(f"Received sentence: {sentence}")
    sentence_words = nltk.word_tokenize(sentence)
    logging.debug(f"Tokenized words: {sentence_words}")
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)  

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1]) })
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Load data when the module is imported
load_data()
