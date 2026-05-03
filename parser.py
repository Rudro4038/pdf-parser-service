import re
from typing import List, Dict, Any

def transform_pdf_rows(rows: List[List[str]]) -> List[Dict[str, Any]]:
    if not rows:
        return []

    # 1. Identify where the header ends and data begins
    # We look for the first row that contains a student ID pattern
    data_start_idx = -1
    for i, row in enumerate(rows):
        if any(cell and re.search(r"\d{10}", str(cell)) for cell in row):
            data_start_idx = i
            break
    
    if data_start_idx <= 0:
        return [] # Could not find data

    # 2. Build a "Collapsed Header"
    # We combine all text from rows BEFORE data_start_idx vertically
    raw_headers = rows[:data_start_idx]
    num_cols = len(rows[data_start_idx])
    final_header = [""] * num_cols

    for col_idx in range(num_cols):
        col_parts = []
        for row_idx in range(len(raw_headers)):
            cell_val = raw_headers[row_idx][col_idx]
            if cell_val and cell_val.strip():
                # Clean up newlines often found in PDF cells
                clean_val = cell_val.replace('\n', ' ').strip()
                col_parts.append(clean_val)
        
        # Join multi-row headers with a space (e.g., "Attendance" + "(Out of 20)")
        final_header[col_idx] = " ".join(col_parts).strip()

    # 3. Process Data Rows
    transformed_data = []
    for row in rows[data_start_idx:]:
        # Skip empty rows or rows that don't look like student data
        id_cell = next((cell for cell in row if cell and re.search(r"\d{10}", str(cell))), None)
        
        if id_cell:
            obj = {}
            for i, h_name in enumerate(final_header):
                if i < len(row):
                    val = row[i].strip() if row[i] else ""
                    # Handle cases like "8.5+1" found in your image
                    obj[h_name] = val
            
            obj["id"] = id_cell.strip()
            transformed_data.append(obj)

    return transformed_data