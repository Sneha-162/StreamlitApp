import streamlit as st
import pandas as pd
from transformers import pipeline
from torch import Tensor

import time 

st.title("working with cache")

@st.cache_data
def read_data():
    df = pd.read_csv("autism_screening.csv")
    return df.head()

start = time.time()
df = read_data()
st.write(time.time()-start)
st.button("Refresh")

def update_session_state():
    if 'counter' not in st.session_state:
        st.session_state.counter = 0
    st.write("counter:", st.session_state.counter)
    st.session_state.counter += 1
update_session_state()

def load_model():
    model = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

    st.success("loaded NLP in function")
    return model

model = load_model()
st.success("Got the model")
