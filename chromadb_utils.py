
"""
Module: chromadb_utils.py

Description:
    Handles all ChromaDB-related functionality, including
    add, update, delete, query, and list operations.

Author: Shreyash Chavare
Created: 2025-12-26
"""

import chromadb
import os
import streamlit as st

from embedding import embedding
from pdf_utils import pdf_utils
from dotenv import load_dotenv


load_dotenv()


class chromadb_utils:

    def __init__(self):
        # Create client
        chroma_db_path = os.getenv("CHROMA_DB_PATH", "./resume_rag")
        self.__db = chromadb.PersistentClient(path=chroma_db_path)

        # Create collection
        self.__collection = self.__db.get_or_create_collection(
            name="resumes"
        )

        self.__embedder = embedding()

    # ================= Add all PDFs from directory =================
    def add_resumes_in_db(self, dir_path):
        try:
            if not dir_path or not os.path.isdir(dir_path):
                raise ValueError("Invalid directory path")

            result = self.__embedder.embedding_of_resumes(
                dir_path=dir_path
            )

            if result is None:
                return False

            embeddings, metadatas, ids = result

            if not ids:
                return False

            # Add directory information to metadata
            for meta in metadatas:
                meta["source_dir"] = os.path.basename(
                    os.path.normpath(dir_path)
                )

            self.__collection.upsert(
                ids=ids,
                embeddings=embeddings.tolist()
                if hasattr(embeddings, "tolist")
                else embeddings,
                metadatas=metadatas
            )

            return True

        except Exception as e:
            st.write(
                f"❌ Error while adding resumes from directory: {e}"
            )
            return False

    # ================= Query processing =================
    def query_processing(self, query):
        try:
            if not query or not query.strip():
                return None

            collection_count = self.__collection.count()

            if collection_count == 0:
                return None

            query_embed = self.__embedder.query_embedding(
                query=query
            )

            results = self.__collection.query(
                query_embeddings=[
                    query_embed.tolist()
                    if hasattr(query_embed, "tolist")
                    else query_embed
                ],
                n_results=min(3, collection_count)
            )

            return results

        except Exception as e:
            st.write(f"Query error: {e}")
            return None

    # ================= Add single resume =================
    def add_resume_in_db(self, pdf_path):
        try:
            result = self.__embedder.embedding_of_resume(
                pdf_path=pdf_path
            )

            if result is None:
                return False

            vector, metadata, resume_id = result

            self.__collection.upsert(
                ids=[resume_id],
                metadatas=[metadata],
                embeddings=[
                    vector.tolist()
                    if hasattr(vector, "tolist")
                    else vector
                ]
            )

            return True

        except Exception as e:
            st.write(f"Error occurred while adding resume: {e}")
            return False

    # ================= Update single resume =================
    def update_resume_in_db(self, pdf_path):
        try:
            result = self.__embedder.embedding_of_resume(
                pdf_path=pdf_path
            )

            if result is None:
                return False

            vector, metadata, resume_id = result

            self.__collection.upsert(
                ids=[resume_id],
                metadatas=[metadata],
                embeddings=[
                    vector.tolist()
                    if hasattr(vector, "tolist")
                    else vector
                ]
            )

            return True

        except Exception as e:
            st.write(f"Error occurred while updating resume: {e}")
            return False

    # ================= Delete resume from database =================
    def delete_resume_in_db(self, pdf_path):
        try:
            if not pdf_path:
                return False

            result = self.__collection.get(
                where={"pdf_path": pdf_path}
            )

            ids = result.get("ids", [])

            if not ids:
                return False

            # Delete all records associated with this PDF path.
            self.__collection.delete(ids=ids)

            # Do not delete the original PDF file here.
            return True

        except Exception as e:
            st.write(f"Delete error: {e}")
            return False

    # ================= List resumes =================
    def list_resume_in_db(self):
        try:
            data = self.__collection.get(
                include=["metadatas"]
            )

            rows = []

            for i, meta in enumerate(
                data.get("metadatas") or []
            ):
                if not meta:
                    continue

                rows.append({
                    "S.No": len(rows) + 1,
                    "PDF Name": meta.get("pdf_name"),
                    "Candidate": meta.get("person_name"),
                    "Uploaded At": meta.get("upload_date")
                })

            return rows

        except Exception as e:
            st.write(f"Error while listing resumes: {e}")
            return []

    # ================= Process DB query and reload PDFs =================
    def result_processing_for_the_query(self, query):
        try:
            result = self.query_processing(query=query)

            if not result:
                return []

            metadata_groups = result.get("metadatas") or [[]]

            if not metadata_groups:
                return []

            metadatas = metadata_groups[0] or []

            pdf_results = []
            pdf_reader = pdf_utils()

            for meta in metadatas:
                if not meta:
                    continue

                pdf_path = meta.get("pdf_path")
                pdf_name = meta.get("pdf_name")
                person_name = meta.get("person_name")

                if not pdf_path:
                    continue

                documents = pdf_reader.pdf_reading(pdf_path)

                if not documents:
                    continue

                pdf_results.append({
                    "pdf_name": pdf_name,
                    "pdf_path": pdf_path,
                    "person_name": person_name,
                    "documents": documents
                })

            return pdf_results

        except Exception as e:
            st.write(
                f"Error while processing query results: {e}"
            )
            return []
