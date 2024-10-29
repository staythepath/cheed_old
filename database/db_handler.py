from sqlalchemy import create_engine, Column, String, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Set up base and database engine
Base = declarative_base()
DATABASE_URL = "postgresql://stay:thisisit@localhost/fediverse_posts"

# Create the engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Define the Post model
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(String, unique=True)
    community_id = Column(Integer)  # Adding community_id
    creator_id = Column(Integer)    # Adding creator_id
    title = Column(String)
    content = Column(Text)
    score = Column(Integer)
    community = Column(String)
    creator_name = Column(String)
    creator_avatar = Column(String)
    community_description = Column(Text)
    embed_title = Column(String)
    embed_description = Column(Text)
    counts_comments = Column(Integer)
    counts_score = Column(Integer)
    full_post = Column(JSON)  # Store the full JSON response

# Initialize the database (creates tables if they do not exist)
Base.metadata.create_all(engine)

class DatabaseHandler:
    def __init__(self):
        self.session = session

    def save_post(self, post_data):
        post_id = post_data['post']['id']
        community_id = post_data['post'].get('community_id', None)  # Fetching community_id
        creator_id = post_data['creator'].get('id', None)  # Fetching creator_id
        title = post_data['post'].get('name', 'No title available')
        content = post_data['post'].get('body', 'No content available')
        score = post_data['counts'].get('score', 0)
        community = post_data['community'].get('name', 'Unknown')
        creator_name = post_data['creator'].get('name', 'Unknown')
        creator_avatar = post_data['creator'].get('avatar', 'No avatar available')
        community_description = post_data['community'].get('description', 'No description available')
        embed_title = post_data['post'].get('embed_title', 'No embed title available')
        embed_description = post_data['post'].get('embed_description', 'No embed description available')
        counts_comments = post_data['counts'].get('comments', 0)
        counts_score = post_data['counts'].get('score', 0)
        full_post = post_data

        

        # Create a new post instance
        post = Post(
            post_id=str(post_id),
            community_id=community_id,
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
            full_post=full_post
        )

        # Check if post already exists
        existing_post = self.session.query(Post).filter_by(post_id=str(post_id)).first()
        if existing_post:
            print(f"Post with id {post_id} already exists.")
            print(json.dumps(full_post, indent=4))
            return
        
        # Add to session and commit
        self.session.add(post)
        self.session.commit()
        print(json.dumps(full_post, indent=4))

    def get_all_posts(self):
        return self.session.query(Post).all()

    def get_post_by_id(self, post_id):
        return self.session.query(Post).filter_by(post_id=str(post_id)).first()

    def delete_post(self, post_id):
        post = self.get_post_by_id(post_id)
        if post:
            self.session.delete(post)
            self.session.commit()
            print(f"Post {post_id} deleted successfully.")
        else:
            print(f"Post with id {post_id} does not exist.")
