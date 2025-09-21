# Pathfinder AI: Your Personal Career Co-Pilot 🚀

An intelligent career advisor that provides a **personalized, end-to-end toolkit for job seekers**. Pathfinder AI leverages **Generative AI** to analyze your skills, identify market trends, and prepare you for every step of your career journey — from self-discovery to interview success.

---

## ✨ Live Demo

➡️ \[[Deployed Application Link – Placeholder](https://adept-ai-svplp3m4e6kqvk5iauwear.streamlit.app/)]

<img width="1918" height="911" alt="image" src="https://github.com/user-attachments/assets/983305ec-8cf0-4799-85e7-294eab8887ad" />


---

## 🎯 The Problem

In today’s fast-evolving job market, students and professionals often struggle with questions like:

* *What skills are actually in demand?*
* *How do my current skills match up to my dream job?*
* *How can I effectively prepare for interviews for a specific role?*

Generic advice isn’t enough. Job seekers need a **dynamic, data-driven, personalized guide** to navigate their careers with confidence.

---

## 💡 Our Solution: Pathfinder AI

Pathfinder AI is a **multi-faceted career platform** powered by Google’s **Gemini LLM**. It provides an **end-to-end personalized experience** across the entire career development lifecycle.

---

## 🚀 Key Features

| Feature                                | Description                                                                                                  |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| 👤 **Personalized Profile Builder**    | Upload your PDF/TXT resume, parse it instantly, and enrich your profile with skills + proficiency levels.    |
| 💡 **AI Career Advisor**               | Get skill gap analysis, actionable learning paths, and AI-generated project ideas to enhance your portfolio. |
| 🌌 **Interactive Skill Constellation** | Visualize connections between skills and roles, uncovering non-obvious career pivots.                        |
| 📈 **Real-Time Market Pulse**          | Analyze job market trends: in-demand skills, salary ranges, industries, and market sentiment.                |
| 🎙️ **AI Mock Interview Simulator**    | Practice with an AI interviewer tailored to your role and receive detailed Hotspot Analysis feedback.        |
| 📄 **Resume & Cover Letter Co-Pilot**  | Critique your resume for job-specific alignment or auto-generate tailored cover letters.                     |

---

## 🛠️ Tech Stack

* **Backend:** Python
* **Frontend/UI:** Streamlit
* **AI/LLM:** Google Gemini API (`gemini-1.5-flash-latest`)
* **Core Libraries:**

  * `streamlit`
  * `google-generativeai`
  * `streamlit-agraph` *(for graph visualization)*
  * `PyMuPDF` *(for PDF parsing)*

---

## ⚙️ Getting Started

### 1️⃣ Prerequisites

* Python **3.9+**
* `pip` package manager

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 3️⃣ Set Up Virtual Environment *(Recommended)*

```bash
# Create a virtual environment
python -m venv venv  

# Activate it
# On Windows:
venv\Scripts\activate  
# On macOS/Linux:
source venv/bin/activate  
```

### 4️⃣ Install Dependencies

Create a `requirements.txt` file:

```
streamlit
google-generativeai
streamlit-agraph
PyMuPDF
```

Install packages:

```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Your API Key

Create `.streamlit/secrets.toml`:

```toml
API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

In `career_advisor_app.py`, load the key:

```python
API_KEY = st.secrets["API_KEY"]
```

### 6️⃣ Run the Application

```bash
streamlit run career_advisor_app.py
```

Open your browser at **[http://localhost:8501](http://localhost:8501)** 🎉

---

## ❤️ Built For

The **Gen AI Hackathon**, with the vision of making **career guidance smarter, adaptive, and accessible**.

