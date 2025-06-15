from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, BLOB
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session


Base = declarative_base()

class Document(Base):
    __tablename__ = 'document_table'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    url = Column(String, nullable=True)
    
    chunks = relationship("Chunk", back_populates="document")

class Chunk(Base):
    __tablename__ = 'chunk_table'

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('document_table.id'))
    chunk_text = Column(Text, nullable=False)
    embedding = Column(BLOB, nullable=False)

    document = relationship("Document", back_populates="chunks")