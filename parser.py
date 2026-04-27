import re
from typing import List, Dict, Any

def transform_pdf_rows(rows: List[List[str]]) -> List[Dict[str, Any]]:
    """
    Transforms PDF table rows into JSON objects.

    - Detects header dynamically
    - Skips repeated headers
    - Searches entire row for '2022337'
    - Adds that value as 'id'
    """

    header = None
    transformed_data = []

    # 1️⃣ Detect header (first row with any alphabet)
    for row in rows:
        if row:
            for cell in row:
                if cell and re.search(r"[a-zA-Z]", cell):
                    header = [h.strip() if h else "" for h in row]
                    break
        if header:
            break

    if not header:
        return []

    # 2️⃣ Process rows
    for row in rows:
        if not row or row == header:
            continue

        for cell in row:
            if cell and re.search(r"2022337", cell):
                obj = {
                    header[i]: row[i].strip() if i < len(row) and row[i] else ""
                    for i in range(len(header))
                }
                obj["id"] = cell.strip()
                transformed_data.append(obj)
                break

    return transformed_data