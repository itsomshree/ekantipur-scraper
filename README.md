# Ekantipur Scraper

A production-grade web scraper that extracts structured data from [ekantipur.com](https://ekantipur.com) - Nepal's leading news website. Built with Python, Playwright, and Pydantic.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-latest-45ba4b?style=flat&logo=playwright&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=flat&logo=pydantic&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9?style=flat)
![Tests](https://img.shields.io/badge/Tests-9%20passing-brightgreen?style=flat)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)

---

## Overview

Ekantipur Scraper automates the extraction of two data sources from ekantipur.com:

- **Entertainment News** - Top 5 articles from the मनोरञ्जन section with title, image URL, category, and author
- **Cartoon of the Day** - Title and image URL from the daily ग्यात्र section

The scraper handles dynamic content loading, lazy-loaded images, and preserves Nepali Devanagari text correctly in the output.

---

## Features

- **Playwright browser automation** - handles JavaScript-rendered content
- **Lazy loading support** - scrolls page to trigger image loading
- **Pydantic data validation** - structured, type-safe output models
- **Structured logging** - timestamped logs with error tracking
- **Full test suite** - 9 pytest tests covering all data points
- **Config driven** - all settings in one place
- **GitHub Actions** - automated daily runs with artifact upload
- **Nepali text support** - Devanagari script preserved in output

---

## Project Structure

```
ekantipur-scraper/
├── .github/
│   └── workflows/
│       └── scraper.yml         # GitHub Actions workflow
├── src/
│   └── ekantipur_scraper/
│       ├── __init__.py
│       ├── scraper.py          # Main scraper logic
│       ├── models.py           # Pydantic data models
│       └── config.py           # Configuration settings
├── tests/
│   ├── __init__.py
│   └── test_scraper.py         # pytest test suite
├── output/                     # Generated output (gitignored)
├── main.py                     # Entry point
├── pyproject.toml              # Project dependencies
├── uv.lock                     # Dependency lock file
├── .gitignore
├── .python-version
└── README.md
```

---

## Installation

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

**1. Install uv**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

**2. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ekantipur-scraper.git
cd ekantipur-scraper
```

**3. Install dependencies**

```bash
uv sync
uv run playwright install chromium
```

**Using pip instead:**

```bash
pip install -r requirements.txt
playwright install chromium
```

---

## Usage

```bash
uv run python main.py
```

A Chromium browser window will open, navigate to ekantipur.com, scrape the data, and save the results to `output/output.json`.

---

## Output Format

```json
{
  "entertainment_news": [
    {
      "title": "Article headline in Nepali",
      "image_url": "https://assets-cdn-api.ekantipur.com/...",
      "category": "मनोरञ्जन",
      "author": "Author Name"
    }
  ],
  "cartoon_of_the_day": {
    "title": "Cartoon title in Nepali",
    "image_url": "https://assets-cdn-api.ekantipur.com/...",
    "author": null
  }
}
```

---

## Running Tests

```bash
uv run pytest tests/ -v
```

Expected output:

```
tests/test_scraper.py::test_entertainment_news_count PASSED
tests/test_scraper.py::test_entertainment_news_has_titles PASSED
tests/test_scraper.py::test_entertainment_news_has_images PASSED
tests/test_scraper.py::test_entertainment_news_has_category PASSED
tests/test_scraper.py::test_entertainment_news_image_urls_are_valid PASSED
tests/test_scraper.py::test_cartoon_exists PASSED
tests/test_scraper.py::test_cartoon_has_title PASSED
tests/test_scraper.py::test_cartoon_has_image PASSED
tests/test_scraper.py::test_cartoon_image_url_is_valid PASSED

9 passed in 0.02s
```

---

## Configuration

All settings are managed in `src/ekantipur_scraper/config.py`:

| Setting | Default | Description |
|---|---|---|
| `MAX_ARTICLES` | `5` | Number of articles to extract |
| `SCROLL_WAIT_MS` | `2000` | Wait time after scrolling (ms) |
| `SELECTOR_TIMEOUT_MS` | `5000` | Timeout for elements on loaded page (ms) |
| `NAVIGATION_TIMEOUT_MS` | `15000` | Timeout for new page navigation (ms) |
| `OUTPUT_PATH` | `output/output.json` | Path to save output file |

---

## GitHub Actions

The scraper runs automatically every day at 12:15 AM UTC (6:00 AM NPT) via GitHub Actions. You can also trigger it manually from the **Actions** tab in your repository.

The generated `output.json` is uploaded as a workflow artifact and can be downloaded directly from GitHub.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| [Python 3.11+](https://python.org) | Core language |
| [Playwright](https://playwright.dev/python/) | Browser automation |
| [Pydantic v2](https://docs.pydantic.dev/) | Data validation and modeling |
| [pytest](https://pytest.org) | Testing framework |
| [uv](https://docs.astral.sh/uv/) | Package management |
| [GitHub Actions](https://github.com/features/actions) | CI/CD and automation |

---

## Notes

- Headless mode is automatically enabled in CI environments (`CI=true`) and disabled locally for easier debugging
- Nepali Devanagari text is preserved using `ensure_ascii=False` in JSON output
- Author field is `null` for articles and cartoons where author information is unavailable
- Page is scrolled before scraping to ensure lazy-loaded images are fully rendered

---

## Known Limitation: Cloudflare Bot Protection in CI

When running via GitHub Actions, ekantipur.com's **Cloudflare bot protection** blocks the scraper with a "Performing security verification" challenge page. This happens because GitHub-hosted runners use shared, well-known cloud/datacenter IP ranges, which Cloudflare flags as likely bot traffic - unlike a residential IP (e.g., running locally), which passes through without a challenge.

**The scraper works correctly when run locally** since local connections come from a residential IP.

In a production environment, this is typically addressed with one or more of the following:
- **Residential or rotating proxies** to avoid datacenter IP flags
- **Self-hosted runners** (running the workflow from a non-cloud IP)
- **Headless-detection evasion** techniques (stealth plugins, fingerprint spoofing)
- **Official APIs** if the target site provides one, avoiding scraping entirely

This is a deliberate architectural trade-off for this project - solving full Cloudflare evasion is out of scope for this assessment, so the limitation is documented here rather than worked around with fragile hacks.

---

## License

MIT License