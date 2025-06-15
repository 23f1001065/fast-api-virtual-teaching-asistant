import json
import httpx
import os 

def load_json(file_path):
    """Load a JSON file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def fetch_topics_from_discourse(url,cookie):
  response = httpx.get(
      url,
      headers={
        "User-Agent" : "Thunder Client (https://www.thunderclient.com)",
        "Accept" : "*/*",
        "Cookie" : cookie
      }
  )
  return response

def fetch_posts_from_discourse(url,cookie):
  response = httpx.get(
      url,
      headers={
        "User-Agent" : "Thunder Client (https://www.thunderclient.com)",
        "Accept" : "*/*",
        "Cookie" : cookie
      }
  )
  return response