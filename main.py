from lemmy.api_client import LemmyApiClient
from ap.post_ingestor import PostIngestor

# Lemmy instance URL
LEMMY_INSTANCE = "https://lemmy.ml"

# Initialize API Client and Ingestor
api_client = LemmyApiClient(base_url=LEMMY_INSTANCE)
post_ingestor = PostIngestor()

def fetch_and_store_posts():
    posts = api_client.fetch_posts("opensource")  # Replace with actual community name
    for post in posts:
        #print(post)
        post_ingestor.ingest_post(post)

# Run the function
fetch_and_store_posts()
