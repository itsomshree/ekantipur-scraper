from pydantic import BaseModel


class Article(BaseModel):
    title: str | None
    image_url: str | None
    category: str
    author: str | None


class CartoonOfTheDay(BaseModel):
    title: str | None
    image_url: str | None
    author: str | None


class ScraperOutput(BaseModel):
    entertainment_news: list[Article]
    cartoon_of_the_day: CartoonOfTheDay
