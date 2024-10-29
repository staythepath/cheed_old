import requests

class LemmyApiClient:
    def __init__(self, base_url, access_token=None):
        self.base_url = base_url
        self.access_token = access_token

    def fetch_posts(self, community_name=None):
        # Construct the API URL
        url = f"{self.base_url}/api/v3/post/list"
        
        # Optionally include a community name if provided
        params = {}
        if community_name:
            params['community_name'] = community_name

        # Make the request
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            posts = response.json().get("posts", [])
            return posts
        except requests.exceptions.RequestException as e:
            print(f"Error fetching posts: {e}")
            return []

