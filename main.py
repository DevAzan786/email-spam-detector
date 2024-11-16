import streamlit as st
import pickle
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

try:
  vectorize = pickle.load(open('vectorize.pkl','rb'))
  model = pickle.load(open('MNB.pkl','rb'))

except FileNotFoundError as e:
    st.error(f'FIle not found {e}')
    st.stop()


def preprocess(text):
    try:
        text = text.lower()
        text = nltk.word_tokenize(text)
        lst = []
        for i in text:
            if i.isalnum():
                lst.append(i)

        text = lst[:]
        lst.clear()

        for i in text:
            if i not in stopwords.words('english') and i not in string.punctuation:
                lst.append(i)

        text = lst[:]
        lst.clear()
        stemmer = PorterStemmer()
        for i in text:
            lst.append(stemmer.stem(i))

        return ' '.join(lst)
    except Exception as e:
        st.error("An error occured during text processing")
        return ''

st.title('Email Spam Detector')
input_text = st.text_area('Enter the message')

if st.button('Check'):
    if not input_text.strip():
        st.warning('Enter a message to check')
    else:
        processed_email = preprocess(input_text)
        vectors = vectorize.transform([processed_email])
        predicted = model.predict(vectors)
        if(predicted==1):
                 st.header('Spam')
        else:
                 st.header('Not spam')