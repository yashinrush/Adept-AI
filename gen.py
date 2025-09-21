import streamlit as st
import google.generativeai as genai
import json
import time

# --- Configuration ---
# WARNING: Do not hardcode API keys in production. Use environment variables or Streamlit secrets.
# The user-provided key is used here for hackathon purposes.
API_KEY = "AIzaSyAERC3aSiS3jyWH4uBCBGpITnu9XOUH7z0" # This is the user provided API key

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Failed to configure AI model. Please check your API key. Error: {e}", icon="🚨")
    st.stop()

# --- Page Configuration ---
st.set_page_config(
    page_title="Adept AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling (UI Enhancement) ---
st.markdown("""
<style>
    /* --- DARK THEME --- */

    /* Main app styling */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FAFAFA !important;
    }
    p, .st-write, .st-markdown {
        color: #E0E0E0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
        border-right: 2px solid #31333F;
    }
    [data-testid="stSidebar"] h1 {
        color: #4B8BBE !important; /* Accent color for sidebar title */
    }

    /* Main call-to-action button styling */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #4B8BBE;
        background-color: #4B8BBE;
        color: white;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #5A9CD8;
        color: white;
        border: 1px solid #5A9CD8;
    }
    
    /* Sidebar navigation buttons */
    /* Inactive (secondary) button */
    div[data-testid="stSidebarContent"] .stButton>button[kind="secondary"] {
        background-color: transparent;
        color: #FAFAFA;
        border: 1px solid #31333F;
    }
    div[data-testid="stSidebarContent"] .stButton>button[kind="secondary"]:hover {
        background-color: #31333F;
        border-color: #4B8BBE;
    }
    /* Active (primary) button */
    div[data-testid="stSidebarContent"] .stButton>button[kind="primary"] {
        background-color: #4B8BBE;
        color: white;
        border-color: #4B8BBE;
    }

    /* Expander styling */
    .st-expander {
        border: 1px solid #31333F !important;
        border-radius: 10px !important;
        background-color: #262730;
    }
    .st-expander header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4B8BBE;
    }
    .st-expander p {
        color: #E0E0E0;
    }

    /* Card-like containers */
    .card {
        background-color: #262730;
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
    }
    .card p {
        color: #E0E0E0;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
    }
    .chat-message.user {
        background-color: #0B4C7A;
        justify-content: flex-end;
    }
    .chat-message.bot {
        background-color: #262730;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
    }
     .chat-message.user .avatar {
        margin-left: 1rem;
        margin-right: 0;
    }
    
    /* Text input/area styling */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background-color: #1E1E1E;
        color: #FAFAFA;
        border: 1px solid #31333F;
    }
    
    /* Native Streamlit alerts (info, warning, error) */
    /* They have light backgrounds, so text inside needs to be dark */
    [data-testid="stAlert"] * {
        color: #111 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
def init_session_state():
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {
            "resume_text": "",
            "skills": [],
            "interests": "",
            "career_goal": ""
        }
    if "page" not in st.session_state:
        st.session_state.page = "Home"
    if "interview_chat" not in st.session_state:
        st.session_state.interview_chat = []
    if "analysis_cache" not in st.session_state:
        st.session_state.analysis_cache = {}
    if "interview_feedback" not in st.session_state:
        st.session_state.interview_feedback = None
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "market_pulse_cache" not in st.session_state:
        st.session_state.market_pulse_cache = {}


# --- AI Helper Function ---
def get_ai_response(prompt, is_json=False):
    """
    Generic function to get a response from the AI model.
    Retries with exponential backoff.
    """
    retries = 3
    delay = 2
    for i in range(retries):
        try:
            generation_config = genai.types.GenerationConfig(
                # Only one candidate for now.
                candidate_count=1,
                temperature=0.7,
            )
            if is_json:
                # Adding instruction for JSON output directly in the prompt
                full_prompt = f"{prompt}\n\nIMPORTANT: Please provide the response in a valid JSON format only, with no other text or explanations."
                response = model.generate_content(full_prompt, generation_config=generation_config)
                # Attempt to find and parse the JSON block
                json_text = response.text.strip().lstrip('```json').rstrip('```').strip()
                return json.loads(json_text)
            else:
                response = model.generate_content(prompt, generation_config=generation_config)
                return response.text
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                st.error(f"AI model request failed after multiple retries. Error: {e}", icon="🔥")
                return None
    return None

# --- Page Rendering Functions ---

def render_home():
    st.title("Welcome to Your Personalized AI Career Advisor 🚀")
    st.markdown("### Your one-stop solution to navigate the job market, powered by Generative AI.")

    st.markdown("""
    <div class="card">
    <p>In today's fast-paced job market, finding the right career path can be overwhelming. This tool is designed to be your personal guide. We'll help you understand your skills, discover exciting career opportunities, and prepare you for the interviews that will land you your dream job.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**1. Build Your Profile**", icon="👤")
        st.write("Upload your resume or manually enter your skills, interests, and career goals. The more detail you provide, the better the advice!")
    with col2:
        st.info("**2. Get AI-Powered Insights**", icon="💡")
        st.write("Discover your skill gaps, get a personalized learning plan, and explore career paths that match your unique profile.")
    with col3:
        st.info("**3. Prepare for Success**", icon="🎯")
        st.write("Practice with our AI mock interviewer and fine-tune your resume to stand out to recruiters for any job.")
        
    if st.button("Get Started: Build Your Profile →", key="start_button"):
        st.session_state.page = "Profile Builder"
        st.rerun()


def render_profile_builder():
    st.title("👤 Profile Builder")
    st.markdown("Let's create a snapshot of your professional self. Provide as much detail as possible for the most accurate advice.")

    with st.container(border=True):
        st.subheader("Upload Your Resume (Optional)")
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF, TXT) and we'll try to extract the text.", 
            type=['txt', 'pdf']
        )
        if uploaded_file is not None:
            try:
                # Simple text extraction (for PDF, might need a library like PyMuPDF)
                if uploaded_file.type == "application/pdf":
                    st.warning("PDF parsing is experimental. For best results, please copy-paste the text below.", icon="⚠️")
                    # Placeholder for more complex PDF extraction
                    st.session_state.user_profile["resume_text"] = "PDF content extraction is a complex feature. Please paste your resume text manually for this demo."
                else:
                    st.session_state.user_profile["resume_text"] = uploaded_file.getvalue().decode("utf-8")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        resume_text = st.text_area(
            "Or, paste your resume text here:", 
            value=st.session_state.user_profile.get("resume_text", ""), 
            height=300
        )
        st.session_state.user_profile["resume_text"] = resume_text

    with st.container(border=True):
        st.subheader("Your Skills & Interests")
        skills = st.text_input(
            "Enter your skills, separated by commas (e.g., Python, Data Analysis, React)",
            value=", ".join(st.session_state.user_profile.get("skills", []))
        )
        st.session_state.user_profile["skills"] = [s.strip() for s in skills.split(',') if s.strip()]

        interests = st.text_area(
            "Describe your professional interests and passions:",
            value=st.session_state.user_profile.get("interests", "")
        )
        st.session_state.user_profile["interests"] = interests

    with st.container(border=True):
        st.subheader("Your Career Goal")
        career_goal = st.text_input(
            "What is your target job role? (e.g., Software Engineer, Product Manager)",
            value=st.session_state.user_profile.get("career_goal", "")
        )
        st.session_state.user_profile["career_goal"] = career_goal

    if st.button("Save and Analyze My Profile", key="save_profile"):
        if not st.session_state.user_profile["career_goal"] or (not st.session_state.user_profile["skills"] and not st.session_state.user_profile["resume_text"]):
            st.error("Please provide your Career Goal and at least some skills or a resume.", icon="🚨")
        else:
            # Invalidate cache if profile changes
            st.session_state.analysis_cache = {}
            st.session_state.page = "Career Advisor"
            st.success("Profile saved! Navigating to the Career Advisor...")
            time.sleep(1)
            st.rerun()

