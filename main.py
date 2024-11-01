from lemmy.api_client import LemmyApiClient
from ap.post_ingestor import PostIngestor
from scrape.scrape import ArticleScraper

# Lemmy instance URL
LEMMY_INSTANCE = "https://lemmy.ml"

# Initialize API Client and Ingestor
api_client = LemmyApiClient(base_url=LEMMY_INSTANCE)
post_ingestor = PostIngestor()

def fetch_and_store_posts():
    posts = api_client.fetch_posts("opensource")  # Replace with actual community name
    for post in posts:
        url = post['post'].get('url')
        if url:
            scraper = ArticleScraper(url)
            scraper.scrape()
            article_details = scraper.get_details()
            print('ARTICLE CONTENT:', article_details)
            # Optionally add article details to the post_data
            post['article'] = article_details
        post_ingestor.ingest_post(post)

# Run the function
fetch_and_store_posts()
