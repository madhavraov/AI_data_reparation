import fitz  # PyMuPDF
import jsonlines
import os

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    full_text = []

    # Extract text from each page
    total_pages = document.page_count
    for page_num in range(total_pages):
        page = document.load_page(page_num)
        text = page.get_text("text")
        if not text.strip():
            print(f"Warning: No text found on page {page_num} of {pdf_path}")
        filtered_text = filter_text(text, page_num)
        full_text.append(filtered_text)

    return full_text

def filter_text(text, page_num):
    # Filter out unwanted text patterns (e.g., links, copyright notices, headers, footers)
    lines = text.split('\n')
    filtered_lines = []
    for i, line in enumerate(lines):
        if "http" in line or "www" in line:
            continue
        if "Copyright" in line or "All rights reserved" in line:
            continue
        if line.strip() == "":
            continue
        
        # Assuming headers are in the first few lines or last few lines of the page
        if i < 3 or i > len(lines) - 3:
            if "Chapter" in line or line.isnumeric():
                continue
        
        filtered_lines.append(line)
    return "\n".join(filtered_lines)

def structure_text_into_jsonl(full_text, max_words=1000):
    jsonl_data = []
    current_id = 321
    current_text = ""
    current_length = 0

    for page_text in full_text:
        paragraphs = page_text.split('\n')
        
        for paragraph in paragraphs:
            if paragraph.strip() == "":
                continue

            words = paragraph.split()
            paragraph_length = len(words)

            if current_length + paragraph_length > max_words:
                jsonl_data.append({
                    "id": current_id,
                    "text": current_text.strip(),
                    "length": current_length,
                    "ended": False
                })
                current_id += 1
                current_text = ""
                current_length = 0

            current_text += paragraph + "\n"
            current_length += paragraph_length

    # Add the last chunk of text
    if current_text:
        jsonl_data.append({
            "id": current_id,
            "text": current_text.strip(),
            "length": current_length,
            "ended": True
        })

    return jsonl_data

def save_to_jsonl(jsonl_data, output_path):
    with jsonlines.open(output_path, mode='w') as writer:
        writer.write_all(jsonl_data)

def process_pdf_folder(folder_path, output_path):
    all_jsonl_data = []
    current_id = 1

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(folder_path, file_name)
            print(f"Processing {pdf_path}")

            # Extract text from the PDF
            full_text = extract_text_from_pdf(pdf_path)

            if not full_text:
                print(f"No text extracted from {pdf_path}")
                continue

            # Structure the text into JSONL format
            jsonl_data = structure_text_into_jsonl(full_text)

            # Update IDs and collect all JSONL data
            for entry in jsonl_data:
                entry["id"] = current_id
                current_id += 1
                all_jsonl_data.append(entry)

    # Save all JSONL data to a single file
    save_to_jsonl(all_jsonl_data, output_path)
    print(f"All JSONL data has been saved to {output_path}")

# Path to the folder containing PDF files
pdf_folder_path = r"ICAI\Cropped"
output_file_path = "CA_Foundation.jsonl"

# Process all PDF files in the specified folder and save to one JSONL file
process_pdf_folder(pdf_folder_path, output_file_path)
