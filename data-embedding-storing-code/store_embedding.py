"""
Document_table():
    id : int (primary key)
    content : str
    url: str
    chunks = relation to Chunk_table

Chunk_table():
    id : int (primary key)
    document_id: int (foreign key to Document_table)
    chunk_text : str
    embedding : list (float)
    document : relation to Document_table
"""



import numpy as np
from create_embedding import *
from model import Base, Document, Chunk, create_engine, sessionmaker




if __name__ == "__main__":
    engine = create_engine('sqlite:///vector_store_float32.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine) 
    db = Session()
    print("Database and tables created successfully.")


    course_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_sourcing_preprocessing', 'jan_2025_course_data.json')
    post_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_sourcing_preprocessing', 'all_posts_with_image_description.json')

    data_with_embeddings = create_embeddings_from_file(course_file_path, post_file_path)
    print("Storing embeddings in the database.....................")
    
    try:
        for post in data_with_embeddings['posts']:
            document = Document(content=post['text'], url=post['url'])
            db.add(document)
            db.flush()  # Ensure the document is added and has an ID
            chunk_entry = []
            for chunk, embedding in post['embedding']:
                chunk_entry.append(
                    Chunk(document_id=document.id, chunk_text=chunk, embedding=np.array(embedding,dtype=np.float32).tobytes())
                )
            db.add_all(chunk_entry)
        db.commit()
        
        for course in data_with_embeddings['courses']:
            document = Document(content=course['text'], url=course['url'])
            db.add(document)
            db.flush()  # Ensure the document is added and has an ID
            chunk_entry = []
            for chunk, embedding in course['embedding']:
                chunk_entry.append(
                    Chunk(document_id=document.id, chunk_text=chunk, embedding=np.array(embedding,dtype=np.float32).tobytes())
                )
            db.add_all(chunk_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    else:
        print("Embeddings stored successfully in the database.")
    finally:
        db.close()
        
    