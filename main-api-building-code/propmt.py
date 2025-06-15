import os
API_KEY = os.getenv("AIPIPE_API_TOKEN")
def define_prompt(context,query):
    url = "https://aipipe.org/openrouter/v1/chat/completions"
    headers = {
        "Content-Type" : "application/json",
        "Authorization" : "Bearer" + API_KEY
    }
    prompt = f"""You are answering a question based on the following retrieved context: \n {context}\n
    Given this information, please answer the following question clearly and thoroughly, assuming the reader is a student in a Data Science tools course:\n
    {query}

    """
    json = {
        "model" : "gpt-4o-mini",
        "messages" : [
            {
                "role" : "system",
                "content" : "You are a Teaching Instructor of Tools in Data Science Course."
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ]
    }
    return url,headers,json

    
