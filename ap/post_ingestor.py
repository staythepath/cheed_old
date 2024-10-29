from database.db_handler import DatabaseHandler

class PostIngestor:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def ingest_post(self, post_data):
        # Extracting necessary information from the response
        post_id = post_data['post']['id']
        title = post_data['post'].get('name', 'No title available')
        content = post_data['post'].get('body', 'No content available')
        score = post_data['counts'].get('score', 0)
        community = post_data['community'].get('name', 'Unknown')
        creator_name = post_data['creator'].get('name', 'Unknown')
        creator_avatar = post_data['creator'].get('avatar', 'No avatar available')
        creator_id = post_data['creator'].get('id', 'No ID available')
        community_description = post_data['community'].get('description', 'No description available')
        embed_title = post_data['post'].get('embed_title', 'No embed title available')
        embed_description = post_data['post'].get('embed_description', 'No embed description available')
        counts_comments = post_data['counts'].get('comments', 0)
        counts_score = post_data['counts'].get('score', 0)

        # Save the post using DatabaseHandler
        self.db_handler.save_post({
            'post': {
                'id': post_id,
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
                'id' : creator_id,
            },
            'counts': {
                'comments': counts_comments,
                'score': counts_score,
            }
        })
