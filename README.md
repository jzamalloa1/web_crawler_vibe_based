# Document Web Crawler

A powerful web crawler that can extract content from web pages through browser automation or direct URL processing. Uses LlamaIndex for vector storage and retrieval.

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

#### Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Update the .env file with your database credentials
# Edit these values in .env:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=document_crawler
DB_USER=crawler_user
DB_PASSWORD=your_secure_password  # Replace with your chosen password
```

### 2. Conda Environment Setup

1. Install Conda if you haven't already
2. Create the environment:
   ```bash
   conda env create -f environment.yaml
   ```
3. Activate the environment:
   ```bash
   conda activate document_web_crawler
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

## Usage

The crawler can be used in two modes:

1. Browser Integration Mode:
   ```bash
   python src/crawler.py --mode browser
   ```
   This will launch a browser session where you can navigate to pages you want to crawl.

2. URL List Mode:
   ```bash
   python src/crawler.py --mode urls --input urls.txt
   ```
   This will process a list of URLs from a text file.

## Project Structure

- `src/`: Source code directory
  - `crawler.py`: Main crawler implementation
  - `browser_manager.py`: Browser automation utilities
  - `vector_store.py`: LlamaIndex vector store management
  - `db/`: Database models and utilities
- `tests/`: Test files
- `.env.example`: Example environment variables
- `environment.yaml`: Conda environment specification

## Troubleshooting

### PostgreSQL Issues

1. If PostgreSQL is not running:
   ```bash
   # Start PostgreSQL service
   brew services start postgresql
   
   # Check status
   brew services list | grep postgresql
   ```

2. If you can't connect to the database:
   - Verify PostgreSQL is running
   - Check your credentials in `.env`
   - Ensure the database exists:
     ```bash
     psql postgres -c "\l" | grep document_crawler
     ```

3. To reset credentials:
   ```bash
   # Change user password
   psql postgres -c "ALTER USER crawler_user WITH PASSWORD 'new_password';"
   
   # Don't forget to update your .env file after changing the password
   ```

### Security Notes

- Never commit the `.env` file to version control
- Use strong passwords for database credentials
- Keep your environment files secure
- Each developer should maintain their own `.env` file with their credentials 