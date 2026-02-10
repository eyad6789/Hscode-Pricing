import pandas as pd
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load TSC
tsc = pd.read_excel(r'd:\workspace\Know-Prcie-HScode\TSC 2026-01-11.xlsx')
tsc_p = tsc[tsc['AVR_MNT'].notna()]

# Build NB1 -> price map
nb1_prices = {}
for _, r in tsc_p.iterrows():
    code = str(int(r['IDE_HSC_NB1']))
    if code not in nb1_prices:
        nb1_prices[code] = {'avr': r['AVR_MNT'], 'unt': r.get('AVR_UNT', ''), 'nam': r.get('AVR_UNT_NAM', '')}

# Load hs_data
with open(r'd:\workspace\Know-Prcie-HScode\deploy\files\hs_data.js', 'r', encoding='utf-8') as f:
    content = f.read()
d = json.loads(content.replace('const HS_DATA = ', '', 1).rstrip().rstrip(';'))

# Missing codes
missing = {k for k, v in d.items() if v.get('avr_mnt') is None}

print(f"Missing codes: {len(missing)}")
print(f"NB1 price keys: {len(nb1_prices)}")

# Check code length distributions
from collections import Counter
ml = Counter(len(k) for k in missing)
nl = Counter(len(k) for k in nb1_prices.keys())
print(f"Missing code lengths: {dict(ml)}")
print(f"NB1 code lengths: {dict(nl)}")

# Try prepending 0
fill_prepend = {m for m in missing if '0' + m in nb1_prices}
# Try appending 0
fill_append = {m for m in missing if m + '0' in nb1_prices}
# Try matching first 7 chars of NB1 (strip last digit)
nb1_7 = {}
for code, data in nb1_prices.items():
    c7 = code[:7]
    if c7 not in nb1_7:
        nb1_7[c7] = data
fill_7 = {m for m in missing if m in nb1_7}

print(f"Fillable (prepend 0): {len(fill_prepend)}")
print(f"Fillable (append 0): {len(fill_append)}")
print(f"Fillable (first 7 of NB1): {len(fill_7)}")

# Show samples
if fill_append:
    print("\nSample append-0 fills:")
    for c in sorted(list(fill_append))[:5]:
        nb1_code = c + '0'
        data = nb1_prices[nb1_code]
        print(f"  {c} -> NB1:{nb1_code} AVR={data['avr']:.2f}")

if fill_7:
    print("\nSample first-7 fills:")
    for c in sorted(list(fill_7))[:10]:
        data = nb1_7[c]
        desc = d[c].get('description', 'N/A')
        print(f"  {c}: {desc} -> AVR={data['avr']:.2f} {data['unt']}")
