import csv
from datetime import datetime
from collections import defaultdict

captured_file = 'data/captured.csv'
categorized_file = 'data/categorized_data.csv'
output_file = 'data/cleaned_merged.csv'

FILTER_CATEGORIES = [
    'advertisement', 'ads', 'tracking', 'analytics', 'ad server', 'adservice',
    'doubleclick', 'adnxs', 'criteo', 'taboola', 'pubmatic', 'casalemedia',
    'stickyadstv', '360yield', 'onetrust', 'qualaroo', 'media.net', 'contextual',
    'ads-twitter', 'rhythmxchange', 'ad.360yield.com'
]

def parse_timestamp(ts):
    ts_clean = ts.rsplit(' ', 1)[0]
    if '.' in ts_clean:
        date_part, frac = ts_clean.split('.', 1)
        frac = frac[:6]
        ts_clean = f"{date_part}.{frac}"
    return datetime.strptime(ts_clean, "%b %d, %Y %H:%M:%S.%f")

def is_ad_category(category):
    if not category:
        return False
    category_lower = category.lower()
    return any(filt in category_lower for filt in FILTER_CATEGORIES)

def main():
    timestamps_map = defaultdict(list)
    with open(captured_file, 'r', encoding='utf-8') as cap_file:
        reader = csv.DictReader(cap_file)
        for row in reader:
            domain = row['Domain']
            source_ip = row['Source IP']
            timestamp = row['Timestamp']
            timestamps_map[(domain, source_ip)].append(timestamp)

    combined_rows = []
    with open(categorized_file, 'r', encoding='utf-8') as cat_file:
        reader = csv.DictReader(cat_file)
        for row in reader:
            domain = row['domain']
            source_ip = row['source_ip']
            category = row['category']

            if is_ad_category(category):
                continue

            ts_list = timestamps_map.get((domain, source_ip), [])
            if not ts_list:
                continue

            for ts in ts_list:
                combined_rows.append({
                    'domain': domain,
                    'category': category,
                    'source_ip': source_ip,
                    'Timestamp': ts
                })

    combined_rows.sort(key=lambda r: (r['source_ip'], r['category'], parse_timestamp(r['Timestamp'])))

    merged_rows = []
    prev_row = None
    for row in combined_rows:
        if prev_row:
            same_ip = (row['source_ip'] == prev_row['source_ip'])
            same_cat = (row['category'] == prev_row['category'])
            t1 = parse_timestamp(prev_row['Timestamp'])
            t2 = parse_timestamp(row['Timestamp'])
            time_diff = (t2 - t1).total_seconds()

            if same_ip and same_cat and time_diff <= 3:
                continue
            else:
                merged_rows.append(prev_row)
        prev_row = row

    if prev_row:
        merged_rows.append(prev_row)

    fieldnames = ['domain', 'category', 'source_ip', 'Timestamp']
    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in merged_rows:
            writer.writerow(row)

if __name__ == '__main__':
    main()

def run():
    main()