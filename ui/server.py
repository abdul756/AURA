import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))
import requests
import streamlit as st
from config.application_config import ApplicationConfig
from utils.upload_file_to_drive import upload_file_to_drive
# from dotenv import load_dotenv

# # Load environment variables
# # load_dotenv()
api_host = ApplicationConfig.PATHWAY_REST_CONNECTOR_HOST
api_port = ApplicationConfig.PATHWAY_REST_CONNECTOR_PORT


# Append necessary system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

# Load environment variables, if needed
# from dotenv import load_dotenv
# load_dotenv()

# Custom CSS for message aesthetics



# Streamlit UI elements
st.set_page_config(page_title="AURA")
st.title("Adaptive Understanding and Resource Assistant")

# Inject custom CSS for sidebar background color

st.markdown("""
<style>
h1 {
    font-size: 32px !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# st.sidebar.image("./assets/logo_round.png", width=50)
# logo_path = "path_or_url_to_your_logo.png"

# HTML and CSS to make the image circular and center-align it along with the text
circular_logo_html = f"""
<div style="text-align: center;">
    <img src="https://drive.google.com/thumbnail?id=18X6E7Ts93V-VkdRFHxIA6K6Zcly15j-3" alt="Logo" style="border-radius: 50%; width: 100px; height: 100px; object-fit: cover; display: inline-block;">
    <br>
    <h1 style="margin-top: 10px;">AURA</h1>
</div>
"""

# Use Markdown to render the HTML and CSS
st.sidebar.markdown(circular_logo_html, unsafe_allow_html=True)
# st.sidebar.markdown("<h1 style='text-align: center;'>AURA</h1>", unsafe_allow_html=True)
# Custom CSS for sidebar and user messages

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #ffdab9;
    }
    /* This targets markdown cells, which you could use for displaying messages */
    .markdown-text-container {
        font-size: 20px; /* Increase font size */
    }
    /* Style for the active input box */
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50; /* Change color when typing (focus state) */
        box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
    }
            
    /* Style for all buttons in the app */
    .stButton>button {
        font-weight: bold; /* Make button text bold */
        background-color: #f0f0f0; /* Light shade for the button background */
        border: 1px solid #4CAF50; /* Optional: Adds a border */
        color: #4CAF50; /* Optional: Changes the text color */
    }
    /* Button hover effect */
    .stButton>button:hover {
        background-color: #e6e6e6; /* Slightly darker shade when hovered */
    }
            
    .main-title {
    text-align: center;
    font-size: 20px; /* Adjust the size of 'AURA' text here */
    }
    .main-title {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    difficulty_level = st.radio('**Select your difficulty level**', options=['Novice', 'Skilled', 'Expert'], 
          horizontal=True)
    mode= st.radio('**Select your Mode**', options=['Basic Mode', 'Deep Dive Mode'], 
          horizontal=True)
    context_keywords = st.text_input(
    "Enter context keywords (Optional):",
    placeholder="deep learning, machine learing",
    help="Provide context keywords for better response."
)
  
    uploaded_file = st.file_uploader("Choose a PDF or DOC file (Optional)", type=['pdf', 'doc', 'docx'])

    if uploaded_file is not None:
        file_id = upload_file_to_drive(uploaded_file.name, uploaded_file.type, uploaded_file)
        if file_id:
            st.success('File has been uploaded successfully.')
        else:
            st.error('Failed to upload the file.')
    
    st.markdown("""
    <style>
    .enhance-aura {
        font-size: 16px; /* Adjust font size as needed */
    }
    </style>
    
    <div class="enhance-aura">
        <p><strong>Upload a PDF or DOC file to enhance AURA's learning.</strong> This optional step improves response accuracy and personalization.</p>
    </div>
""", unsafe_allow_html=True)

# Parse context keywords
context_keywords_list = [kw.strip() for kw in context_keywords.split(",") if kw.strip()]



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
           st.markdown(f"**User:** {message['content']}", unsafe_allow_html=True)

        else:
            st.markdown(f"**Assistant:** {message['content']}", unsafe_allow_html=True)

# React to user input
user_input = st.text_input("How can I assist you today?", key="user_input")
if st.button("Ask"):
    # Display user message in chat message container
    with st.container():
        st.markdown(f"**User:** {user_input}")

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare request data
    data = {
        "query": user_input,
        "user": "user",
        "difficulty_level": difficulty_level,
        "context_keywords": context_keywords_list,
        "mode": mode
    }

    # Send request to the backend
    url = f"http://{api_host}:{api_port}/"
    response = requests.post(url, json=data)

    if response.status_code == 200:
        response_data = response.json()
        with st.container():
            st.markdown(f"**Assistant:** {response_data}")
        st.session_state.messages.append({"role": "assistant", "content": response_data})
    else:
        st.error(f"Failed to retrieve data. Status code: {response.status_code}")

# Note: Adjust the `response_data['result']` based on the actual key where the response text is stored in your API's response.
