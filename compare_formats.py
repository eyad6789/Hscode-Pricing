import pandas as pd

# Check the actual format of codes in TSC vs hs_data
tsc = pd.read_excel(r'd:\workspace\Know-Prcie-HScode\TSC 2026-01-11.xlsx')

# Show sample TSC codes
print("Sample TSC IDE_HSC_NB5 values:")
for v in tsc['IDE_HSC_NB5'].dropna().head(30).values:
    print(f"  '{v}' (type: {type(v).__name__})")

print("\nSample TSC codes with AVR_MNT:")
with_price = tsc[tsc['AVR_MNT'].notna()].head(20)
for _, row in with_price.iterrows():
    code = str(row['IDE_HSC_NB5']).replace('.', '').replace(' ', '')
    print(f"  NB5='{row['IDE_HSC_NB5']}' -> clean='{code}' | AVR_MNT={row['AVR_MNT']:.2f} | {row.get('AVR_UNT', '')}")

# Also check hs_data codes format
import json
with open(r'd:\workspace\Know-Prcie-HScode\deploy\files\hs_data.js', encoding='utf-8') as f:
    content = f.read()
json_str = content.replace('const HS_DATA = ', '', 1).rstrip().rstrip(';')
hs_data = json.loads(json_str)

print("\nSample hs_data.js keys:")
keys = list(hs_data.keys())[:20]
for k in keys:
    print(f"  '{k}'")

# Check: are TSC codes formatted differently?
tsc_clean = set(str(v).replace('.', '').replace(' ', '') for v in tsc['IDE_HSC_NB5'].dropna())
hs_keys = set(hs_data.keys())
overlap = tsc_clean & hs_keys
print(f"\nOverlap between TSC clean codes and hs_data keys: {len(overlap)}")
print(f"TSC codes NOT in hs_data: {len(tsc_clean - hs_keys)}")
print(f"hs_data keys NOT in TSC: {len(hs_keys - tsc_clean)}")

# Show some codes that are in both
if overlap:
    print(f"\nSample overlapping codes:")
    for c in sorted(list(overlap))[:10]:
        has_price = hs_data[c].get('avr_mnt') is not None
        print(f"  {c}: has_price_in_js={has_price}")
