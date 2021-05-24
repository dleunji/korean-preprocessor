from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from starlette.responses import Response
from soynlp.normalizer import *
import sys
import soynlp

class Input(BaseModel):
  text: str
  n1: Optional[bool] = False
  n2: Optional[bool] = False
  n3: Optional[bool] = False
  n4: Optional[bool] = False
  n5: Optional[bool] = False
  num_repeats1: Optional[int] = None
  num_repeats2: Optional[int] = None

app = FastAPI(
  title = "Korean Preprocessor",
  description = "Please enter text to preprocess",
  version = "1.0.0"
)

@app.post("/preprocess")
def get_response(input: Input):
  preprocessed = input.text
  if input.n1:
    preprocessed = emoticon_normalize(preprocessed, num_repeats = input.num_repeats1)
  if input.n2:
    preprocessed = repeat_normalize(preprocessed, num_repeats = input.num_repeats2)
  if input.n3:
    preprocessed = only_hangle(preprocessed)
  if input.n4:
    preprocessed = only_hangle_number(preprocessed)
  if input.n5:
    preprocessed = only_text(preprocessed)
  return Response(preprocessed, media_type="text/plain")


