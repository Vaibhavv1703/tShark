import csv

capture_file = 'data/captured.csv'
scraped_file = 'data/scraped_data.csv'
output_file = 'data/categorized_data.csv'

scraped_info = {}
with open(scraped_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        domain = row['domain'].strip()
        title = row['title'].strip()
        scraped_info[domain] = title

def categorize(title, domain):
    title = title.lower()
    domain = domain.lower()

    if any(x in domain for x in ['google', 'bing', 'yahoo']):
        return 'Search Engine'
    elif any(x in domain for x in ['facebook', 'twitter', 'instagram', 'reddit']):
        return 'Social Media'
    elif 'youtube' in domain or 'video' in title:
        return 'Video Platform'
    elif 'udemy' in domain or 'coursera' in domain or 'khanacademy' in domain:
        return 'Online Learning'
    elif any(x in title for x in ['analytics', 'ads', 'advertising']):
        return 'Ad/Tracking'
    elif 'amazon' in domain or 'flipkart' in domain:
        return 'E-commerce'
    else:
        return 'Other'

def main():
    with open(capture_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ['source_ip', 'domain', 'category']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            domain = row.get('Domain', '').strip()
            source_ip = row.get('Source IP', '').strip()

            title = scraped_info.get(domain, '')
            category = categorize(title, domain)

            writer.writerow({
                'source_ip': source_ip,
                'domain': domain,
                'category': category
            })

if __name__ == '__main__':
    main()

def run():
    main()