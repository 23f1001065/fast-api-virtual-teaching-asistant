import glob
from tools import load_json, save_json

def assemble_all_topics(output_file):
    """Assemble all topics from the input JSON file and save to the output file."""
    input_files = glob.glob("tds-kb_34_page*.json")  # Adjust the pattern as needed
    all_topics = []
    total_topics = 0
    for input_file in input_files:
        data = load_json(input_file)

        for topic in data["topic_list"]["topics"]:
            edited_topic = {
                "id": topic["id"],
                "title": topic["title"],
                "slug": topic["slug"],
                "posts_count": topic["posts_count"],
                "created_at": topic["created_at"],
                "last_posted_at": topic["last_posted_at"],
                "reply_count": topic["reply_count"]
            }
            total_topics += 1
            all_topics.append(edited_topic)

    # Remove duplicates by converting to a set and back to a list
    unique_topics = list({topic['id']: topic for topic in all_topics}.values())
    print(f"Total topics processed: {total_topics}")
    print(f"Unique topics found: {len(unique_topics)}")

    data = {
        "topics": unique_topics,
        "count": len(unique_topics)
    }
    # Save the unique topics to the output file
    save_json(output_file, data)

if __name__ == "__main__":
    output_file = "all_topics.json"
    assemble_all_topics(output_file)
    print(f"All topics have been assembled and saved to {output_file}.")