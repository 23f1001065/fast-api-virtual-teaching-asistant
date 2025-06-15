from model import  Chunk
from query_embbeder import query_embedding
from  sentence_transformers import SentenceTransformer
import numpy as np
import faiss



model = SentenceTransformer('all-MiniLM-L6-v2')


class FAISS_SIMILARITY:
    def __init__(self,db):
        self.db =db
        self.index = None 
        self.index = self.create_faiss_index()

    def load_vector_for_faiss(self):
        """
        Load all chunks from the database and prepare them for FAISS indexing.
        """
        chunks = self.db.query(Chunk).all()
        embeddings = []
        ids = []
        for chunk in chunks:
            embedding = np.frombuffer(chunk.embedding, dtype=np.float16)
            embeddings.append(embedding)
            ids.append(chunk.id)
        
        embeddings = np.vstack(embeddings,dtype=np.float32)  # Convert to float32 for FAISS
        print(embeddings.shape)
        return embeddings, ids

    def create_faiss_index(self):
        """
        Create a FAISS index from the embeddings loaded from the database.
        """
        if self.index is not None:
            return self.index
        embeddings, ids = self.load_vector_for_faiss()
        faiss.normalize_L2(embeddings)  # Normalize embeddings for cosine similarity
        dimension = embeddings.shape[1]
        self.index = faiss.IndexIDMap(faiss.IndexFlatIP(dimension))  # Use Inner Product for cosine similarity
        self.index.add_with_ids(embeddings, np.array(ids))
        return self.index
    
    def find_similar_chunks(self, query_body, top_k=5, threshold=0.0):
        """
        Find the top_k most similar chunks to the query_text using FAISS.
        """
        query_vector = query_embedding(query_body).reshape(1,-1)
        print("IN-FSC>>Query-vector shape before normalization: " , query_vector.shape)
        
        try:
            faiss.normalize_L2(query_vector)  # Normalize the query embedding again
        except:
            print("ERROR in >QUERY>NORMALIZATION inside find_similar_chunks function")
        else:
            print("ok")
        
        
        print("IN-FSC>>Query-vector-shape after normalization: " , query_vector.shape)
        try:
            D, I = self.index.search(query_vector, top_k)
        except Exception as e:
            raise ValueError("ERROR from find_similar_chunks function")

        similar_chunks = []
        for i,d in zip(I[0], D[0]):
            similar_chunks.append(
                (int(i),float(d))
            )
        return similar_chunks



class RAW_COSINE_SIMILARITY:
    def load_chunks_from_db(db):
        """
        Load all chunks from the database.
        """
        chunks = db.query(Chunk).all()
        chunks_data = []
        for chunk in chunks:
            embedding = np.frombuffer(chunk.embedding, dtype=np.float16)
            chunks_data.append({
                'id': chunk.id,
                'document_id': chunk.document_id,
                'embedding': embedding
            })
        return chunks_data

    def cosine_similarity(vec1, vec2):
        """
        Calculate the cosine similarity between two vectors.
        """

        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)

    def find_similar_chunks(query_body, top_k=5,threshold=0.0):
        """
        Find the top_k most similar chunks to the query_text.
        """
        query_vector = query_embedding(query_body)
        chunks = RAW_COSINE_SIMILARITY.load_chunks_from_db()

        similarity_scores = []
        for chunk in chunks:
            sim = RAW_COSINE_SIMILARITY.cosine_similarity(query_vector, chunk['embedding'])
            similarity_scores.append((chunk['id'], chunk['document_id'], sim))

        similarity_scores = list(filter(lambda x: x[2] >= threshold, similarity_scores))
        similarity_scores.sort(key=lambda x: x[2], reverse=True)

        return similarity_scores[:top_k]




