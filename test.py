from activitypub.manager import Manager
from activitypub.database import ListDatabase
import requests

# Initialize ActivityPub Manager
db = ListDatabase()  # For testing, use an in-memory database; replace with SQLAlchemy or MongoDB as needed
manager = Manager(database=db)

# Define the Lemmy instance URL and API endpoint for posts
LEMMY_INSTANCE = "https://lemmy.ml"  # Replace with your Lemmy instance URL

def fetch_posts_from_activitypub():
    try:
        response = requests.get(f"{LEMMY_INSTANCE}/api/v3/post/list")
        response.raise_for_status()

        posts = response.json().get("posts", [])
        for post in posts:
            print("Title:", post["post"]["name"])
            # Check if 'body' exists before trying to print it
            if "body" in post["post"]:
                print("Content:", post["post"]["body"])
            else:
                print("Content: No body available.")
            print("Score:", post["counts"]["score"])
            print("-" * 20)

            # Optional: Add to ActivityPub database if needed
            #db.add(post)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching posts: {e}")


# Run the function
fetch_posts_from_activitypub()
