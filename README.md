# PDF Parser Service

A small FastAPI service for uploading PDF files, extracting table rows with `pdfplumber`, and using the Gemini API to identify and normalize table headers from the first page image.

The current API exposes a health/root endpoint and a PDF parsing endpoint. It is designed to support a frontend client, such as a Next.js app, that sends PDF files and receives structured JSON containing detected headers and extracted table rows.

## Project Structure

```text
pdf-parser-service/
├── main.py                  # FastAPI app, CORS middleware, and API routes
├── parser/
│   ├── __init__.py
│   └── parser.py            # PDF image/table extraction logic
├── gemini/
│   ├── __init__.py
│   └── gemini.py            # Gemini API integration for header extraction
├── app/
│   ├── routers/             # Conventional FastAPI router modules
│   ├── models/              # Database/domain models
│   ├── schemas/             # Pydantic request/response schemas
│   └── services/            # Business logic/service modules
├── tests/                   # Test suite
├── ARCHITECTURE             # Short architecture notes
├── requirements.txt         # Legacy pip requirements
├── pyproject.toml           # Project metadata, dependencies, and tooling config
├── .env.example             # Environment variable template
├── .gitignore
└── .vscode/
    └── settings.json        # Optional editor defaults
```

Note: `app/`, `routers/`, `models/`, `schemas/`, and `services/` are included as a conventional FastAPI scaffold for future organization. The existing source code remains unchanged.

## Requirements

- Python 3.11 or newer
- A Gemini API key
- System packages required by `pdfplumber`/PDF rendering in your environment

## Setup

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

Alternatively, install from the legacy requirements file:

```bash
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Then set `GEMINI_API_KEY` in `.env`.

## Configuration

The service currently reads the following environment variable:

| Variable | Required | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | Yes | API key used by `google-genai` for Gemini header extraction. |

CORS is currently configured in `main.py` with `allow_origins=["*"]`. For production, restrict this to the actual frontend domain.

## Run

Development server with reload:

```bash
uvicorn main:app --reload
```

Equivalent FastAPI CLI command:

```bash
fastapi dev main.py
```

Production-style Uvicorn command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- `GET /` - health message
- `POST /parse-pdf` - multipart PDF upload using form field `file`

Example request:

```bash
curl -X POST "http://127.0.0.1:8000/parse-pdf" \
  -F "file=@/path/to/file.pdf"
```

## Development Notes

- `parser.Parser` writes uploaded PDFs and first-page images to temporary files during processing.
- `gemini.get_header_JSON_List` sends the first page image to Gemini and requests a JSON array of normalized headers.
- Table rows are extracted with `pdfplumber`.
- Future source refactors can move `main.py` into `app/main.py`, split endpoints into `app/routers/`, and move parsing/Gemini logic under `app/services/`.

## Testing

A `tests/` directory is included for future tests. Once tests are added, run them with:

```bash
pytest
```
