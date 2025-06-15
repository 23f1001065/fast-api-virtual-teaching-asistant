import os
import httpx
from google import genai
from tools import load_json, save_json

GENAI_API_KEY = os.getenv('GENAI_API_KEY')
client = genai.Client(api_key=GENAI_API_KEY)
def get_image_description(image_path):
    im_extension = image_path.split('.')[-1].lower()
    image_bytes = httpx.get(image_path).content
    image = genai.types.Part.from_bytes(
        data=image_bytes, mime_type=f"image/{im_extension}"
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image , "Generate text description of this image."],
        )
    except Exception as e:
        print(f"Error generating image description: {e}")
        return
    return response


def main():
    data = load_json('jan_to_april_posts_with_@user.json')
    if not data:
        print("No data found in the JSON file.")
        return
    all_posts_with_image_description = []
    count = 1
    total_img = sum(len(post['image_urls']) for post in data['posts'])
    print(f"Total number of images to process: {total_img}")
    print("Starting to process posts for image descriptions...")
    for post in data['posts']:
        image_description = []
        if len(post['image_urls']) > 0:
            for image_url in post['image_urls']:
                try:
                    print(f"({count}|{total_img}) Processing image: {image_url}")
                    response = get_image_description(image_url)
                    if response and response.text:
                        image_description.append({
                            'image_url': image_url,
                            'description': response.text
                        })
                except Exception as e:
                    print(f"Error processing image {image_url}: {e}")
                    return
                else:
                    print(f"Image description for {image_url} added successfully.")
        all_posts_with_image_description.append({
            'post_text': post['content'],
            'image_description': image_description,
            "post_url" : post['post_url']
        })
    save_json('all_posts_with_image_description.json', all_posts_with_image_description)

if __name__ == "__main__":
    main()
    print("Image descriptions have been successfully generated and saved.")