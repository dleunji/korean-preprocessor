import streamlit as st
import json
import requests
backend = "http://0.0.0.0:8000/preprocess"

def process(url: str, text: str):
  data = {
    'text' : text
  }
  res = requests.post(url, data = json.dumps(data), headers={"Content-Type": "application/json"})
  return res

st.title("Preprocess text")
input = st.text_area("Which text do you want to preprocess?")

if st.button("Preprocess"):
  if input:
    preprocessed = process(backend, input)
    st.write(preprocessed)
  else:
    st.write("Please insert text")

