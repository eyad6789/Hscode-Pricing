import pandas as pd
import json

# Load TSC data
tsc = pd.read_excel(r'd:\workspace\Know-Prcie-HScode\TSC 2026-01-11.xlsx')
print(f"TSC rows: {len(tsc)}")
print(f"TSC unique HS codes (NB5): {tsc['IDE_HSC_NB5'].nunique()}")
print(f"TSC rows with AVR_MNT: {tsc['AVR_MNT'].notna().sum()}")
print(f"TSC rows with AVR_MNT > 0: {(tsc['AVR_MNT'] > 0).sum()}")

# Load hs_data.js
with open(r'd:\workspace\Know-Prcie-HScode\deploy\files\hs_data.js', encoding='utf-8') as f:
    content = f.read()
json_str = content.replace('const HS_DATA = ', '', 1).rstrip().rstrip(';')
hs_data = json.loads(json_str)

# Find codes with null avr_mnt in hs_data.js
missing_codes = [code for code, entry in hs_data.items() if entry.get('avr_mnt') is None]
print(f"\nHS codes with missing avr_mnt in hs_data.js: {len(missing_codes)}")

# Check if TSC has data for these missing codes
# TSC IDE_HSC_NB5 format might need normalization
tsc_codes = tsc.dropna(subset=['AVR_MNT'])
tsc_codes = tsc_codes[tsc_codes['AVR_MNT'] > 0]

# Normalize TSC codes - remove dots and spaces
tsc_codes['clean_code'] = tsc_codes['IDE_HSC_NB5'].astype(str).str.replace('.', '').str.replace(' ', '').str.strip()

# Group by clean_code and average the AVR_MNT
tsc_avg = tsc_codes.groupby('clean_code').agg({
    'AVR_MNT': 'mean',
    'AVR_UNT': 'first',
    'AVR_UNT_NAM': 'first'
}).reset_index()

print(f"\nTSC unique codes with prices: {len(tsc_avg)}")

# How many missing codes can be filled from TSC?
missing_set = set(missing_codes)
tsc_set = set(tsc_avg['clean_code'].values)

can_fill = missing_set & tsc_set
print(f"Missing codes that can be filled from TSC: {len(can_fill)}")
print(f"Still missing after fill: {len(missing_set - tsc_set)}")

# Show first few fillable entries
if can_fill:
    print(f"\n--- First 20 codes that can be filled ---")
    for code in sorted(list(can_fill))[:20]:
        tsc_row = tsc_avg[tsc_avg['clean_code'] == code].iloc[0]
        desc = hs_data.get(code, {}).get('description', 'N/A')
        print(f"  {code}: {desc} -> AVR_MNT={tsc_row['AVR_MNT']:.2f} {tsc_row['AVR_UNT']}")
