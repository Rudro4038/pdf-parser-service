import PIL.Image
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def get_header_JSON_List(img_path: str) -> str:

    # Define the refined prompt based on your requirements
    img = PIL.Image.open(img_path)
    prompt = """
    Analyze the provided table image and extract a flat list of column headers.

    Guidelines:
    1. Identify Data Columns: Only include headers for "General Columns"—defined as columns that contain unique data for every student row.
    2. Handle Complex Headers: Merge multi-line or vertical text (like "রেজিস্ট্রেশন নং") into a single cohesive string.
    3. Handle Empty/Gibberish Columns: If a column exists in the grid but contains no data across the rows, or if the header is illegible, use an empty string "".
    4. Output Format: Return ONLY a valid JSON array of strings. Do not include markdown formatting or explanations.
    5. If any thing in bangla is found in the header, translate it to english and use that as the header name. For example, "রেজিস্ট্রেশন নং" should be translated to "Registration No" and used as the header name in the output.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")
    
    client = genai.Client(api_key=api_key)

    try:
        # Generate content using the image and the prompt
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                # Use JSON mode to ensure the format is strictly followed
                response_mime_type="application/json"
            )
        )
        return response.text
    except Exception:
        return "[]"
    # return "[\"SL1. No.\", \"Registration no.\", \"Term test (10)\", \"\", \"Attendance (18)\"]"
