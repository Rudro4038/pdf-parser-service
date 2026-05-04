from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
summarizer = pipeline("summarization", model="facebook/bart-base")

def summarize(text: str):
    result = summarizer(text, max_length=50, min_length=10, do_sample=False)
    return {"summary": result[0]['summary_text']}
