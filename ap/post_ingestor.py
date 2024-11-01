from database.db_handler import DatabaseHandler
from scrape.scrape import ArticleScraper
from datetime import datetime

def convert_datetime_to_string(data):
    # Recursively convert datetime objects to strings in the data structure
    if isinstance(data, dict):
        return {key: convert_datetime_to_string(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_datetime_to_string(element) for element in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    else:
        return data

class PostIngestor:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def ingest_post(self, post):
        # Extracting necessary information from the response
        post_id = post['post']['id']
        print(post_id)
        title = post['post'].get('name', 'No title available')
        content = post['post'].get('body', 'No content available')
        score = post['counts'].get('score', 0)
        community = post['community'].get('name', 'Unknown')
        creator_name = post['creator'].get('name', 'Unknown')
        creator_avatar = post['creator'].get('avatar', 'No avatar available')
        creator_id = post['creator'].get('id', 'No ID available')
        community_description = post['community'].get('description', 'No description available')
        embed_title = post['post'].get('embed_title', 'No embed title available')
        embed_description = post['post'].get('embed_description', 'No embed description available')
        counts_comments = post['counts'].get('comments', 0)
        counts_score = post['counts'].get('score', 0)
        url = post['post'].get('url', 'No URL available')

        # If URL is available, use ArticleScraper to scrape the article
        article_details = {}
        if url and url != 'No URL available':
            scraper = ArticleScraper(url)
            scraper.scrape()
            article_details = scraper.get_details()

        # Convert all datetime objects to strings in article details
        article_details = convert_datetime_to_string(article_details)

        # Extract article details
        article_title = article_details.get('title', 'No title available')
        article_authors = article_details.get('authors', [])
        publication_date = article_details.get('publication_date', 'No date available')
        article_content = article_details.get('content', 'No content available')
        top_image = article_details.get('top_image', 'No image available')
        article_keywords = article_details.get('keywords', [])
        article_summary = article_details.get('summary', 'No summary available')

        # Convert all datetime objects in post to strings before saving
        post_data_to_save = convert_datetime_to_string({
            'post': {
                'id': post_id,
                'url': url,
                'name': title,
                'body': content,
                'embed_title': embed_title,
                'embed_description': embed_description,
            },
            'community': {
                'name': community,
                'description': community_description,
            },
            'creator': {
                'name': creator_name,
                'avatar': creator_avatar,
                'id': creator_id,
            },
            'counts': {
                'comments': counts_comments,
                'score': counts_score,
            },
            'article': {
                'title': article_title,
                'authors': article_authors,
                'publication_date': publication_date,
                'content': article_content,
                'top_image': top_image,
                'keywords': article_keywords,
                'summary': article_summary
            }
        })

        # Save the post using DatabaseHandler
        self.db_handler.save_post(post_data_to_save)
