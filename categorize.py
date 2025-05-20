import csv

capture_file = 'data/captured.csv'
scraped_file = 'data/scraped_data.csv'
output_file = 'data/categorized_data.csv'

search = ['google', 'bing', 'yahoo']
social = ['facebook', 'twitter', 'instagram', 'reddit']
video = ['youtube', 'vimeo', 'dailymotion']
learning = ['udemy', 'coursera', 'khanacademy', 'code']
ads = ['doubleclick', 'adnxs', 'criteo', 'taboola', 'pubmatic', 'ads']
shopping = ['amazon', 'flipkart', 'ebay']

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

    if any(x in domain for x in search):
        return 'Search Engine'
    elif any(x in domain for x in social):
        return 'Social Media'
    elif any(x in domain for x in video):
        return 'Video Platform'
    elif any(x in title for x in learning):
        return 'Online Learning'
    elif any(x in title for x in ads):
        return 'Ad/Tracking'
    elif any(x in domain for x in shopping):
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