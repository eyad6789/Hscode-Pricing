import pandas as pd
import PyPDF2
import sys

# Inspect Excel file
print("=" * 50)
print("INSPECTING EXCEL FILE")
print("=" * 50)
df = pd.read_excel('التعرفية الجديدة 2026-1.xlsx')
print(f'\nShape: {df.shape}')
print('\nAll columns:')
for i, col in enumerate(df.columns):
    print(f'{i}: {col}')
print('\nFirst 10 rows:')
with pd.option_context('display.max_columns', None, 'display.width', None):
    print(df.head(10))

# Save to file for easier viewing
output_file = 'excel_inspection.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("Excel File Inspection\n")
    f.write("=" * 50 + "\n\n")
    f.write(f'Shape: {df.shape}\n\n')
    f.write('Columns:\n')
    for i, col in enumerate(df.columns):
        f.write(f'{i}: {col}\n')
    f.write('\n\nFirst 20 rows:\n')
    f.write(df.head(20).to_string())

print(f'\n\nExcel data saved to {output_file}')

# Inspect PDF file
print("\n" + "=" * 50)
print("INSPECTING PDF FILE")
print("=" * 50)
try:
    with open('جداول التعرفة الكمركية قرار مجلس الوزراء 957.pdf', 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        print(f'\nTotal pages: {len(reader.pages)}')
        
        # Save PDF text to file
        pdf_output = 'pdf_inspection.txt'
        with open(pdf_output, 'w', encoding='utf-8') as f:
            f.write(f'Total pages: {len(reader.pages)}\n\n')
            for i in range(min(5, len(reader.pages))):
                f.write(f'\n{"=" * 50}\n')
                f.write(f'PAGE {i+1}\n')
                f.write(f'{"=" * 50}\n')
                f.write(reader.pages[i].extract_text())
                f.write('\n\n')
        
        print(f'PDF data saved to {pdf_output}')
        
except Exception as e:
    print(f'Error reading PDF: {e}')
    import traceback
    traceback.print_exc()
