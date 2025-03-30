import argparse
import time
from typing import List, Optional
import sys
import os
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from dotenv import load_dotenv

from browser_manager import BrowserManager
from vector_store import VectorStoreManager
from db.models import Document, get_db_session

load_dotenv()

class DocumentCrawler:
    def __init__(self):
        self.browser = None
        self.vector_store = VectorStoreManager()
        self.db_session = get_db_session()
    
    def process_url(self, url: str) -> None:
        """Process a single URL."""
        try:
            if not url:
                print("No URL provided or browser window closed.")
                return
                
            # Skip if already processed
            existing = self.db_session.query(Document).filter_by(url=url).first()
            if existing:
                print(f"URL already processed: {url}")
                return
            
            # Get content
            title, content = self.browser.get_page_content(url)
            
            # Add to vector store
            vector_id = self.vector_store.add_document(
                content=content,
                metadata={'url': url, 'title': title}
            )
            
            # Save to database
            doc = Document(
                url=url,
                title=title,
                content=content,
                vector_id=vector_id
            )
            self.db_session.add(doc)
            self.db_session.commit()
            
            print(f"Successfully processed: {url}")
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            self.db_session.rollback()
    
    def process_url_list(self, urls: List[str]) -> None:
        """Process a list of URLs."""
        self.browser = BrowserManager()
        try:
            for url in urls:
                self.process_url(url.strip())
                time.sleep(1)  # Be nice to servers
        finally:
            self.browser.close()
    
    def browser_mode(self) -> None:
        """Run in browser mode, processing the current page when requested."""
        self.browser = BrowserManager()
        print("Browser mode started. Press Enter to process the current page, 'r' to restart browser, or 'q' to quit.")
        
        try:
            while True:
                command = input("> ").strip().lower()
                if command == 'q':
                    break
                elif command == 'r':
                    print("Restarting browser...")
                    self.browser.close()
                    self.browser = BrowserManager()
                    print("Browser restarted. Navigate to a page you want to crawl.")
                    continue
                
                try:
                    url = self.browser.get_current_url()
                    print(f"Processing current page: {url}")
                    self.process_url(url)
                except (WebDriverException, NoSuchWindowException) as e:
                    print(f"Browser connection lost: {str(e)}")
                    print("Restarting browser...")
                    try:
                        self.browser.close()
                    except:
                        pass
                    self.browser = BrowserManager()
                    print("Browser restarted. Navigate to a page you want to crawl.")
        finally:
            if self.browser:
                self.browser.close()
                self.browser = None

def main():
    parser = argparse.ArgumentParser(description='Document Web Crawler')
    parser.add_argument('--mode', choices=['browser', 'urls'], required=True,
                      help='Operation mode: browser or urls')
    parser.add_argument('--input', help='Input file containing URLs (one per line)')
    
    args = parser.parse_args()
    
    crawler = DocumentCrawler()
    
    if args.mode == 'browser':
        crawler.browser_mode()
    elif args.mode == 'urls':
        if not args.input:
            print("Error: --input file required for urls mode")
            sys.exit(1)
        
        try:
            with open(args.input) as f:
                urls = f.readlines()
            crawler.process_url_list(urls)
        except FileNotFoundError:
            print(f"Error: Input file {args.input} not found")
            sys.exit(1)

if __name__ == '__main__':
    main() 