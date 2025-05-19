import csv

def classify_domain(title, description, keywords):
    text = f"{title} {description} {keywords}".lower()

    if any(word in text for word in ['learn', 'course', 'udemy', 'study', 'coding', 'codechef']):
        return 'Education'
    elif any(word in text for word in ['facebook', 'twitter', 'social', 'linkedin']):
        return 'Social Media'
    elif any(word in text for word in ['ad', 'ads', 'advertising', 'marketing', 'analytics', 'doubleclick']):
        return 'Advertising'
    elif any(word in text for word in ['cloud', 'aws', 's3', 'storage', 'azure']):
        return 'Cloud Services'
    elif any(word in text for word in ['google', 'search', 'bing']):
        return 'Search Engine'
    elif any(word in text for word in ['privacy', 'cookie', 'gdpr', 'consent']):
        return 'Privacy/Compliance'
    else:
        return 'Unknown'

input_file = 'scraped_data.csv'
output_file = 'categorized_data.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = ['domain', 'title', 'category']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in reader:
        category = classify_domain(row['title'], row['description'], row['keywords'])
        writer.writerow({
            'domain': row['domain'],
            'title': row['title'],
            'category': category
        })

print(f"Categorized domains saved to: {output_file}")

