"""
Module: llm.py

Description:
    Handles all functionality related to llm and its all prompts.

Author: Shreyash Chavare
Created: 2025-12-26
"""


# import all neccessary modules
from langchain.chat_models import init_chat_model
from chromadb_utils import chromadb_utils
import streamlit as st

class llm:
    def __init__(self):
        self.__llm = init_chat_model(
        model="google/gemma-3-4b",
        model_provider="openai",
        base_url="http://localhost:1234/v1",
        api_key="non-needed"
        )
        self.__conversation = []

        self.__MAX_TURNS = 5

        self.__resume_context_added = False


        self.__SYSTEM_PROMPT = """
            ROLE:
            You are an experienced HR analyst with expertise in resume screening and job–candidate matching.

            OBJECTIVE:
            Analyze the provided resumes (PDFs) and compare them ONLY with the provided job description.
            Identify the most suitable candidate based strictly on the given data.

            STRICT DATA USAGE RULE (VERY IMPORTANT):
            - Use ONLY the information explicitly present in the provided resumes and job description.
            - Do NOT assume, infer, guess, or add any new skills, experience, roles, or details.
            - Do NOT use general knowledge or external information.
            - If required information is missing, treat it as NOT PRESENT.

            RULES:
            - Carefully analyze each provided resume.
            - Match resumes strictly against the provided job description.
            - Select the MOST relevant profile based only on available data.
            - Use simple and clear English.
            - Be unbiased and factual.
            - If no resume sufficiently matches the job description, return EXACTLY:
            "No matching profile for this job"

            ANSWER FLOW (STRICT FORMAT — DO NOT CHANGE):
            pdf name:
            Name:
            Summary:
            Reason of selection:
            Note:

            FIELD GUIDELINES:
            - pdf name:
            Name of the resume file used for selection.

            - Name:
            Full name as mentioned in the resume.

            - Summary:
            Short summary using ONLY resume content relevant to the job.

            - Reason of selection:
            Reasons based ONLY on direct matches between resume data and job requirements.

            - Note:
            Explain why this profile was selected over others,
            based strictly on missing skills, weaker alignment, or gaps found in other resumes.

            CONSTRAINTS:
            - Do not add explanations outside the defined format.
            - Do not include assumptions or hypothetical statements.
            - Keep the response concise and professional.
            """



    def __trim_conversation(self):
        """
        Keeps:
        - system prompt
        - resume context
        - last N user/assistant turns
        """

        system_msgs = []
        chat_msgs = []

        for msg in self.__conversation:
            if msg["role"] == "system":
                system_msgs.append(msg)
            else:
                chat_msgs.append(msg)

        # Each turn = user + assistant
        max_msgs = self.__MAX_TURNS * 2

        trimmed_chat = chat_msgs[-max_msgs:]

        self.__conversation = system_msgs + trimmed_chat


    def user_llm_prompts_interaction(self, user_input):

        if not self.__conversation:
            self.__conversation.append({
                "role": "system",
                "content": self.__SYSTEM_PROMPT
            })

        if not self.__resume_context_added:
            db = chromadb_utils()
            results = db.result_processing_for_the_query(user_input)

            if not results:
                resume_context = "NO RESUME DATA FOUND"
            else:
                resume_texts = []

                for item in results:
                    pages_text = "\n".join(
                        doc.page_content for doc in item["documents"]
                    )

                    resume_texts.append(pages_text)

                resume_context = "\n\n".join(resume_texts)

            self.__conversation.append(
                {
                    "role": "system",
                    "content": f"Resume Context:\n{resume_context}"
                })

            self.__resume_context_added = True

        # Add user input
        self.__conversation.append({
            "role": "user",
            "content": user_input
        })

        # 🔥 Trim conversation BEFORE invoking LLM
        self.__trim_conversation()

        response = self.__llm.invoke(self.__conversation)

        self.__conversation.append({
            "role": "assistant",
            "content": response.content
        })

        return response.content

                
    def display_chat(self):
        """
        Displays chat history cleanly.
        Shows only user and assistant messages.
        Hides system context (RAG data, prompts).
        """

        for msg in self.__conversation:
            role = msg.get("role")
            content = msg.get("content")

            if role == "user":
                st.write(f"\n🧑 User:\n{content}")

            elif role == "assistant":
                st.write(f"\n🤖 Assistant:\n{content}")

    def clear_chat(self):
        self.__conversation = []
        self.__resume_context_added = False