def render_career_advisor():
    st.title("💡 AI Career Advisor")
    st.markdown("Here are your personalized insights based on your profile.")

    profile = st.session_state.user_profile
    if not profile["career_goal"] or (not profile["skills"] and not profile["resume_text"]):
        st.warning("Please build your profile first to get advice!", icon="⚠️")
        if st.button("Go to Profile Builder"):
            st.session_state.page = "Profile Builder"
            st.rerun()
        return

    st.markdown(f"### Analysis for: **{profile['career_goal']}**")

    cache_key = f"{profile['career_goal']}-{'-'.join(sorted(profile['skills']))}"
    if cache_key in st.session_state.analysis_cache:
        analysis = st.session_state.analysis_cache[cache_key]
    else:
        with st.spinner("Your AI advisor is analyzing your profile... This may take a moment."):
            prompt = f"""
            Analyze the user profile for a career as a '{profile['career_goal']}'.
            User Skills: {', '.join(profile['skills'])}
            User Resume: {profile['resume_text']}
            User Interests: {profile['interests']}

            Provide a detailed analysis in a valid JSON structure. Do NOT include any text outside of the JSON.
            Example JSON:
            {{
                "skill_gap_analysis": {{
                    "required_skills": ["Python", "SQL", "Data Visualization", "Machine Learning", "Communication"],
                    "user_has_skills": ["Python", "SQL"],
                    "missing_skills": ["Data Visualization", "Machine Learning", "Communication"]
                }},
                "learning_pathway": [
                    {{
                        "skill_to_learn": "Data Visualization",
                        "recommendation": "Master a library like Matplotlib or Seaborn.",
                        "resources": [
                            "Coursera: 'Data Visualization with Python'",
                            "Project Idea: Create a dashboard analyzing a public dataset (e.g., COVID-19 trends)."
                        ]
                    }},
                    {{
                        "skill_to_learn": "Machine Learning",
                        "recommendation": "Understand core concepts and popular libraries.",
                        "resources": [
                            "Book: 'Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow'",
                            "Project Idea: Build a simple spam classifier for emails."
                        ]
                    }}
                ],
                "alternative_careers": [
                    {{
                        "career_title": "Data Engineer",
                        "match_reason": "Strong foundation in Python and SQL are highly transferable to data engineering roles."
                    }}
                ],
                "summary": "You have a strong foundational skillset for a Data Analyst role. Focusing on practical application through data visualization and machine learning projects will make you a highly competitive candidate."
            }}
            """
            analysis = get_ai_response(prompt, is_json=True)
            if analysis:
                st.session_state.analysis_cache[cache_key] = analysis
            else:
                st.error("Failed to get analysis from AI. The model may be overloaded or the request timed out. Please try again later.", icon="🔥")
                return

    if not analysis:
        return
        
    st.markdown(f'<div class="card"><p><strong>Summary:</strong> {analysis.get("summary", "No summary available.")}</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📊 Skill Gap Analysis")
            sga = analysis.get("skill_gap_analysis", {})
            if sga:
                st.write("**Skills You Have:**")
                for skill in sga.get("user_has_skills", []):
                    st.markdown(f"✅ {skill}")
                
                st.write("**Skills to Develop:**")
                for skill in sga.get("missing_skills", []):
                    st.markdown(f"❌ {skill}")
            else:
                st.write("Could not perform skill gap analysis.")
    with col2:
         with st.container(border=True):
            st.subheader("🛤️ Alternative Career Paths")
            alt_careers = analysis.get("alternative_careers", [])
            if alt_careers:
                for career in alt_careers:
                    with st.expander(f"**{career.get('career_title')}**"):
                        st.write(career.get('match_reason'))
            else:
                st.write("No alternative careers could be identified at this time.")

    st.subheader("📚 Your Personalized Learning Pathway")
    learning_pathway = analysis.get("learning_pathway", [])
    if learning_pathway:
        for item in learning_pathway:
            with st.expander(f"**Learn: {item.get('skill_to_learn')}** - {item.get('recommendation')}"):
                for resource in item.get("resources", []):
                    st.markdown(f"- {resource}")
    else:
        st.write("Could not generate a learning pathway.")

def render_market_pulse():
    st.title("📈 Market Pulse Dashboard")
    st.markdown("Get real-time insights into the job market for any career.")

    job_title = st.text_input("Enter a job title to analyze:", placeholder="e.g., Data Scientist, UX Designer")

    if st.button("Analyze Market Trends", key="market_pulse_button"):
        if not job_title:
            st.error("Please enter a job title.", icon="🚨")
        else:
            with st.spinner(f"Analyzing the job market for '{job_title}'..."):
                prompt = f"""
                Analyze the current job market for a '{job_title}'. Based on recent trends and data, provide the following information in a valid JSON structure. Do not include any text outside of the JSON.

                Example JSON for 'Data Scientist':
                {{
                    "market_summary": "The market for Data Scientists remains strong, with high demand in the tech, finance, and healthcare sectors. The role is becoming more specialized, with an emphasis on machine learning operations (MLOps) and cloud platforms.",
                    "trending_skills": ["Python", "SQL", "TensorFlow/PyTorch", "AWS/GCP/Azure", "MLOps"],
                    "salary_range": "₹12,00,000 - ₹25,00,000 per annum (India)",
                    "top_industries": ["Technology & SaaS", "Financial Services", "Healthcare & Pharma"],
                    "market_sentiment": "Growing"
                }}
                """
                analysis = get_ai_response(prompt, is_json=True)
                if analysis:
                    st.session_state.market_pulse_cache[job_title] = analysis
                else:
                    st.error("Failed to get market analysis. The model may be overloaded or the request timed out. Please try again later.", icon="🔥")

    if job_title and job_title in st.session_state.market_pulse_cache:
        data = st.session_state.market_pulse_cache[job_title]
        st.markdown("---")
        st.subheader(f"Insights for: {job_title}")
        
        st.markdown(f'<div class="card"><p><strong>Market Summary:</strong> {data.get("market_summary", "N/A")}</p></div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Market Sentiment", value=data.get("market_sentiment", "N/A"))
        with col2:
            st.metric(label="Estimated Salary Range (India)", value=data.get("salary_range", "N/A"))
        
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.subheader("🔥 Trending Skills")
                for skill in data.get("trending_skills", []):
                    st.markdown(f"- {skill}")
        
        with c2:
            with st.container(border=True):
                st.subheader("🏢 Top Hiring Industries")
                for industry in data.get("top_industries", []):
                    st.markdown(f"- {industry}")
        
def render_mock_interview():
    st.title("🎙️ AI Mock Interview Simulator")
    st.markdown("Practice your interview skills. The AI will act as your interviewer and provide feedback.")

    job_role = st.text_input("Enter the job role you want to practice for:", value=st.session_state.user_profile.get("career_goal", ""))

    if st.button("Start New Interview", type="primary") and job_role:
        st.session_state.interview_active = True
        st.session_state.interview_feedback = None
        st.session_state.interview_chat = [{
            "role": "system",
            "content": f"You are an expert interviewer for a '{job_role}' position. Introduce yourself and ask the first relevant question. Ask only one question at a time and wait for the user's response before proceeding. Keep your questions concise."
        }]
        with st.spinner("Preparing your interviewer..."):
            ai_response = get_ai_response(st.session_state.interview_chat[0]['content'])
            if ai_response:
                st.session_state.interview_chat.append({"role": "bot", "content": ai_response})
            else:
                st.session_state.interview_active = False
        st.rerun()

    if not st.session_state.interview_active:
        st.info("Enter a job role and click 'Start New Interview' to begin.")
        if st.session_state.interview_feedback:
            st.subheader("📋 Interview Feedback")
            st.markdown(st.session_state.interview_feedback)
        return

    # Display chat history
    chat_container = st.container(height=500, border=True)
    with chat_container:
        for message in st.session_state.interview_chat[1:]: # Skip system prompt
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user"><div style="flex-grow: 1; text-align: right;">{message["content"]}</div><div class="avatar" style="background-color: #4B8BBE; color: white; display: flex; align-items: center; justify-content: center;">You</div></div>', unsafe_allow_html=True)
            elif message["role"] == "bot":
                st.markdown(f'<div class="chat-message bot"><div class="avatar" style="background-color: #1E3A5F; color: white; display: flex; align-items: center; justify-content: center;">AI</div><div>{message["content"]}</div></div>', unsafe_allow_html=True)
    
    # User input
    if user_input := st.chat_input("Your answer..."):
        st.session_state.interview_chat.append({"role": "user", "content": user_input})
        
        prompt_history = "\n".join([f"{'Human' if msg['role'] == 'user' else 'AI'}: {msg['content']}" for msg in st.session_state.interview_chat])
        
        with st.spinner("AI is thinking..."):
            ai_response = get_ai_response(prompt_history)
            if ai_response:
                st.session_state.interview_chat.append({"role": "bot", "content": ai_response})
        st.rerun()

    if st.button("End Interview & Get Feedback"):
        st.session_state.interview_active = False
        with st.spinner("Generating your interview feedback..."):
            feedback_prompt = f"""
            The following is a transcript of a job interview for a '{job_role}' position.
            Please act as a hiring manager and provide constructive feedback for the user (Human).
            Analyze their responses for clarity, STAR method usage (for behavioral questions), technical accuracy, and overall communication style.
            Provide a summary of their strengths, areas for improvement, and actionable tips. Format the response in Markdown.

            Transcript:
            {"\n".join([f"{'User' if msg['role'] == 'user' else 'Interviewer'}: {msg['content']}" for msg in st.session_state.interview_chat[1:]])}
            """
            feedback = get_ai_response(feedback_prompt)
            st.session_state.interview_feedback = feedback
        st.rerun()
        
def render_resume_copilot():
    st.title("📄 Resume & Cover Letter Co-pilot")
    st.markdown("Tailor your application materials to perfectly match the job you want.")

    col1, col2 = st.columns(2)

    with col1:
        job_desc = st.text_area("📋 Paste the Job Description Here", height=400, placeholder="e.g., We are looking for a proactive Product Manager...")
    
    with col2:
        resume_content = st.text_area("📝 Paste Your Resume/CV Content Here", height=400, value=st.session_state.user_profile.get("resume_text", ""), placeholder="e.g., John Doe - Experienced Software Engineer...")

    option = st.radio(
        "What would you like to generate?",
        ("Critique My Resume", "Draft a Cover Letter"),
        horizontal=True,
    )
    
    if st.button("Analyze and Generate", key="copilot_generate"):
        if not job_desc or not resume_content:
            st.error("Please paste both the job description and your resume content.", icon="🚨")
        else:
            with st.spinner("Your AI co-pilot is working its magic..."):
                if option == "Critique My Resume":
                    prompt = f"""
                    Act as a professional resume reviewer. Critique the following resume based on the provided job description. 
                    
                    **Job Description:**
                    {job_desc}

                    **Resume Content:**
                    {resume_content}

                    Provide a detailed critique covering these areas:
                    1.  **Keyword Alignment:** Identify key skills and qualifications from the job description that are missing or not emphasized in the resume.
                    2.  **Action Verb Strength:** Suggest stronger action verbs to make the experience more impactful.
                    3.  **Quantifiable Results:** Point out where the user could add numbers or metrics to show achievements.
                    4.  **Overall Impression & Suggestions:** Give a final summary and actionable advice for improvement.

                    Format the output using Markdown.
                    """
                else: # Draft a Cover Letter
                    prompt = f"""
                    Act as a professional career coach. Write a compelling and professional draft for a cover letter based on the user's resume and the target job description.

                    **Job Description:**
                    {job_desc}

                    **User's Resume Content:**
                    {resume_content}

                    The cover letter should:
                    - Be structured in 3-4 paragraphs.
                    - Directly address the key requirements from the job description.
                    - Highlight the most relevant skills and experiences from the user's resume.
                    - Maintain a professional and enthusiastic tone.
                    - Be a draft that the user can easily edit and personalize.

                    Format the output using Markdown.
                    """
                
                response = get_ai_response(prompt)
                if response:
                    st.markdown("---")
                    st.subheader("✨ Your AI-Generated Result")
                    st.markdown(response)
                else:
                    st.error("Failed to generate a response. Please try again.", icon="🔥")


# --- Main App Logic ---
def main():
    init_session_state()

    with st.sidebar:
        st.markdown(f'<h1>AI Career Advisor</h1>', unsafe_allow_html=True)
        
        # Navigation
        pages = {
            "Home": "🏠 Home",
            "Profile Builder": "👤 Profile Builder",
            "Career Advisor": "💡 Career Advisor",
            "Market Pulse": "📈 Market Pulse",
            "Mock Interview": "🎙️ Mock Interview",
            "Resume Co-pilot": "📄 Resume Co-pilot",
        }
        
        for page_id, page_name in pages.items():
            if st.button(page_name, use_container_width=True, type="secondary" if st.session_state.page != page_id else "primary"):
                st.session_state.page = page_id
                st.rerun()

        st.markdown("---")
        st.info("Built for the Gen AI Hackathon with ❤️ by a Team TECHNOKAMI.")
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-View_Code-blue?style=for-the-badge&logo=github)](https://github.com/yashinrush/AI-Personalized-Career-and-Skills-Advisor)", unsafe_allow_html=True)


    # Page routing
    if st.session_state.page == "Home":
        render_home()
    elif st.session_state.page == "Profile Builder":
        render_profile_builder()
    elif st.session_state.page == "Career Advisor":
        render_career_advisor()
    elif st.session_state.page == "Market Pulse":
        render_market_pulse()
    elif st.session_state.page == "Mock Interview":
        render_mock_interview()
    elif st.session_state.page == "Resume Co-pilot":
        render_resume_copilot()


if __name__ == "__main__":
    main()

