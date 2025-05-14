
# Amazon Product Scraper with Selenium

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/selenium-4.15.2-red)


A configurable web scraper that extracts product data from Amazon while evading bot detection.

## Features

- **Stealth scraping** with anti-detection techniques
- **CAPTCHA handling** with manual intervention support
- **CSV export** of product data (title, price, rating)
- **Pagination support** for multi-page scraping
- **Human-like behavior** with randomized delays

## Tech Stack

| Component | Technology |
|-----------|------------|
| Core Language | Python 3.8+ |
| Browser Automation | Selenium WebDriver |
| Chrome Management | webdriver-manager |
| Data Export | pandas |
| Anti-Detection | Custom Chrome flags |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amazon-scraper.git
   cd amazon-scraper
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.py`:
```python
SEARCH_TERM = "wireless headphones"  # Your target product
BASE_URL = "https://www.amazon.com"  # Regional domain if needed
MAX_PAGES = 3                        # Pages to scrape
```

## Usage

Run the scraper:
```bash
python scraper.py
```

For debugging:
```bash
python -u scraper.py  # Unbuffered output
```

## File Structure

```
amazon-scraper/
├── scraper.py         # Main scraping logic
├── config.py          # Configuration settings
├── requirements.txt   # Dependencies
└── outputs/           # Generated CSV files
```

## Legal Disclaimer

This project is for educational purposes only. Always:
- Check Amazon's Terms of Service
- Respect robots.txt rules
- Limit request frequency
- Consider using official APIs when available

