import json
from pathlib import Path

import pytest


@pytest.fixture
def output():
    output_path = Path("output/output.json")
    assert output_path.exists(), "Output file does not exist. Please run the scraper first."
    with open(output_path, encoding="utf-8") as f:
        return json.load(f)


# Entertainment news tests

def test_entertainment_news_count(output):
    assert len(output["entertainment_news"]) == 5
    
def test_entertainment_news_has_titles(output):
    for article in output["entertainment_news"]:
        assert article["title"] is not None
        assert len(article["title"]) > 0

def test_entertainment_news_has_images(output):
    for article in output['entertainment_news']:
        assert article["image_url"] is not None

def test_entertainment_news_has_category(output):
    for article in output['entertainment_news']:
        assert article["category"] == "मनोरञ्जन"
        
def test_entertainment_news_image_urls_are_valid(output):
    for article in output['entertainment_news']:
        if article["image_url"]:
            assert article["image_url"].startswith("https://")


# Cartoon of the day tests

def test_cartoon_exists(output):
    assert output["cartoon_of_the_day"] is not None
    
def test_cartoon_has_title(output):
    assert output["cartoon_of_the_day"]["title"] is not None
    assert len(output["cartoon_of_the_day"]["title"]) > 0

def test_cartoon_has_image(output):
    assert output["cartoon_of_the_day"]["image_url"] is not None
    
def test_cartoon_image_url_is_valid(output):
    assert output["cartoon_of_the_day"]["image_url"].startswith("https://")
