"""
Module: embedding.py

Description:
    Handles all embedding-related functionality, including embedding generation and management.

Author: Shreyash Chavare
Created: 2025-12-26
"""


# Import neccessary modules
from sentence_transformers import SentenceTransformer
import os
from collections import defaultdict
from datetime import date

# Import neccessary modules
from pdf_utils import pdf_utils
# class: embedding
class embedding:
    def __init__(self):
        # embedding model 
        self.__embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # ============================= embedding_of_resume ==================================
    def embedding_of_resumes(self, dir_path):
        """
        Docstring for embedding_of_resume
        embedding_of_resumes function is used create vector embedding for give directory path of pdfs
        :param dir_path: directory path of pdfs where all pdf are present 
        :return: 
                embeddings: vector of pdf 
                metadatas: metadata of pdf
                ids: ids for vectors of pdf
        """

        try:
            pdf = pdf_utils()
            documents = pdf.dir_pdfs_reading(dir_path)
        except Exception as e:
            print(f"Error while reading directory: {e}")
            return None

        metadatas = []
        pdf_texts = defaultdict(str)
        pdf_paths = {}
        ids = []

        # Collect text per PDF
        for doc in documents:
            pdf_path = doc.metadata["source"]              # ✅ full path
            pdf_name = os.path.basename(pdf_path)

            pdf_texts[pdf_name] += doc.page_content + "\n\n"
            pdf_paths[pdf_name] = pdf_path                 # map name → path

        texts = []

        for pdf_name, text in pdf_texts.items():
            texts.append(text)

            base_name = os.path.splitext(pdf_name)[0]
            words = base_name.split()
            person_name = " ".join(words[:2]) if len(words) >= 2 else base_name

            metadatas.append({
                "pdf_name": pdf_name,
                "pdf_path": pdf_paths[pdf_name],   # ✅ added
                "person_name": person_name,
                "upload_date": str(date.today())
            })

            ids.append(f"{pdf_name}/{person_name}/{date.today()}")

        embeddings = self.__embed_model.encode(texts)

        return embeddings, metadatas, ids

    # ============================= query_embedding ==================================
    def query_embedding(self, query):
        """
        Docstring for query_embedding
        query_embedding function used only for creating vector embedding of query
        :param query: Text query
        :return: Embedded vector
        """
        return self.__embed_model.encode(query)
    
    # ============================= embedding_of_resume ==================================
    def embedding_of_resume(self, pdf_path):
        """
        Docstring for embedding_of_resume
        
        :param self: self is passed for class parameters
        :param pdf_path: pdf path of the resume
        :return:
            embedding: embedding of the resume
            metadata: metadata of the resume 
            id: id for the resume
        """
        try:
            pdf = pdf_utils()
            documents = pdf.pdf_reading(pdf_path)
        except Exception as e:
            print(f"Error while reading PDF: {e}")
            return None

        pdf_text = ""

        for doc in documents:
            pdf_text += doc.page_content + "\n\n"

        # Extract metadata from first page (same for all pages)
        source_path = documents[0].metadata["source"]
        pdf_name = os.path.basename(source_path)

        base_name = os.path.splitext(pdf_name)[0]
        words = base_name.split()
        person_name = " ".join(words[:2]) if len(words) >= 2 else base_name

        metadata = {
            "pdf_name": pdf_name,
            "pdf_path": source_path,          # ✅ added
            "person_name": person_name,
            "upload_date": str(date.today())
        }

        id = f"{pdf_name}/{person_name}/{date.today()}"

        embedding = self.__embed_model.encode(pdf_text)

        return embedding, metadata, id