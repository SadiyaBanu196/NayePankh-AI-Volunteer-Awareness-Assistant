import streamlit as st
import google.generativeai as genai

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="NayePankh AI Assistant",
    page_icon="🤖",
    layout="wide"
)
try:
    st.image(
        "logo.avif",
        width=180
    )
except:
    st.warning("Logo not found")

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("⚙️ Configuration")

    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password"
    )

    st.markdown("---")

    st.subheader("About NGO")

    st.write("""
    NayePankh Foundation is a student-led NGO working on:

    • Education

    • Youth Empowerment

    • Skill Development

    • Social Awareness

    • Community Impact
    """)

    st.markdown("---")

    st.subheader("Project Objectives")

    st.write("""
    ✅ Automate NGO Queries

    ✅ Improve Volunteer Support

    ✅ Generate Awareness Content

    ✅ Increase User Engagement

    ✅ Demonstrate AI Implementation
    """)

# =====================================
# GEMINI CONFIG
# =====================================

if api_key:
    genai.configure(api_key=api_key)
if api_key:
    st.sidebar.success(
        "Gemini API Connected"
    )

# =====================================
# KNOWLEDGE BASE
# =====================================

with open("knowledge_base.txt","r",encoding="utf-8") as file:
    ngo_info = file.read()

# =====================================
# TITLE
# =====================================

st.title("🤖 NayePankh AI Volunteer & Awareness Assistant")
st.info(
    """
    This AI assistant helps volunteers, interns,
    donors and visitors quickly access NGO information,
    generate awareness campaigns and receive volunteer recommendations.
    """
)

# =====================================
# TABS
# =====================================

tab1, tab2, tab3 = st.tabs(
    [
        "🤖 AI Chatbot",
        "📢 Awareness Generator",
        "🙋 Volunteer Recommender"
    ]
)

# =====================================
# CHATBOT TAB
# =====================================

with tab1:

    st.subheader("Ask Questions About NayePankh Foundation")

    st.write("### Quick Questions")

    col1, col2 = st.columns(2)

    if "quick_question" not in st.session_state:
        st.session_state.quick_question = ""

    with col1:

        if st.button("What is NayePankh Foundation?"):
            st.session_state.quick_question = (
                "What is NayePankh Foundation?"
            )

        if st.button("Who is the founder?"):
            st.session_state.quick_question = (
                "Who is the founder?"
            )

    with col2:

        if st.button("How can I volunteer?"):
            st.session_state.quick_question = (
                "How can I volunteer?"
            )

        if st.button("Internship Benefits"):
            st.session_state.quick_question = (
                "What internship benefits are available?"
            )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.chat_input(
        "Ask about internships, volunteering, donations..."
    )

    prompt = None

    if user_input:
        prompt = user_input

    elif st.session_state.quick_question:
        prompt = st.session_state.quick_question
        st.session_state.quick_question = ""

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.write(prompt)

        if api_key:

            try:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
                    You are NayePankh Foundation AI Assistant.

                    Use ONLY the following NGO information.

                    {ngo_info}

                    User Question:
                    {prompt}

                    Answer as an official NayePankh Foundation AI Assistant.

                    Rules:
                    - Use only the provided NGO information.
                    - Be professional and concise.
                    - If information is unavailable, politely say it is not available in the knowledge base.
                    - Do not make up facts.
                    """
                )

                answer = response.text

            except Exception as e:

                answer = f"Error: {str(e)}"

        else:

            answer = (
                "Please enter your Gemini API Key in the sidebar."
            )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)

# =====================================
# AWARENESS GENERATOR
# =====================================

with tab2:

    st.subheader("AI Awareness Campaign Generator")

    topic = st.text_input(
        "Enter Awareness Topic"
    )

    if st.button("Generate Campaign Content"):

        if not api_key:

            st.warning(
                "Please enter Gemini API Key."
            )

        elif not topic:

            st.warning(
                "Please enter a topic."
            )

        else:

            try:

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
                    Create:

                    1. Awareness Message

                    2. Instagram Caption

                    3. LinkedIn Post

                    4. Five Hashtags

                    Topic:
                    {topic}
                    """
                )

                st.success(
                    "Campaign Content Generated"
                )

                st.write(response.text)

            except Exception as e:

                st.error(str(e))

# =====================================
# VOLUNTEER RECOMMENDER
# =====================================

with tab3:

    st.subheader(
        "Volunteer Recommendation System"
    )

    role = st.selectbox(
        "Who are you?",
        [
            "Student",
            "Teacher",
            "Developer",
            "Designer",
            "Working Professional"
        ]
    )

    interest = st.selectbox(
        "Select Interest Area",
        [
            "Education",
            "Technology",
            "Awareness",
            "Community Service"
        ]
    )

    if st.button(
        "Get Volunteer Recommendations"
    ):

        recommendations = {

            "Education": [
                "Teaching Support",
                "Student Mentoring",
                "Educational Content Creation"
            ],

            "Technology": [
                "Website Development",
                "Automation Projects",
                "AI-Based NGO Solutions"
            ],

            "Awareness": [
                "Social Media Campaigns",
                "Poster Design",
                "Awareness Programs"
            ],

            "Community Service": [
                "Volunteer Drives",
                "Fundraising Support",
                "Community Outreach"
            ]
        }

        st.success(
            f"Recommended Activities for {role}"
        )

        for item in recommendations[interest]:

            st.write(f"✅ {item}")

# =====================================
# FOOTER
# =====================================
st.markdown("---")

st.subheader("📞 Contact NayePankh Foundation")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("📧 contact@nayepankh.com")

with col2:
    st.write("📱 +91-8318500748")

with col3:
    st.write("🌐 https://nayepankh.com")