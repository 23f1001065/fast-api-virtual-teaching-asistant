from tools import fetch_topics_from_discourse,save_json
import os 

Discourse_forum_Cookie = os.environ.get('DFC')
for page in range(0,7):
    try :
        url = f"https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34.json?page={page}"
        response = fetch_topics_from_discourse(url, Discourse_forum_Cookie)
    except Exception as e:
        print(f"An error occurred while fetching topics from page {page} : {e}")
    else:
        if response.status_code == 200:
            save_json(f"tds-kb_34_page={page}.json", response.json())
        else:
            print(f"Failed to fetch topics from page {page}. Status code: {response.status_code}")
    
