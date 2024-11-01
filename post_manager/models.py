from django.db import models

class Post(models.Model):
    post_id = models.CharField(max_length=255, unique=True)
    community_id = models.IntegerField(null=True, blank=True)
    creator_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, default="No title available")
    content = models.TextField(default="No content available")
    score = models.IntegerField(default=0)
    community = models.CharField(max_length=255, default="Unknown")
    creator_name = models.CharField(max_length=255, default="Unknown")
    creator_avatar = models.CharField(max_length=255, default="No avatar available")
    community_description = models.TextField(default="No description available")
    embed_title = models.CharField(max_length=255, default="No embed title available")
    embed_description = models.TextField(default="No embed description available")
    counts_comments = models.IntegerField(default=0)
    counts_score = models.IntegerField(default=0)
    url = models.CharField(max_length=255, default="No URL available")
    article_title = models.CharField(max_length=255, default="No title available")
    article_authors = models.JSONField(default=list)  # Storing as a JSON list
    publication_date = models.CharField(max_length=255, default="No date available", null=True, blank=True)  # Allowing null values
    article_content = models.TextField(default="No content available")
    top_image = models.CharField(max_length=255, default="No image available")
    article_keywords = models.JSONField(default=list)  # Storing as a JSON list
    article_summary = models.TextField(default="No summary available")

    def __str__(self):
        return self.title
