from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import Response
class Text(BaseModel):
  text: str

app = FastAPI(
  title = "Korean Preprocessor",
  description = "Please enter text to preprocess",
  version = "1.0.0"
)

@app.post("/preprocess")
async def get_response(text: Text):
  data = text.text
  return Response(data, media_type="text/plain")


