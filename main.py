from lemmy.api_client import LemmyApiClient
from ap.post_ingestor import PostIngestor
from scrape.scrape import ArticleScraper
from database.db_handler import DatabaseHandler
import json

# Lemmy instance URL
LEMMY_INSTANCE = "https://lemmy.ml"

# Initialize API Client, Ingestor, and Database Handler
api_client = LemmyApiClient(base_url=LEMMY_INSTANCE)
post_ingestor = PostIngestor()
db_handler = DatabaseHandler()

def fetch_and_store_posts():
    posts = api_client.fetch_posts("opensource")  # Replace with actual community name
    for post in posts:
        post_id = post['post']['id']
        # Check if the post already exists in the database
        if db_handler.get_post_by_id(post_id):
            print(f"Post with id {post_id} already exists in the database. Skipping...")
            continue
        # Pass each post directly to the PostIngestor without extra restructuring
        post_ingestor.ingest_post(post)

def query_and_print_post(post_id):
    # Fetch a post from the database to see if the information is stored correctly
    post = db_handler.get_post_by_id(post_id)
    if post:
        print("Stored Post Information:")
        print(json.dumps({
            "post_id": post.post_id,
            "url": post.url,
            "community_id": post.community_id,
            "creator_id": post.creator_id,
            "title": post.title,
            "content": post.content,
            "score": post.score,
            "community": post.community,
            "creator_name": post.creator_name,
            "creator_avatar": post.creator_avatar,
            "community_description": post.community_description,
            "embed_title": post.embed_title,
            "embed_description": post.embed_description,
            "counts_comments": post.counts_comments,
            "counts_score": post.counts_score,
            "article_title": post.article_title,
            "article_authors": post.article_authors,
            "publication_date": post.publication_date,
            "article_content": post.article_content,
            "top_image": post.top_image,
            "article_keywords": post.article_keywords,
            "article_summary": post.article_summary,
            #"full_post": post.full_post
        }, indent=4))
    else:
        print(f"Post with id {post_id} not found in the database.")

# Run the function to fetch and store posts
fetch_and_store_posts()

# Query and print one of the stored posts (replace with a real post_id to test)
query_and_print_post("21976413")
