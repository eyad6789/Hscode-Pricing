import pandas as pd
import json

tsc = pd.read_excel(r'd:\workspace\Know-Prcie-HScode\TSC 2026-01-11.xlsx')

# Check NB1 and NB2 columns for actual HS codes
print("Sample IDE_HSC_NB1 values (first 20 with AVR_MNT):")
with_price = tsc[tsc['AVR_MNT'].notna()].head(20)
for _, row in with_price.iterrows():
    print(f"  NB1={row['IDE_HSC_NB1']}, NB2={row['IDE_HSC_NB2']}, NB5='{row['IDE_HSC_NB5']}', AVR_MNT={row['AVR_MNT']:.2f}")

# Check if NB1 codes match hs_data keys
with open(r'd:\workspace\Know-Prcie-HScode\deploy\files\hs_data.js', encoding='utf-8') as f:
    content = f.read()
json_str = content.replace('const HS_DATA = ', '', 1).rstrip().rstrip(';')
hs_data = json.loads(json_str)
hs_keys = set(hs_data.keys())

# NB1 as string
tsc_nb1 = set(str(int(v)) for v in tsc['IDE_HSC_NB1'].dropna())
tsc_nb2 = set(str(int(v)) for v in tsc['IDE_HSC_NB2'].dropna())

overlap_nb1 = tsc_nb1 & hs_keys
overlap_nb2 = tsc_nb2 & hs_keys
print(f"\nOverlap NB1 with hs_data: {len(overlap_nb1)}")
print(f"Overlap NB2 with hs_data: {len(overlap_nb2)}")

# Now check: can we fill missing avr_mnt using NB1?
missing_codes = {code for code, entry in hs_data.items() if entry.get('avr_mnt') is None}
print(f"\nMissing codes in hs_data: {len(missing_codes)}")

tsc_with_price = tsc[tsc['AVR_MNT'].notna() & (tsc['AVR_MNT'] > 0)].copy()
tsc_with_price['nb1_str'] = tsc_with_price['IDE_HSC_NB1'].astype(int).astype(str)

# Get avg AVR_MNT per NB1
nb1_avg = tsc_with_price.groupby('nb1_str').agg({
    'AVR_MNT': 'mean',
    'AVR_UNT': 'first',
    'AVR_UNT_NAM': 'first'
}).reset_index()

nb1_set = set(nb1_avg['nb1_str'])
fillable = missing_codes & nb1_set
print(f"Missing codes fillable via NB1 match: {len(fillable)}")

if fillable:
    print("\nSample fillable codes:")
    for code in sorted(list(fillable))[:20]:
        row = nb1_avg[nb1_avg['nb1_str'] == code].iloc[0]
        desc = hs_data[code].get('description', 'N/A')
        print(f"  {code}: {desc} -> AVR_MNT={row['AVR_MNT']:.2f} {row['AVR_UNT']}")
