from scrape.scrape import ArticleScraper
from datetime import datetime
from post_manager.models import Post

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
    def ingest_post(self, post):
        # Extracting necessary information from the response
        post_id = post['post']['id']
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

        # Save the post using Django ORM
        post_instance = Post(
            post_id=post_id,
            community_id=post['community'].get('id', None),
            creator_id=creator_id,
            title=title,
            content=content,
            score=score,
            community=community,
            creator_name=creator_name,
            creator_avatar=creator_avatar,
            community_description=community_description,
            embed_title=embed_title,
            embed_description=embed_description,
            counts_comments=counts_comments,
            counts_score=counts_score,
            url=url,
            article_title=article_title,
            article_authors=article_authors,
            publication_date=publication_date,
            article_content=article_content,
            top_image=top_image,
            article_keywords=article_keywords,
            article_summary=article_summary
        )

        # Check if post already exists to prevent duplicates
        if not Post.objects.filter(post_id=post_id).exists():
            post_instance.save()
