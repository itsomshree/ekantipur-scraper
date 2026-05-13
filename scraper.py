import json

from playwright.sync_api import sync_playwright


def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # TASK 1: Entertainment News
        print("Navigating to entertainment section...")
        page.goto("https://ekantipur.com/entertainment")

        # Wait for article containers to load
        page.wait_for_selector("div.category-inner-wrapper")

        # Scroll to bottom to trigger lazy loading of images
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        articles = page.query_selector_all("div.category-inner-wrapper")
        print(f"Found {len(articles)} articles")

        entertainment_news = []

        for article in articles[:5]:  # extract top 5 only
            # Title from the h2 anchor tag
            title_el = article.query_selector("h2 a")
            title = title_el.text_content().strip() if title_el else None

            # Thumbnail image URL
            img_el = article.query_selector("div.category-image img")
            image_url = img_el.get_attribute("src") if img_el else None

            # Author name (null if not available)
            author_el = article.query_selector("div.author-name p a")
            author = author_el.text_content().strip() if author_el else None

            # Category is hardcoded since we're scraping the entertainment page
            category = "मनोरञ्जन"

            entertainment_news.append(
                {
                    "title": title,
                    "image_url": image_url,
                    "category": category,
                    "author": author,
                }
            )

            print(f"  ✓ {title}")

        # TASK 2: Cartoon of the Day
        print("\nNavigating to cartoon page...")
        page.goto("https://ekantipur.com/cartoon")

        # Wait for cartoon container to load
        page.wait_for_selector("div.cartoon-wrapper", timeout=15000)

        cartoon_el = page.query_selector("div.cartoon-wrapper")

        # Get title from image alt text and image URL from src
        img_el = cartoon_el.query_selector("img")
        cartoon_title = img_el.get_attribute("alt") if img_el else None
        cartoon_image_url = img_el.get_attribute("src") if img_el else None

        print(f" Cartoon: {cartoon_title}")

        # Build and save output
        output = {
            "entertainment_news": entertainment_news,
            "cartoon_of_the_day": {
                "title": cartoon_title,
                "image_url": cartoon_image_url,
                "author": None,  # Author not available on the page
            },
        }

        # Save with ensure_ascii=False to preserve Nepali (Devanagari) text
        with open("output.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print("\nDone, output.json saved.")
        browser.close()


scrape()
