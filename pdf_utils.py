"""
Module: pdf_utils.py

Description:
    Handles PDF reading and parsing, including text extraction.

Author: Shreyash Chavare
Created: 2025-12-26
"""
"""
Module: pdf_utils.py

Description:
    Handles PDF reading and parsing using LangChain loaders.
    Reloads PDFs using metadata returned from ChromaDB.

Author: Shreyash Chavare
Created: 2025-12-26
"""

import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from typing import cast

class pdf_utils:

    # ==============================
    # Read all PDFs from a directory
    # ==============================
    def dir_pdfs_reading(self, dir_path):
        try:
            if not dir_path or not os.path.isdir(dir_path):
                raise ValueError("Invalid directory path")

            loader = DirectoryLoader(
                path=dir_path,
                glob="**/*.pdf",
                loader_cls=cast(type, PyPDFLoader)
            )

            documents = loader.load()

            if not documents:
                print("No readable PDF documents found in directory")
                return None

            return documents

        except Exception as e:
            print(f"Error while parsing directory: {e}")
            return None

        # ==============================
    # Read a single PDF using path
    # ==============================
    def pdf_reading(self, pdf_path):
        try:
            if not pdf_path or not os.path.isfile(pdf_path):
                raise FileNotFoundError(
                    f"PDF not found: {pdf_path}"
                )

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

            if not documents:
                print("No readable content found in PDF")
                return None

            return documents

        except Exception as e:
            print(f"Error while parsing PDF: {e}")
            return None