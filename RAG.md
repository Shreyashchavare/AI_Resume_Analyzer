# 📄 AI-Enabled Resume Analyzer & Shortlisting System (RAG)

An AI-powered Resume Shortlisting Application for HR Teams using **Retrieval Augmented Generation (RAG)**.

---

## 📌 Project Overview

Recruitment teams often spend a significant amount of time manually reviewing resumes to identify suitable candidates.  
This project automates and simplifies the **resume shortlisting process** using **Generative AI** and **RAG**.

The system allows HR users to:
- Upload and manage resumes
- Perform semantic resume search
- Automatically shortlist the most relevant candidate for a job description
- Get **fact-based, unbiased HR-style analysis**

This project is developed as part of the **RAG Assignment** at **Sunbeam Institute of Information Technology**.

---

## 🎯 Objectives

- Automate resume screening using AI
- Replace keyword search with semantic similarity
- Ensure LLM outputs are grounded strictly in resume data
- Demonstrate real-world RAG architecture
- Provide a simple, HR-friendly UI

---

## 🚀 Key Features

### 🔐 User Authentication
- Login and Registration
- Session-based authentication
- Secure logout with session cleanup

### 📂 Resume Management
- Add resumes (PDF)
- Update existing resumes
- Delete resumes (from DB and filesystem)
- List all uploaded resumes with metadata

### 🧠 AI Resume Shortlisting (RAG)
- HR enters a job description
- Relevant resumes retrieved from ChromaDB
- LLM analyzes resumes using **only retrieved data**
- Outputs structured HR-style evaluation

### 💬 HR Chat Interface
- Conversational interface
- Context-aware responses
- Clean chat history handling

---

## 🧠 RAG Architecture (High-Level)

```
Resume PDFs
↓
PDF Text Extraction
↓
Embedding Generation
↓
Chroma Vector Database
↓
Job Description (Query)
↓
Similarity Search
↓
Retrieved Resume Context
↓
LLM (HR Analyst Role)
↓
Shortlisted Candidate
```


---

## 🧩 Technology Stack

| Component | Technology |
|--------|-----------|
| Language | Python |
| UI | Streamlit |
| LLM | Local LLM (Gemma 3 4B via LM Studio) |
| RAG Framework | LangChain |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector DB | ChromaDB (Persistent) |
| PDF Processing | Custom PDF utilities |
| Storage | CSV + Local filesystem |

---

## 🗂️ Project Structure

```
├── user_service.py # Streamlit frontend & user flow
├── llm.py # LLM logic & HR prompt design
├── chromadb_utils.py # ChromaDB CRUD operations
├── embedding.py # Resume & query embeddings
├── pdf_utils.py # PDF reading & chunk extraction
├── resume_rag/ # Persistent ChromaDB storage
├── user.csv # Registered users(demo)
├── history.csv # Login history(demo)
└── RAG.md
```

---

## 🔍 How Resume Shortlisting Works

1. HR enters a job description
2. Job description is embedded
3. ChromaDB performs semantic similarity search
4. Relevant resume chunks are retrieved
5. LLM analyzes resumes using strict RAG rules
6. Final output includes:
   - PDF name
   - Candidate name
   - Summary
   - Reason for selection
   - Comparative note

⚠️ The LLM **does not assume or hallucinate** any information.

---

## 📐 LLM Constraints

- Uses ONLY resume content and job description
- No guessing or inferred skills
- Missing information is treated as NOT PRESENT
- Output format is strictly controlled
- Fully explainable HR-style reasoning

---

## 🧪 Assumptions & Constraints

- Only PDF resumes are supported
- Shortlisting is semantic, not keyword-based
- Accuracy depends on resume quality
- Local LLM must be running (LM Studio)

---

## 🔮 Future Enhancements

- Resume scoring & ranking
- Skill extraction and tagging
- Multi-job profile support
- Role-based access (Admin / HR)
- Resume version history
- Soft delete & audit logs
- DOCX resume support

---

## 📚 Learning Outcomes

Through this project, you will learn:
- Practical RAG architecture
- Vector databases and embeddings
- Semantic document search
- Prompt engineering for factual grounding
- End-to-end AI application design
- Streamlit + AI backend integration

---

## 🏁 Conclusion

This project demonstrates how **Generative AI and RAG** can solve a real-world HR problem.  
By combining **Streamlit**, **ChromaDB**, and a **local LLM**, the system delivers:

✔ Accurate resume shortlisting  
✔ Transparent decision-making  
✔ Scalable and modular architecture  

---

## 👨‍💻 Author

**Shreyash Chavare**  
Sunbeam Institute of Information Technology  
December 2025

---

## 🏫 Academic Context & Attribution

This project is developed as part of a **Retrieval Augmented Generation (RAG) assignment**
provided by **Sunbeam Institute of Information Technology**.

- The **problem statement and project idea** were given as part of the academic curriculum.
- The **design, architecture, implementation, prompt engineering, and integrations**
  have been independently developed by the author for learning and demonstration purposes.
- This project is intended strictly for **educational and non-commercial use**.



---
