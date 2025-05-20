import csv
from tabulate import tabulate

file_path = 'data/cleaned_merged.csv'

def main():
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            rows.append([
                row['source_ip'],
                row['category'],
                row['domain'],
                row['Timestamp']
            ])

    headers = ['Source IP', 'Category', 'Domain', 'Timestamp']
    print(tabulate(rows, headers=headers, tablefmt='fancy_grid'))

if __name__ == "__main__":
    main()

def run():
    main()