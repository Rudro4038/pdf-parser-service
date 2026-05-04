from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from parser.parser import Parser

app = FastAPI()

# ✅ CORS (important for Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "PDF Parser API is running"}

@app.post("/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):
    try:
        parser = Parser(file=file)
        data = parser.parse()

        return {
            "success": True,
            "count": len(data),
            "data": data
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
