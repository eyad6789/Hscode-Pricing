import pandas as pd

# Check the TSC Excel file for avr_mnt data
df = pd.read_excel(r'd:\workspace\Know-Prcie-HScode\TSC 2026-01-11.xlsx')
print(f'Shape: {df.shape}')
print(f'\nColumns:')
for i, col in enumerate(df.columns):
    print(f'  {i}: {col}')
print(f'\nFirst 10 rows:')
print(df.head(10).to_string())

# Check for avr_mnt related columns
avr_cols = [c for c in df.columns if 'avr' in str(c).lower() or 'mnt' in str(c).lower() or 'price' in str(c).lower()]
print(f'\nAVR/price related columns: {avr_cols}')

# Check how many unique HS codes
hs_cols = [c for c in df.columns if 'hs' in str(c).lower() or 'code' in str(c).lower() or 'hsc' in str(c).lower()]
print(f'HS code related columns: {hs_cols}')

# Look at all column types
print(f'\nColumn dtypes:')
print(df.dtypes)
