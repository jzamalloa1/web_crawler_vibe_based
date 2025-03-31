# Document Web Crawler

A powerful web crawler that can extract content from web pages through browser automation or direct URL processing. Uses LlamaIndex for vector storage and retrieval, enabling semantic search capabilities through OpenAI embeddings.

## Features

- **Dual Crawling Modes**:
  - Browser Mode: Interactive crawling through Chrome automation
  - URL List Mode: Batch processing of URLs from a text file
- **Vector Storage**: Uses LlamaIndex with ChromaDB for efficient storage and retrieval
- **Semantic Search**: OpenAI embeddings for intelligent content searching
- **Persistent Storage**: Saves crawled content for future queries
- **Flexible Output**: Support for both human-readable and JSON formats

## Setup

### 1. PostgreSQL Setup

#### Installation (macOS)
```bash
# Install PostgreSQL using Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql
```

For other operating systems, download PostgreSQL from the [official website](https://www.postgresql.org/download/).

#### Database Setup
```bash
# Create a new PostgreSQL user (replace 'your_secure_password' with your chosen password)
psql postgres -c "CREATE USER crawler_user WITH PASSWORD 'your_secure_password' CREATEDB;"

# Create the database
psql postgres -c "CREATE DATABASE document_crawler OWNER crawler_user;"

# Verify the user was created
psql postgres -c "\du"

# Test the connection
PGPASSWORD=your_secure_password psql -U crawler_user -d document_crawler -c "SELECT 1;"
```

### 2. Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Update the .env file with your credentials:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=document_crawler
DB_USER=crawler_user
DB_PASSWORD=your_secure_password  # Replace with your chosen password
OPENAI_API_KEY=your_openai_api_key  # Required for embeddings
VECTOR_STORE_DIR=./vector_store  # Optional, defaults to ./vector_store
```

### 3. ChromeDriver Setup

#### macOS Setup
```bash
# Install ChromeDriver using Homebrew
brew install --cask chromedriver

# Remove macOS security quarantine attribute
sudo xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
```

#### macOS M1/M2/M3 (Apple Silicon) Notes
- If you encounter any issues with ChromeDriver on Apple Silicon Macs:
  1. Make sure you have Chrome browser installed
  2. Verify ChromeDriver is properly installed: `chromedriver --version`
  3. If you get a security warning about ChromeDriver, follow these steps:
     - Open System Settings > Privacy & Security
     - Look for the blocked ChromeDriver message
     - Click "Allow Anyway" if prompted
     - Run the quarantine removal command above

#### Other Operating Systems
- Windows: Download ChromeDriver from [official site](https://sites.google.com/chromium.org/driver/) and add to PATH
- Linux: Install via package manager (e.g., `apt install chromium-chromedriver`)

### 4. Python Environment Setup

1. Install Conda if you haven't already
2. Create the environment:
   ```bash
   conda env create -f environment.yaml
   ```
3. Activate the environment:
   ```bash
   conda activate document_web_crawler
   ```

## Usage

### 1. Crawling Websites

#### URL List Mode
1. Create a text file with URLs (one per line):
   ```bash
   echo "https://example.com" > urls.txt
   ```
2. Run the crawler:
   ```bash
   python src/crawler.py --mode urls --input urls.txt
   ```

#### Browser Mode
1. Run the crawler in interactive mode:
   ```bash
   python src/crawler.py --mode browser
   ```
2. The browser will open, and you can navigate to pages you want to crawl
3. Follow the prompts to process or skip pages

### 2. Querying Crawled Data

Basic search:
```bash
python src/query_data.py "your search query here"
```

Options:
- Control number of results:
  ```bash
  python src/query_data.py "your query" --k 10
  ```
- Get JSON output:
  ```bash
  python src/query_data.py "your query" --json
  ```

## Project Structure

```
.
├── src/
│   ├── crawler.py          # Main crawler implementation
│   ├── browser_manager.py  # Browser automation utilities
│   ├── vector_store.py     # LlamaIndex vector store management
│   ├── query_data.py       # Query interface for crawled data
│   └── db/                 # Database models and utilities
├── vector_store/          # Persistent storage for vectors
├── tests/                # Test files
├── .env.example         # Example environment variables
├── environment.yaml     # Conda environment specification
└── README.md           # This file
```

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords for database credentials
- Keep your environment files secure
- Store API keys securely
- Each developer should maintain their own `.env` file

## Troubleshooting

### Vector Store Issues
- If the index isn't found:
  ```bash
  rm -rf ./vector_store/*  # Clear the vector store
  ```
  Then re-crawl your pages

### ChromeDriver Issues
- If ChromeDriver fails to start:
  1. Check Chrome and ChromeDriver versions match
  2. Verify ChromeDriver is in PATH
  3. Remove quarantine attribute (macOS)
  4. Check security settings

### PostgreSQL Issues
1. If PostgreSQL is not running:
   ```bash
   brew services start postgresql
   brew services list | grep postgresql
   ```
2. Connection issues:
   - Verify PostgreSQL is running
   - Check credentials in `.env`
   - Ensure database exists:
     ```bash
     psql postgres -c "\l" | grep document_crawler
     ``` 