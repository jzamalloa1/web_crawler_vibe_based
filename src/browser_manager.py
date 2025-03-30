from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class BrowserManager:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize the Chrome WebDriver."""
        chrome_options = Options()
        if os.getenv('BROWSER_HEADLESS', 'false').lower() == 'true':
            chrome_options.add_argument('--headless=new')  # Updated headless syntax
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # Use system-installed ChromeDriver from Homebrew
        service = Service('/opt/homebrew/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def get_page_content(self, url: str) -> tuple[str, str]:
        """
        Get the content of a webpage.
        Returns a tuple of (title, content)
        """
        self.driver.get(url)
        
        # Wait for dynamic content to load
        self.driver.implicitly_wait(5)
        
        # Get the page source and parse with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Get the title
        title = soup.title.string if soup.title else ''
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get the text content
        content = soup.get_text(separator=' ', strip=True)
        
        return title, content
    
    def get_current_url(self) -> str:
        """Get the current URL in the browser."""
        return self.driver.current_url
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None 