import httpx, base64, imghdr
import os 
from google import genai

def detect_mime_from_base64(image_bytes):
    # image_bytes = base64.b64decode(b64_string)       if bs64 character encoding provided, it convert to binary.
    ext = imghdr.what(None, h=image_bytes)
    return f"image/{ext}" if ext else "application/octet-stream"
    

aipipe_token = os.getenv("AIPIPE_API_TOKEN")
def get_image_ocr_from_aipipe(image_uri):
    """sumary_line
    
    Keyword arguments:
    image_uri --  base64 character encoded data[string]
    Return: text_description[string]
    """
    
    url = "https://aipipe.org/openai/v1/chat/completions"
    response = httpx.post(
        url,
        headers={
        "Authorization" : "Bearer "+aipipe_token,
        "Content-Type" : "application/json"
        },
        json={
        "model" : "gpt-4o-mini",
        "messages" : [
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : "Extract text from this image."
                    },
                    {
                        "type" : "image_url",
                        "image_url" : {
                            "url" : "data:image/jpg;base64," + image_uri    # this model need only base64 character encoded data
                        }
                    }
                ]
            }
        ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]





GENAI_API_KEY = os.getenv('GENAI_API_KEY')
def get_image_ocr_from_genai(image_uri):
    """sumary_line
    
    Keyword arguments:
    image_uri --  base64 character encoded data[string]
    Return: text_description[string]
    """
    client = genai.Client(api_key=GENAI_API_KEY)
    try:
        # this model needs binary image data
        image_bytes = base64.b64decode(image_uri)
        mime_type = detect_mime_from_base64(image_bytes)
        # You can adjust the mime_type if it's not png
        image_part = genai.types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[image_part , "Generate OCR of this image. and give as plain text for further vector embedding"],
        )
    except Exception as e:
        raise ValueError(f"Error generating image description: {e}")
        
    return response.text

