# Adept AI — Your Personal Career Co-Pilot 🚀

An intelligent, AI-powered career advisor that gives you a **personalized, end-to-end toolkit for job seekers**. Adept AI leverages **Google's Gemini LLM** to analyze your skills, identify market trends, and prepare you for every step of your career journey — from self-discovery to interview success.

---

## ✨ Live Demo

➡️ [Deployed Application](https://adept-ai-svplp3m4e6kqvk5iauwear.streamlit.app/)

<img width="1918" height="911" alt="Adept AI Screenshot" src="https://github.com/user-attachments/assets/983305ec-8cf0-4799-85e7-294eab8887ad" />

---

## 🎯 The Problem

In today's fast-evolving job market, students and professionals often struggle with:

- *What skills are actually in demand?*
- *How do my current skills match up to my dream job?*
- *How can I effectively prepare for interviews for a specific role?*

Generic advice isn't enough. Job seekers need a **dynamic, data-driven, personalized guide**.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 👤 **Profile Builder** | Upload your PDF/TXT resume or paste it manually, and enrich your profile with skills and career goals. |
| 💡 **AI Career Advisor** | Get skill gap analysis, actionable learning paths, and AI-generated project ideas tailored to your target role. |
| 📈 **Market Pulse Dashboard** | Analyze job market trends: in-demand skills, salary ranges, top industries, and market sentiment. |
| 🎙️ **AI Mock Interview Simulator** | Practice with an AI interviewer tailored to your target role and receive detailed feedback. |
| 📄 **Resume & Cover Letter Co-Pilot** | Critique your resume for job-specific alignment or auto-generate tailored cover letters. |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.9+ |
| **UI Framework** | Streamlit |
| **AI / LLM** | Google Gemini API (`gemini-flash-latest`) |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Graph Visualization** | streamlit-agraph |

---

## ⚙️ Getting Started (Local Setup)

### 1️⃣ Prerequisites

- **Python 3.9 or higher** — [Download Python](https://www.python.org/downloads/)
- **pip** package manager (bundled with Python)
- A **Google Gemini API Key** — [Get one here](https://aistudio.google.com/app/apikey)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/Adept-AI.git
cd Adept-AI
```

---

### 3️⃣ Set Up a Virtual Environment *(Recommended)*

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate
```

---

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

```
streamlit
google-generativeai
streamlit-agraph
PyMuPDF
```

---

### 5️⃣ Configure Your API Key

Open `gen.py` and replace the placeholder API key on **line 8** with your own:

```python
# gen.py — line 8
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

> ⚠️ **Security tip:** For production or shared environments, use Streamlit's secrets manager instead.
> Create a file at `.streamlit/secrets.toml`:
> ```toml
> API_KEY = "YOUR_GEMINI_API_KEY_HERE"
> ```
> Then update `gen.py` to read: `API_KEY = st.secrets["API_KEY"]`

---

### 6️⃣ Run the Application

```bash
streamlit run gen.py
```

Your browser will automatically open at **[http://localhost:8501](http://localhost:8501)** 🎉

---

## 📁 Project Structure

```
Adept-AI/
├── gen.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── gen.streamlit/      # Streamlit config files
└── README.md           # This file
```

---

## 🔧 Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError` | Make sure you ran `pip install -r requirements.txt` inside the virtual environment |
| `Failed to configure AI model` | Double-check your API key in `gen.py` |
| `Port already in use` | Run `streamlit run gen.py --server.port 8502` to use a different port |
| Blank page / app not loading | Try refreshing the browser or restarting the Streamlit server |

---

## ❤️ Built For

The **Gen AI Hackathon** — with the vision of making career guidance smarter, adaptive, and accessible to everyone.
