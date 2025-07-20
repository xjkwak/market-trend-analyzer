"""
Social Media Scraper Agent for Reddit data collection.
"""

import os
import praw
from typing import List, Dict


class SocialMediaScraperAgent:
    """Agent for scraping social media content from Reddit."""
    
    def __init__(self):
        """Initialize the Reddit API client with environment variables."""
        self.client_id = os.getenv('REDDIT_CLIENT_ID', 'your_client_id_here')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', 'your_client_secret_here')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'SocialMediaScraper/1.0 by YourUsername')
        
        # Initialize Reddit client
        self.reddit = None
        self._initialize_reddit_client()
    
    def _initialize_reddit_client(self):
        """Initialize the Reddit client with API credentials."""
        try:
            self.reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
        except Exception as e:
            print(f"Warning: Failed to initialize Reddit client: {e}")
            self.reddit = None
    
    def run(self, domain: str) -> List[Dict[str, str]]:
        """
        Search Reddit for recent posts containing the domain keyword.
        
        Args:
            domain (str): The domain keyword to search for
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'source' and 'content' keys
        """
        if not self.reddit:
            return [{"source": "Reddit", "content": "Error: Reddit client not initialized. Please check your API credentials."}]
        
        try:
            # Search for posts in all subreddits
            search_results = self.reddit.subreddit('all').search(
                domain, 
                sort='new',
                time_filter='week',
                limit=10
            )
            
            posts = []
            for submission in search_results:
                posts.append({
                    "source": "Reddit",
                    "content": submission.title
                })
            
            # Handle case when no posts are found
            if not posts:
                return [{"source": "Reddit", "content": f"No posts found for domain {domain}"}]
            
            return posts
            
        except praw.exceptions.RedditAPIException as e:
            return [{"source": "Reddit", "content": f"Reddit API Error: {str(e)}"}]
        except praw.exceptions.PRAWException as e:
            return [{"source": "Reddit", "content": f"PRAW Error: {str(e)}"}]
        except Exception as e:
            return [{"source": "Reddit", "content": f"Unexpected error: {str(e)}"}]


if __name__ == "__main__":
    agent = SocialMediaScraperAgent()
    results = agent.run("Fintech")
    for post in results:
        print(post)