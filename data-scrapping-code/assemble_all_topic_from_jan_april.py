# assemble_from_jan_april.py
from tools import load_json, save_json
from datetime import datetime
starting_timestamp_str = "2025-01-01T00:00:00.000Z"
ending_timestamp_str = "2025-04-14T23:59:59.000Z"

starting_timestamp = datetime.strptime(starting_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
ending_timestamp = datetime.strptime(ending_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

def assemble_jan_april(input_file, output_file):
    all_topics = load_json(input_file)
    jan_april_topics = [topic 
                        for topic in all_topics['topics'] 
                        if starting_timestamp <= datetime.strptime(topic['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ") <= ending_timestamp
    ]
    total_posts = sum(topic['posts_count'] for topic in jan_april_topics)
    print(f"Total posts from January to April: {total_posts}")
    print(f"Total topics from January to April: {len(jan_april_topics)}")
    # Save the filtered topics to the output file
    data = {
        "topic_count": len(jan_april_topics),
        "post_count": total_posts,
        "topics": jan_april_topics
    }
    save_json(output_file, data)



if __name__ == "__main__":
    input_file = "all_topics.json"
    output_file = "jan_april_topics.json"
    assemble_jan_april(input_file, output_file)
    print(f"Topics from January to April have been assembled and saved to {output_file}.")