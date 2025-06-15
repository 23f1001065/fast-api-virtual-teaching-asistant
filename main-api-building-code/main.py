from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import httpx
import time 
from model import *
from propmt import *
from similarity_search import FAISS_SIMILARITY


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity; adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

engine = create_engine('sqlite:///vector_store_float16.db')
session = sessionmaker(bind=engine)
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
global fs
fs = FAISS_SIMILARITY(session())


class QueryRequest(BaseModel):
    question: str
    image: Optional[str] = None


@app.get("/")
def home():
    return {
        "message" : "Well come to my TDS project-1 on virtual Teaching Asistant"
    }

@app.post("/api")
def provide_answer(request_body: QueryRequest, db: Session = Depends(get_db)):
    start = time.time()
    try:
        similar_chunks = fs.find_similar_chunks(request_body)

    except Exception as e:
        print(e)
        return {
            "error" : str(e)
        }
    doc_ids = []
    for chunk_id, score in similar_chunks:
        chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
        if chunk:
            doc_ids.append((chunk.id, chunk.document_id, score))
    documents_similar = []
    for chunk_id, document_id, score in doc_ids:
        document = db.query(Document).filter(Document.id == document_id).first()
        documents_similar.append({
            "chunk_info" : f"chunk_id : {chunk_id}, score : {score:.4f}",
            "document_id" : document.id,
            "document_contents" : document.content,
            "url" : document.url
        })
        
    u_doc = {}
    for doc in documents_similar:
        if doc["document_id"] not in u_doc.keys():
            u_doc[doc["document_id"]] = doc
        else:
            pass

    
    context = "\n".join(u_doc[key]["document_contents"] for key in u_doc)

    url,headers,json = define_prompt(context,(request_body.question))

    response = httpx.post(url,headers=headers,json=json, timeout=30.00)
    print("Time taken:", time.time() - start)
    return {
        "answer" : response.json()["choices"][0]["message"]["content"],
        "links" : [{
            "url" : doc["url"],
            "text" : doc["document_contents"]
        } for doc in documents_similar]
    }

    

if __name__ == "__main__":
    import  uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

    