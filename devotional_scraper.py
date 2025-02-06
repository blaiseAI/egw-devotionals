import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class DevotionalScraper:
    def __init__(self, base_url="https://whiteestate.org"):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_devotional(self, date=None):
        """
        Fetch devotional for a given date or current date if none provided
        """
        if date is None:
            date = datetime.now()
            
        url = f"{self.base_url}/devotional/mlt/{date.strftime('%m_%d')}/"
        
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove footnote references
            for sup in soup.find_all('sup', class_='bookendnote'):
                sup.decompose()
            
            devotional = {
                'date': date.strftime('%Y-%m-%d'),
                'title': self._extract_title(soup),
                'subtitle': self._extract_subtitle(soup),
                'verse': self._extract_verse_reference(soup),
                'content': self._extract_content(soup),
                'thought_for_day': self._extract_thought(soup),
                'source': self._extract_source(soup),
                'url': url
            }
            return devotional
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _extract_title(self, soup):
        title = soup.find('h1', class_='page-title')
        return title.text.strip() if title else ''

    def _extract_subtitle(self, soup):
        subtitle = soup.find('p', class_='center')
        return subtitle.text.strip() if subtitle else ''

    def _extract_verse_reference(self, soup):
        verse = soup.find('p', class_='devotionaltext')
        if verse:
            text = ''.join(
                content.text if hasattr(content, 'text') else str(content)
                for content in verse.contents
            )
            return text.strip()
        return ''

    def _extract_content(self, soup):
        paragraphs = []
        for p in soup.find_all('p', class_='standard-indented'):
            text = p.text.strip()
            if text:
                text = ' '.join(text.split())
                paragraphs.append(text)
        return '\n\n'.join(paragraphs)

    def _extract_thought(self, soup):
        thought = soup.find('div', class_='thought')
        if thought and thought.find_all('p'):
            return thought.find_all('p')[-1].text.strip()
        return ''

    def _extract_source(self, soup):
        for p in soup.find_all('p'):
            if p.text.strip().startswith('From'):
                text = ''.join(
                    content.text if hasattr(content, 'text') else str(content)
                    for content in p.contents
                )
                return text.strip()
        return ''


def main():
    scraper = DevotionalScraper()
    # Get today's devotional
    devotional = scraper.get_devotional()
    
    if devotional:
        # Print the result in a nicely formatted JSON
        print(json.dumps(devotional, indent=2, ensure_ascii=False))
    else:
        print("Failed to fetch devotional")


if __name__ == "__main__":
    main()