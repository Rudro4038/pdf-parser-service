import re
from typing import List, Dict, Any,Optional
from fastapi import UploadFile, File
import pdfplumber
from PIL import Image
import tempfile
import os
from gemini.gemini import get_header_JSON_List
import json

class Parser:
    def __init__(self, file: UploadFile = File(...)):
        self.file = file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(self.file.file.read())
            self.tmp_path = tmp.name

    def parse(self) -> List[Dict[str, Any]]:
        try:
            all_rows = self.extract_all_rows()

            # Get the first page as an image
            first_page_img = self.get_the_first_image_from_the_PDF()
            if first_page_img:
                # Save the image to a temporary file to be used by Gemini
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as img_tmp:
                    first_page_img.save(img_tmp, format='PNG')
                    img_path = img_tmp.name
            else:
                return {"error": "Could not extract image from PDF"}

            try:
                # header list in JSON format
                header_list_text_from_gemini = get_header_JSON_List(img_path)
            finally:
                os.remove(img_path) # Clean up the temporary image file

            header_list_from_gemini = json.loads(header_list_text_from_gemini)
            first_student_row = self.get_first_student_row(all_rows)

            header_json_list = self.combine_header_and_first_row(header_list_from_gemini, first_student_row)
            
            response = {
                "header_json_list": header_json_list,
                "raw_data": all_rows
            }
            return response
        finally:
            # Clean up the temporary PDF file
            if hasattr(self, 'tmp_path') and os.path.exists(self.tmp_path):
                os.remove(self.tmp_path)


    def extract_all_rows(self) -> List[List[str]]:
        all_rows = []
        with pdfplumber.open(self.file.file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    all_rows.extend(table)
        return all_rows 


    def get_the_first_image_from_the_PDF(self) -> Optional[Image.Image]:
        """
        Convert the first page of the uploaded PDF into a PIL Image.
        """

        try:
            with pdfplumber.open(self.tmp_path) as pdf:
                if not pdf.pages:
                    return None
                
                # Process the first page
                first_page = pdf.pages[0]
                
                # Convert page to image
                image_of_first_page = first_page.to_image(resolution=300).original
                
                # You can return the image object or its path if needed
                # For now, returning None as in the original logic
                return image_of_first_page
        
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return None
        
        finally:
            os.remove(self.tmp_path)
        

    def get_first_student_row(self, all_rows: List[List[str]]) -> List[str]:
        ans = []
        for row in all_rows:
            flag = 0
            for cell in row:
                if cell and re.search(r'2022337', str(cell)):  # check not None
                    flag = 1
            if flag == 1:
                ans = row
                break
        return ans

    def combine_header_and_first_row(self, header_list_from_gemini: List[str], first_student_row: List[str]) -> List[Dict[str, str]]:
        header_json_list = []
        for i in range(len(first_student_row)):
            header_json_list.append({
                "id" : i+1,
                "header": header_list_from_gemini[i] if i < len(header_list_from_gemini) else "", 
                "attribute": first_student_row[i],
                "isTaken" : True
            })
        return header_json_list