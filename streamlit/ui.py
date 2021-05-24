import streamlit as st
import json
import requests
backend = "http://0.0.0.0:8000/preprocess"
normalizers = ['emoticon_normalize', 'repeat_normalize', 'only_hangle', 'only_hangle_number','only_text']

def process(url: str, text: str, n1: bool, n2: bool, n3: bool, n4: bool, n5: bool, num_repeats1: int, num_repeats2: int):
  data = {
    'text' : text,
    'emoticon_normalize' : n1, 
    'repeat_normalize' : n2,
    'only_hangle': n3, 
    'only_hangle_number' : n4,
    'only_text' : n5,
    'num_repeats1' : num_repeats1,
    'num_repeats2' : num_repeats2
  }
  res = requests.post(url, data = json.dumps(data), headers={"Content-Type": "application/json"})
  return res

st.title("Korean Preprocessor")
""" ## Normalizers
  1. **Emoticon_normalize** : 반복되는 글자를 줄이고, 자음/모음 이모티콘을 분해합니다.
  2. **Repeat_normalize** : 반복되는 글자를 num_repeats으로 축약합니다.
  3. **Only_hangle** : 한글 글자만 남기고 싶은 경우에 이용합니다.
  4. **Only_hangle_number** : 한글과 숫자만 남기고 싶은 경우에 이용합니다. 한글이 아닌 글자는 빈칸처리합니다.
  5. **Only_text** : 알파벳, 한글, 숫자, 문법기호(!?.,"')만 남기고 싶은 경우에 이용합니다. 해당 글자가 아닌 경우 빈칸처리되며, 연속된 빈칸은 한칸만 남겨집니다.
  ✅ 현재 라이브러리의 문제로 특수문자는 적용되지 않습니다.
"""
st.write("")
with st.sidebar:
  st.write("## Task")
  st.write("📝 원하는 Normarlizer 기능을 고르세요.")
  st.info(
    """반복 글자의 축약 횟수를 의미하는 num_repeats의 기본 값은 2입니다."""
  )
  num_repeats1 = 2
  num_repeats2 = 2
  n1 = st.checkbox(normalizers[0])
  if n1:
    num_repeats1 = st.number_input('num_repeats of Emoticon_normalize', min_value=2,step=1)
  n2 = st.checkbox(normalizers[1])
  if n2:
    num_repeats2 = st.number_input('num_repeats of Repeat_normalize',min_value=2,step=1)
  n3 = st.checkbox(normalizers[2])
  n4 = st.checkbox(normalizers[3])
  n5 = st.checkbox(normalizers[4])

input = st.text_area("전처리할 텍스트를 입력해주세요.")

if st.button("Preprocess"):
  if n1 or n2 or n3 or n4 or n5:
    if input:
      preprocessed = process(backend,input,n1,n2,n3,n4,n5,num_repeats1,num_repeats2)
      text = preprocessed.content.decode('utf-8')
      st.write(text)
    else:
      st.warning("텍스트가 입력되지 않았습니다.")
  else:
    st.warning("Normalizer가 선택되지 않았습니다.")


