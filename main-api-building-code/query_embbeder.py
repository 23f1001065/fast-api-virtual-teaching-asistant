from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from ocr import *
import numpy as np
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
    return chunks

def query_embedding(query_body):
    """
    Create an embedding for the given text data.
    Args:
        List: chunks -- The text chunks to create an embedding for
    Return:
        List: The created embedding
    """
    if query_body.image:
        full_text = query_body.question + "\n" + get_image_ocr_from_genai(query_body.image) 
    else :
        full_text = query_body.question
    #print(full_text)
    
    chunks = create_chunks_by_tokens(full_text)
    if not chunks:
        raise ValueError("No valid text chunks to encode.")
    # Your code to create an embedding from the data
    embeddings = model.encode(chunks, precision='float32')
    #print(embeddings.shape)
    mean_embedding = np.mean(embeddings,axis=0).astype(np.float32)



    #print(mean_embedding)
    return mean_embedding