import os
import fitz  # PyMuPDF

# Define the input and output directory paths
input_dir = r'ICAI\Accounting Decrypted\Model 2'
output_dir = r'ICAI\Cropped'

# Set the height of header and footer to be removed (in points)
header_height = 50
footer_height = 110

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        input_pdf_path = os.path.join(input_dir, filename)
        output_pdf_path = os.path.join(output_dir, filename)

        try:
            # Open the PDF file
            doc = fitz.open(input_pdf_path)
            
            # Loop through all pages and apply the cropping rectangle
            for page in doc:
                page_rect = page.rect
                left_margin = 0
                bottom_margin = footer_height
                right_margin = page_rect.width
                top_margin = page_rect.height - header_height

                # Define the cropping rectangle without header and footer
                rect = fitz.Rect(left_margin, bottom_margin, right_margin, top_margin)

                # Apply the cropping rectangle
                page.set_cropbox(rect)

            # Save the cropped PDF
            doc.save(output_pdf_path)

            print(f'Successfully cropped {filename}')
        except Exception as e:
            print(f'Failed to crop {filename}: {e}')

print('All files have been processed.')
