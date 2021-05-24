from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
from starlette.responses import Response
from soynlp.normalizer import *
import sys
import soynlp

class Input(BaseModel):
  text: str
  emoticon_normalize: Optional[bool] = False
  repeat_normalize: Optional[bool] = False
  only_hangle: Optional[bool] = False
  only_hangle_number: Optional[bool] = False
  only_text: Optional[bool] = False
  num_repeats1: Optional[int] = Query(2)
  num_repeats2: Optional[int] = Query(2)

app = FastAPI(
  title = "Korean Preprocessor",
  description = "Please enter text to preprocess",
  version = "1.0.0"
)

@app.post("/preprocess")
def get_response(input: Input):
  preprocessed = input.text
  if input.emoticon_normalize:
    preprocessed = emoticon_normalize(preprocessed, num_repeats = input.num_repeats1)
  if input.repeat_normalize:
    preprocessed = repeat_normalize(preprocessed, num_repeats = input.num_repeats2)
  if input.only_hangle:
    preprocessed = only_hangle(preprocessed)
  if input.only_hangle_number:
    preprocessed = only_hangle_number(preprocessed)
  if input.only_text:
    preprocessed = only_text(preprocessed)
  return Response(preprocessed, media_type="text/plain")
