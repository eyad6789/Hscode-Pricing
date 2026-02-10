import re
import json

# Read the hs_data.js file
with open(r'd:\workspace\Know-Prcie-HScode\deploy\files\hs_data.js', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON part (remove "const HS_DATA = " prefix and trailing ";")
json_str = content.replace('const HS_DATA = ', '', 1).rstrip().rstrip(';')
data = json.loads(json_str)

total = len(data)
missing = []
zero = []
has_price = []

for code, entry in data.items():
    avr = entry.get('avr_mnt')
    if avr is None:
        missing.append(code)
    elif avr == 0:
        zero.append(code)
    else:
        has_price.append(code)

print(f"Total entries: {total}")
print(f"Entries with avr_mnt > 0: {len(has_price)}")
print(f"Entries with avr_mnt = 0: {len(zero)}")
print(f"Entries with avr_mnt = null/missing: {len(missing)}")

if missing:
    print(f"\n--- First 30 entries with missing avr_mnt ---")
    for code in missing[:30]:
        entry = data[code]
        print(f"  {code}: {entry.get('description', 'N/A')}")

if zero:
    print(f"\n--- First 30 entries with avr_mnt = 0 ---")
    for code in zero[:30]:
        entry = data[code]
        print(f"  {code}: {entry.get('description', 'N/A')}")

# Check how many HS codes in the Excel tariff file are NOT in hs_data.js
print(f"\n\nTotal HS codes in data: {total}")
