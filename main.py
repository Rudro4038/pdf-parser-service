from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
from parser import transform_pdf_rows

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
        all_rows = []

        # Read PDF directly from uploaded file
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    all_rows.extend(table)

        # Transform data
        data = transform_pdf_rows(all_rows)

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