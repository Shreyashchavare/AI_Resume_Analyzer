"""
Module: chromadb_utils.py

Description:
    Handles all ChromaDB-related functionality, including add, update, delete, and list operations.

Author: Shreyash Chavare
Created: 2025-12-26
"""


# Import all neccessary modules
import chromadb
import os
import streamlit as st
# devloper defined modules
from embedding import embedding
from pdf_utils import pdf_utils

class chromadb_utils:
    def __init__(self):
        # Create client 
        self.__db = chromadb.PersistentClient("./resume_rag")

        #Create collection
        self.__collection = self.__db.get_or_create_collection("resumes")

        self.__embedder = embedding()

    # ====================================== add_all_folders_of_dir ==============================
    def add_resumes_in_db(self, dir_path):
        """
        Docstring for add_pdfs_in_vector
        This function add all pdf datas vectors to the Chroma DB ,
        but if update is neccessary then this is not ideal function.
        
        :param dir_path: path of directory where all pdf are present.
        :return True/False: return true if data added.
        """
        
        try:
            if not dir_path or not os.path.isdir(dir_path):
                raise ValueError("Invalid directory path")

            # Generate embeddings
            embeddings, metadatas, ids = self.__embedder.embedding_of_resumes(
                dir_path=dir_path
            )

            # Add directory info to metadata
            for meta in metadatas:
                meta["source_dir"] = os.path.basename(dir_path)

            # Upsert into ChromaDB
            self.__collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metadatas
            )

            return True

        except Exception as e:
            st.write(f"❌ Error while adding resumes from directory: {e}")
            return False


    # ====================================== query_processing ==============================

    def query_processing(self, query):
        """
        Docstring for query_processing
        This function process the text query and returns result
        :param query: text query
        :return: result of query
        """

        try:
            query_embed = self.__embedder.query_embedding(query=query)
            results = self.__collection.query(query_embeddings=[query_embed], n_results= 3)
            return results
        except Exception as e:
            st.write(e)
            return None
    
    # ================== Add Single Resume =========================================
    def add_resume_in_db(self, pdf_path):
        """
        Docstring for add_resume_in_db
        
        :param self: Description
        :param pdf_path: Description
        """
        
        try:
            # Get embedding and information of resume pdf
            embeddings, metadatas, ids = self.__embedder.embedding_of_resume(pdf_path=pdf_path)
            # adding vector in DB
            self.__collection.upsert(ids=ids, metadatas=metadatas, embeddings=embeddings) 
            return True
        except Exception as e:
            st.write(f"Error occured while adding resume pdf: {e}")
            return None
        
    # ================== Add Single Resume =========================================
    def update_resume_in_db(self, pdf_path):
        """
        Docstring for update_resume_in_db
        
        :param self: Description
        :param pdf_path: Description
        """
        
        try:
            # Get embedding and information of resume pdf
            embeddings, metadatas, ids = self.__embedder.embedding_of_resume(pdf_path=pdf_path)
            # updating vector in DB           
            self.__collection.upsert(ids=ids, metadatas=metadatas, embeddings=embeddings) 
            return True
        except Exception as e:
            st.write(f"Error occured while adding resume pdf: {e}")
            return None

    # ================== Delete Selected Resumes from OS and DB ==================================
    def delete_resume_in_db(self, pdf_path):
        try:
            resume_id = self.__embedder._make_id(pdf_path)
            self.__collection.delete(ids=[resume_id])

            if os.path.exists(pdf_path):
                os.remove(pdf_path)

            return True
        except Exception as e:
            st.write(f"Delete error: {e}")
            return False


    # =============== Show all the resume list with name, id, pdf name,serial ====================
    def list_resume_in_db(self):
        data = self.__collection.get(include=["metadatas"])
        rows = []

        for i, meta in enumerate(data.get("metadatas", [])):
            rows.append({
                "S.No": i + 1,
                "PDF Name": meta.get("pdf_name"),
                "Candidate": meta.get("person_name"),
                "Uploaded At": meta.get("upload_date")
            })

        return rows

    # ==============================
    # Process DB query → reload PDFs
    # ==============================

    def result_processing_for_the_query(self, query):
        try:
            result = self.query_processing(query=query)
            metadatas = result.get("metadatas", [[]])[0]

            pdf_results = []
            pdf_reader = pdf_utils()   # ✅ create instance ONCE

            for meta in metadatas:
                pdf_path = meta.get("pdf_path")
                pdf_name = meta.get("pdf_name")
                person_name = meta.get("person_name")

                if not pdf_path:
                    continue

                docs = pdf_reader.pdf_reading(pdf_path)  # ✅ FIX
                if not docs:
                    continue

                pdf_results.append({
                    "pdf_name": pdf_name,
                    "pdf_path": pdf_path,
                    "person_name": person_name,
                    "documents": docs
                })

            return pdf_results

        except Exception as e:
            st.write(f"Error while result processing from db: {e}")
            return []
