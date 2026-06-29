import json
import logging

from playwright.sync_api import sync_playwright

from .config import (
    CARTOON_URL,
    ENTERTAINMENT_URL,
    HEADLESS,
    MAX_ARTICLES,
    NAVIGATION_TIMEOUT_MS,
    OUTPUT_PATH,
    SCROLL_WAIT_MS,
    SELECTOR_TIMEOUT_MS,
)
from .models import Article, CartoonOfTheDay, ScraperOutput

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def scrape_entertainment_news(page) -> list[Article]:
    logger.info("Navigating to entertainment news page...")
    page.goto(ENTERTAINMENT_URL)
    
    
    page.screenshot(path="output/debug_screenshot.png")
    logger.info("Saved debug screenshot")

    # Wait for the articles to load
    page.wait_for_selector("div.category-inner-wrapper", timeout=SELECTOR_TIMEOUT_MS)

    # Scroll to trigger lazy loading of images
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(SCROLL_WAIT_MS)

    articles = page.query_selector_all("div.category-inner-wrapper")
    logger.info(f"Found {len(articles)} articles")

    entertainment_news = []

    for article in articles[:MAX_ARTICLES]:
        try:
            title_el = article.query_selector("h2 a")
            title = title_el.text_content().strip() if title_el else None

            img_el = article.query_selector("div.category-image img")
            image_url = img_el.get_attribute("src") if img_el else None

            author_el = article.query_selector("div.author-name p a")
            author = author_el.text_content().strip() if author_el else None

            # Hardcoding category as it is the entertainment section
            category = "मनोरञ्जन"

            entertainment_news.append(
                Article(
                    title=title, image_url=image_url, category=category, author=author
                )
            )

            logger.info(f"Extracted article: {title}")

        except Exception as e:
            logger.error(f"Error extracting articles: {e}")
            continue

    return entertainment_news


def scrape_cartoon(page) -> CartoonOfTheDay:
    logger.info("Navigating to cartoon page...")
    page.goto(CARTOON_URL)

    page.wait_for_selector("div.cartoon-wrapper", timeout=NAVIGATION_TIMEOUT_MS)

    try:
        cartoon_el = page.query_selector("div.cartoon-wrapper")

        img_el = cartoon_el.query_selector("img")
        cartoon_title = img_el.get_attribute("alt") if img_el else None
        cartoon_image_url = img_el.get_attribute("src") if img_el else None

        logger.info(f"Cartoon title: {cartoon_title}")

        return CartoonOfTheDay(
            title=cartoon_title, image_url=cartoon_image_url, author=None
        )
    except Exception as e:
        logger.error(f"Error extracting cartoon: {e}")
        return CartoonOfTheDay(title=None, image_url=None, author=None)


def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()

        try:
            entertainment_news = scrape_entertainment_news(page)

            cartoon = scrape_cartoon(page)

            output = ScraperOutput(
                entertainment_news=entertainment_news, cartoon_of_the_day=cartoon
            )

            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(output.model_dump(), f, ensure_ascii=False, indent=2)

            logger.info(f"\n Done! Saved to {OUTPUT_PATH}")
        except Exception as e:
            logger.error(f"Scrapper failed: {e}")
            raise
        finally:
            browser.close()


if __name__ == "__main__":
    scrape()
