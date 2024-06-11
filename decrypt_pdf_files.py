import os
import pikepdf

# Define the input and output directory paths
input_dir = r'ICAI\Accounting\Module 2'
output_dir = r'ICAI\Accounting Decrypted\Model 2'

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.pdf'):
        input_pdf_path = os.path.join(input_dir, filename)
        output_pdf_path = os.path.join(output_dir, filename)

        try:
            # Open the restricted PDF
            with pikepdf.open(input_pdf_path) as pdf:
                # Save the unlocked PDF
                pdf.save(output_pdf_path)

            print(f'Successfully unlocked {filename}')
        except Exception as e:
            print(f'Failed to unlock {filename}: {e}')

print('All files have been processed.')
