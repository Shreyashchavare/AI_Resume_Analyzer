"""
Module: user_service.py

Description:
    Handles all user side information and their action by frontend.

Author: Shreyash Chavare
Created: 2025-12-26
"""

import streamlit as st
import os
import pandas as pd
from datetime import datetime
from llm import llm
from chromadb_utils import chromadb_utils
# ========================== CONFIG =================================
st.set_page_config(page_title="AI Resume Analyzer for HR", page_icon="📓", layout="wide")
USER_FILE = "user.csv"
HISTORY_FILE = "history.csv"

# ========================== INIT FILES ===============================
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index= False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["username", "uploaded_at"]).to_csv(HISTORY_FILE, index= False)

# ========================== SESSION STATE ===========================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

if "llm_instance" not in st.session_state:
    st.session_state.llm_instance = llm()

if "db_instance" not in st.session_state:
    st.session_state.db_instance = chromadb_utils()
# ============================ SIDEBAR MENU =================================
st.sidebar.title("📂 Menu")
if not st.session_state.authenticated:
    menu = st.sidebar.radio("Navigation",["Home", "Login", "Register"])
else:
    menu = st.sidebar.radio("Navigation",["Chat", "Resume Management", "Logout"])

# ============================ HELPER FUNCTION =========================
def authenticate_user(username, password):
    username = username.strip()
    password = password.strip()

    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        return False

    users = pd.read_csv(USER_FILE, dtype=str)

    return not users[
        (users["username"].str.strip().str.lower() == username.lower()) &
        (users["password"].str.strip() == password)
    ].empty



def register_user(username, password):
    username = username.strip()
    password = password.strip()

    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        users = pd.DataFrame(columns=["username", "password"])
    else:
        users = pd.read_csv(USER_FILE, dtype=str)

    if not users.empty and username.lower() in users["username"].str.lower().values:
        return False

    users.loc[len(users)] = [username, password]
    users.to_csv(USER_FILE, index=False)
    return True



def save_login_history(username):
    history = pd.read_csv(HISTORY_FILE)
    history.loc[len(history)] = [
        username,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]
    history.to_csv(HISTORY_FILE, index=False)

#================================= Home   ===================================
if menu == "Home":
    st.title("🏠 Welcome")
    st.write("Please login or register to continue.")

#================================= Login  ===================================
elif menu == "Login":
    st.title("🔏Login")

    with st.form(key="login_form"):
        st.header("Login Form")
        username = st.text_input("User Name", key="log_id")
        password = st.text_input("Password", type="password", key="log_pass")
        submit_btn_l = st.form_submit_button("Submit", type="primary")

    if submit_btn_l:
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username.strip()  # display-safe
            st.success("Login successful")
            save_login_history(st.session_state.username)
            st.rerun()
        else:
            st.error("Invalid credentials")

#================================= REGISTER ===================================
elif menu == "Register":
    st.title("📝 Register")
    #Registration Form
    with st.form(key="reg_form"):
        st.header("Registration Form")
        username = st.text_input(key="reg_id", label="User Name")
        password = st.text_input(key="reg_pass", label="Password", type="password")

        submit_btn_r = st.form_submit_button("Submit", type="primary")

    # from submit handling
    if submit_btn_r:
        if register_user(username, password):
            st.success("Registration successful. Please login.")
        else:
            st.error("User already exists")

#================================= REGISTER ===================================
elif menu == "Chat":
    if st.session_state.authenticated:
        st.header("💬 Chat With Resume Analyzer")
        
        # Show existing resumes
        st.subheader("📄 Available Resumes")
        st.table(st.session_state.db_instance.list_resume_in_db())
        st.divider()

        user_input = st.chat_input("Enter your description for search")

        if user_input:
            response = st.session_state.llm_instance.user_llm_prompts_interaction(
                user_input
            )

        # Display chat in Streamlit
        st.session_state.llm_instance.display_chat()

#================================= REGISTER ===================================
elif menu == "Resume Management":
    if st.session_state.authenticated:
        st.header("📂 Resume Resource Management")

        # Show existing resumes
        st.subheader("📄 Available Resumes")
        st.table(st.session_state.db_instance.list_resume_in_db())

        st.divider()

        # Input field
        pdf_path = st.text_input(
            "📂 Enter path of resume PDF",
            placeholder="e.g. D:/resumes/john_doe.pdf"
        )
        
        if not pdf_path:
            st.warning("⚠️ Please provide a file path")
        elif not pdf_path.lower().endswith(".pdf"):
            st.error("❌ Only PDF files are allowed")
        elif not os.path.exists(pdf_path):
            st.error("❌ File does not exist")
        else:
            # safe to process
            pass

        # Buttons layout
        col1, col2, col3 = st.columns(3)

        with col1:
            add_clicked = st.button("➕ Add")

        with col2:
            update_clicked = st.button("✏️ Update")

        with col3:
            delete_clicked = st.button("🗑️ Delete")

        # ---- Button Actions ----
        if add_clicked:
            if not pdf_path:
                st.warning("⚠️ Please provide a PDF path")
            elif st.session_state.db_instance.add_resume_in_db(pdf_path):
                st.success("✅ PDF added successfully")
            else:
                st.error("❌ Failed to add PDF")

        if update_clicked:
            if not pdf_path:
                st.warning("⚠️ Please provide a PDF path")
            elif st.session_state.db_instance.update_resume_in_db(pdf_path):
                st.success("✅ PDF updated successfully")
            else:
                st.error("❌ Failed to update PDF")

        if delete_clicked:
            if not pdf_path:
                st.warning("⚠️ Please provide a PDF path")
            elif st.session_state.db_instance.delete_resume_from_db(pdf_path):
                st.success("🗑️ PDF deleted successfully")
            else:
                st.error("❌ Failed to delete PDF")

        # ===================== DIRECTORY INGESTION =====================
        st.divider()
        st.subheader("📁 Add Resumes by Directory")

        dir_path = st.text_input(
            "📂 Enter directory path containing resume PDFs",
            placeholder="e.g. D:/resumes/"
        )

        dir_add_clicked = st.button("📥 Add All PDFs From Directory")

        if dir_add_clicked:
            if not dir_path:
                st.warning("⚠️ Please provide a directory path")

            elif not os.path.isdir(dir_path):
                st.error("❌ Directory does not exist")

            else:
                with st.spinner("Processing resumes from directory..."):
                    success = st.session_state.db_instance.add_resumes_in_db(dir_path)

                if success:
                    st.success("✅ All resumes from directory added successfully")
                    st.rerun()
                else:
                    st.error("❌ Failed to add resumes from directory")

# ================= LOGOUT =================
elif menu == "Logout":
    st.session_state.authenticated = False
    st.session_state.userid = None
    st.session_state.llm_instance.clear_chat()
    st.success("Logged out successfully")
    st.rerun()



