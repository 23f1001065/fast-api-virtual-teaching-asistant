from tools import load_json, save_json, fetch_posts_from_discourse
from math import ceil
import re
def parse_tds_post(cooked_html: str):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(cooked_html, 'html.parser')
    #text = soup.get_text(strip=True)  # text of the post
    text = re.sub(r"@\w+","",soup.get_text(" ", strip=True))
    image_urls = []                  # if the post contains any image
    for a in soup.find_all('a', class_='lightbox'):
        if 'href' in a.attrs:
            image_urls.append(a['href'])

    #if not image_urls:
        #image_urls = [img['src'] for img in soup.find_all('img') if 'src' in img.attrs]

    return text, image_urls

def make_edited_post_data(response_object):
    all_edited_post = []
    for post in response_object.json()["post_stream"]["posts"]:
        text, image_urls = parse_tds_post(post["cooked"])
        if not text:
            continue
        post_object = {
            "content" : text,
            "image_urls" : image_urls,
            "created_at" : post["created_at"],
            "post_url" : "https://discourse.onlinedegree.iitm.ac.in" + post["post_url"],
            "link_count" : [link["url"] for link in post["link_counts"]] if "link_counts" in post.keys() else [] ,
            "from_topic_name" : post["topic_slug"]
        }
        all_edited_post.append(post_object)
    return all_edited_post



def extract_all_posts(input_file, output_file, dfc):
    """Extract all posts from topics in the input file and save them to the output file."""
    data = load_json(input_file)
    all_edited_posts = []
    count = 0
    topic_count = data["topic_count"]
    print(f"Total topics to process: {topic_count}")
    print(f"Total posts to process: {data['post_count']}")
    print(f"Starting extraction of posts from {input_file}...",end="\n\n")
    for topic in data['topics']:
        topic_id = topic['id']
        topic_slug = topic['slug']
        posts_count = topic['posts_count']
        pages = ceil(topic['posts_count'] / 20)  # Assuming 20 posts per page
        count = count + 1
        print(f"({count}/{topic_count}) Fetching {posts_count} posts for topic ID {topic_id} with slug '{topic_slug}', across {pages} pages....")
        for page in range(1, pages + 1):
            try:
                url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_slug}/{topic_id}.json?page={page}"  # Replace with actual URL
                response = fetch_posts_from_discourse(url, dfc) ####### fetching posts
            except Exception as e:
                print(f"An error occurred while fetching posts for topic ID {topic_id}: {e} on page {page}")
                return
            else:
                if response.status_code == 200:
                    posts = make_edited_post_data(response)
                    all_edited_posts.extend(posts)
                else:
                    print(f"Failed to fetch posts for topic ID {topic_id}: {response.status_code}")
        print(f">>> Successfully fetched {posts_count} posts from topic ID {topic_id}.")
    # Save the extracted posts to the output file
    save_json(output_file, {"posts": all_edited_posts, "count": len(all_edited_posts)})
    print(f"Extracted {len(all_edited_posts)} posts and saved to {output_file}.")



if __name__ == "__main__":
    import os 
    Discourse_site_cookie = os.environ.get('DFC')
    input_file = "jan_april_topics.json"
    output_file = "jan_to_april_posts.json"
    extract_all_posts(input_file, output_file, Discourse_site_cookie)
    print(f"Posts from January to April have been extracted and saved to {output_file}.")
    # This script extracts all posts from topics in the specified input file and saves them to the output file.

