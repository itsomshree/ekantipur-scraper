import os

BASE_URL = "https://ekantipur.com"
ENTERTAINMENT_URL = f"{BASE_URL}/entertainment"
CARTOON_URL = f"{BASE_URL}/cartoon"
MAX_ARTICLES = 5
SCROLL_WAIT_MS = 2000
OUTPUT_PATH = "output/output.json"
SELECTOR_TIMEOUT_MS = 15000
NAVIGATION_TIMEOUT_MS = 20000

# Use headless mode in CI env to prevent crash
HEADLESS = os.getenv("CI", "false").lower() == "true"
