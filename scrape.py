import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

INPUT_CSV = 'captured.csv'
OUTPUT_CSV = 'scraped_data.csv'

def get_domain_url(domain):
    # Ensure URL scheme (http://) for requests
    return f'https://{domain}'

def scrape_domain(domain):
    url = get_domain_url(domain)
    try:
        resp = requests.get(url, timeout=5, verify=False)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        description = ''
        keywords = ''
        for meta in soup.find_all('meta'):
            if 'name' in meta.attrs:
                if meta.attrs['name'].lower() == 'description':
                    description = meta.attrs.get('content', '')
                elif meta.attrs['name'].lower() == 'keywords':
                    keywords = meta.attrs.get('content', '')
        return {
            'domain': domain,
            'title': title,
            'description': description,
            'keywords': keywords
        }
    except Exception as e:
        print(f"Failed to scrape {domain}: {e}")
        return None


def main():
    domains = set()
    with open(INPUT_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get('Domain') or row.get('domain')
            if domain:
                domains.add(domain.lower())

    print(f"Found {len(domains)} unique domains.")

    with open(OUTPUT_CSV, 'w', newline='') as f_out:
        fieldnames = ['domain', 'title', 'description', 'keywords']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for domain in domains:
            data = scrape_domain(domain)
            if data:
                writer.writerow(data)

if __name__ == '__main__':
    main()

