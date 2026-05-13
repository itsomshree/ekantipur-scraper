# Ekantipur Scraper

A Playwright-based web scraper that extracts structured data from [ekantipur.com](https://ekantipur.com) — Nepal's leading news website.

## What It Scrapes

- **Entertainment News** — Top 5 articles from the मनोरञ्जन section, including title, image URL, category, and author
- **Cartoon of the Day** — Title and image URL from the daily cartoon (ग्यात्र) section

## Tech Stack

- Python 3.11+
- [Playwright](https://playwright.dev/python/) — browser automation
- [uv](https://docs.astral.sh/uv/) — package manager

## Project Structure

```
ekantipur-scraper/
├── scraper.py        # Main scraper script
├── output.json       # Extracted data (generated on run)
├── prompts.txt       # AI prompts used during development
├── pyproject.toml    # Project dependencies
└── uv.lock           # Dependency lock file
```

## Setup

**1. Install uv**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

**2. Clone the repo**

```bash
git clone https://github.com/YOUR_USERNAME/ekantipur-scraper.git
cd ekantipur-scraper
```

**3. Install dependencies**

```bash
uv add playwright
uv run playwright install chromium
```

## Usage

```bash
uv run python scraper.py
```

A browser window will open, navigate to ekantipur.com, scrape the data, and save it to `output.json`.

## Output Format

```json
{
  "entertainment_news": [
    {
      "title": "Article headline in Nepali",
      "image_url": "https://...",
      "category": "मनोरञ्जन",
      "author": "Author Name"
    }
  ],
  "cartoon_of_the_day": {
    "title": "Cartoon title",
    "image_url": "https://...",
    "author": null
  }
}
```

## Notes

- Scrolls the page before scraping to trigger lazy-loaded images
- Nepali (Devanagari) text is preserved using `ensure_ascii=False`
- Author field is `null` when not available on the page