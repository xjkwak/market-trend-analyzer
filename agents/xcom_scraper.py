"""
X.com (Twitter) Scraper Agent for Twitter API v2 data collection.
"""

import os
import requests
from typing import List, Dict
from dotenv import load_dotenv


class XComScraperAgent:
    """Agent for scraping X.com (Twitter) content using Twitter API v2."""
    
    def __init__(self):
        """Initialize the Twitter API client with Bearer Token authentication."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Get bearer token from environment variable
        self.bearer_token = "AAAAAAAAAAAAAAAAAAAAAId2hQAAAAAA%2FdwMtjcoVslqnTTt6DLa%2F5lMpXM%3DMTd4s71BHtAfSytoDdxhI5qmncuIuhb8WrOZftJTR4nLEdkfZA"
        self.base_url = "https://api.twitter.com/2/tweets/search/recent"
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}" if self.bearer_token else None,
            "Content-Type": "application/json"
        }
    
    def _validate_token(self) -> bool:
        """Check if Bearer Token is configured properly."""
        return self.bearer_token and self.bearer_token != 'your_bearer_token_here' and self.bearer_token != ''
    
    def run(self, domain: str) -> List[Dict[str, str]]:
        """
        Search X.com for recent tweets containing the domain keyword.
        
        Args:
            domain (str): The domain keyword to search for
            
        Returns:
            List[Dict[str, str]]: List of dictionaries with 'source' and 'content' keys
        """
        if not self._validate_token():
            return [{
                "source": "X.com", 
                "content": "Error: Twitter Bearer Token not configured. Please set TWITTER_BEARER_TOKEN environment variable in your .env file."
            }]
        
        try:
            # Set up query parameters
            params = {
                'query': domain,
                'max_results': 10,
                'tweet.fields': 'text,created_at,public_metrics'
            }
            
            # Make API request
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # Handle different HTTP status codes
            if response.status_code == 200:
                data = response.json()
                
                # Check if we have tweets in the response
                if 'data' in data and data['data']:
                    tweets = []
                    for tweet in data['data']:
                        tweets.append({
                            "source": "X.com",
                            "content": tweet['text']
                        })
                    return tweets
                else:
                    # No tweets found
                    return [{
                        "source": "X.com",
                        "content": f"No posts found for domain {domain}"
                    }]
            
            elif response.status_code == 401:
                return [{
                    "source": "X.com",
                    "content": "Error: Unauthorized - Invalid Bearer Token or insufficient permissions"
                }]
            
            elif response.status_code == 429:
                return [{
                    "source": "X.com",
                    "content": "Error: Rate limit exceeded - Please try again later"
                }]
            
            elif response.status_code == 400:
                return [{
                    "source": "X.com",
                    "content": f"Error: Bad request - Invalid query parameters for domain '{domain}'"
                }]
            
            elif response.status_code == 403:
                return [{
                    "source": "X.com",
                    "content": "Error: Forbidden - Access denied to Twitter API"
                }]
            
            else:
                return [{
                    "source": "X.com",
                    "content": f"Error: Twitter API returned status code {response.status_code}"
                }]
        
        except requests.exceptions.Timeout:
            return [{
                "source": "X.com",
                "content": "Error: Request timeout - Twitter API did not respond in time"
            }]
        
        except requests.exceptions.ConnectionError:
            return [{
                "source": "X.com",
                "content": "Error: Connection error - Unable to connect to Twitter API"
            }]
        
        except requests.exceptions.RequestException as e:
            return [{
                "source": "X.com",
                "content": f"Error: Request failed - {str(e)}"
            }]
        
        except ValueError as e:
            return [{
                "source": "X.com",
                "content": f"Error: Invalid JSON response - {str(e)}"
            }]
        
        except Exception as e:
            return [{
                "source": "X.com",
                "content": f"Unexpected error: {str(e)}"
            }]


if __name__ == "__main__":
    agent = XComScraperAgent()
    results = agent.run("Drupal")
    for tweet in results:
        print(tweet)