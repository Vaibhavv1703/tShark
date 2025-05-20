import csv
import requests
from bs4 import BeautifulSoup
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

INPUT_CSV = 'data/captured.csv'
OUTPUT_CSV = 'data/scraped_data.csv'

def get_domain_url(domain):
    return f'https://{domain}'

def scrape_domain(domain):
    url = get_domain_url(domain)
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; VaibhScraper/1.0)'}
    try:
        resp = requests.get(url, timeout=10, verify=False, headers=headers)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        description = ''
        keywords = ''
        for meta in soup.find_all('meta'):
            attr = meta.attrs.get('name', '').lower() or meta.attrs.get('property', '').lower()
            if attr == 'description':
                description = meta.attrs.get('content', '')
            elif attr == 'keywords':
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
    if not os.path.exists('data'):
        os.makedirs('data')

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
            print(f"Scraping {domain}...")
            data = scrape_domain(domain)
            if data:
                writer.writerow(data)

if __name__ == '__main__':
    main()