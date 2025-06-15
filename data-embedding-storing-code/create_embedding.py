import os, sys
# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_sourcing_preprocessing.tools import load_json, save_json

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
model = SentenceTransformer('all-MiniLM-L6-v2')
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def create_chunks_by_tokens(text,max_tokens=250,overlap=50):
    """
    Create chunks of text with a specified size and overlap.
    
    Args:
        text (str): The input text to be chunked.
        max_tokens (int): The size of each chunk.
        overlap (int): The number of overlapping characters between chunks.
        
    Returns:
        list: A list of text chunks.
    """
    input_ids = tokenizer.encode(text, add_special_tokens=False)
    chunks = []
    start = 0
    while start < len(input_ids):
        end = min(start + max_tokens, len(input_ids))
        chunk = input_ids[start:end]
        chunks.append(tokenizer.decode(chunk, skip_special_tokens=True))
        start += (max_tokens - overlap)
    return chunks,len(input_ids)

def create_embedding(chunks):
    """
    Create an embedding for the given text data.
    Args:
        List: chunks -- The text chunks to create an embedding for
    Return:
        List: The created embedding
    """


    # Your code to create an embedding from the data
    embeddings = model.encode(chunks, precision='float32',)
    embedding_dic = []
    for chunk, embedding in zip(chunks, embeddings):
        embedding_dic.append((chunk, embedding))

    return embedding_dic



def create_embeddings_from_file(course_file_path, post_file_path, first_n_post=None, first_n_course=None):
    course_data = load_json(course_file_path)
    post_data = load_json(post_file_path)
    count = 1
    total_post = len(post_data)
    
    if not first_n_post and not first_n_course:
        first_n_post = total_post
        first_n_course = course_data['count']
    else:
        if not first_n_post and first_n_post:
            first_n_post = total_post
        elif first_n_post and not first_n_course:
            first_n_course = course_data['count']


    data_with_embeddings = []
    post_data_embeddings = []
    course_data_embeddings = []
    
    for post in post_data[:first_n_post]:
        all_text = post["post_text"]
        for image_desc in post["image_description"]:
            all_text = all_text + " " + image_desc["description"]


        chunks,tokens = create_chunks_by_tokens(all_text)
        print(f"* Processing post {count} with text length {tokens}...")
        embeddings = create_embedding(chunks)

        post_data_embeddings.append({
            "id": count,
            "embedding": embeddings,
            "text": post["post_text"],
            "url": post["post_url"]
        })
        print(f">>> Successfully Processed post {count} .")
        count += 1
    
    for course in course_data["contents"][:first_n_course]:
        chunks,tokens = create_chunks_by_tokens(course["text"])
        print(f"Processing course {count} with text length {tokens}...")
        course_data_embeddings.append({
            "id": count,
            "embedding": create_embedding(chunks),
            "text": course["text"],
            "url": course["url"]
        })
        print(f">>> Successfully Processed course {count} .")
        count += 1
    
    data_with_embeddings = {
        "posts": post_data_embeddings,
        "courses": course_data_embeddings,
        "count": count-1
    }

    #save_json("data_with_embeddings.json",data_with_embeddings)
    print("Embeddings created successfully.")
    return data_with_embeddings

    