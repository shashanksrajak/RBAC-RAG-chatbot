import streamlit as st
import requests
import json

st.set_page_config(
    page_title="FinSolve Technologies Chatbot",
    page_icon="🤖",
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

BACKEND_URL = "http://localhost:6001"

# Function to verify credentials with backend


def verify_credentials_with_backend(username, password):
    try:
        # Test authentication with a simple request to backend

        response = requests.get(
            f"{BACKEND_URL}/login", auth=(username, password), timeout=10)
        return response.status_code == 200
    except:
        return False


# Authentication page
if not st.session_state.authenticated:
    st.title("🔐 Login to FinSolve Technologies Chatbot")
    st.markdown("Please enter your credentials to access the chatbot.")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if username and password:
                # Store credentials for header use
                st.session_state.username = username
                st.session_state.password = password

                # Verify credentials with backend
                if verify_credentials_with_backend(username, password):
                    st.session_state.authenticated = True
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error(
                        "❌ Invalid credentials or backend connection failed.")
            else:
                st.error("❌ Please enter both username and password.")

else:
    # Main chatbot interface
    # Header with logout option
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🤖 FinSolve Technologies Chatbot")
        st.markdown(
            f"Welcome, **{st.session_state.username}**! Ask me anything about our knowledge base.")
    with col2:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.password = ""
            st.session_state.messages = []
            st.rerun()

    # Function to call FastAPI backend with auth headers
    def get_bot_response(user_message):
        try:
            print("user message", user_message)

            response = requests.post(
                f"{BACKEND_URL}/chat?message={user_message}",
                auth=(st.session_state.username, st.session_state.password),
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("message", {}).get(
                    "answer", "Sorry, I couldn't generate a response.")
                sources = data.get("message", {}).get("sources", [])

                # Format the response with answer and sources
                formatted_response = answer
                if sources:
                    formatted_response += f"\n\n**Sources:**\n"
                    for source in sources:
                        formatted_response += f"• {source}\n"

                return formatted_response
            elif response.status_code == 401:
                st.error("❌ Authentication failed. Please login again.")
                st.session_state.authenticated = False
                st.rerun()
            else:
                return f"Error: {response.status_code} - {response.text}"

        except requests.exceptions.ConnectionError:
            return "❌ Cannot connect to the backend server. Please make sure it's running."
        except requests.exceptions.Timeout:
            return "⏱️ Request timed out. Please try again."
        except Exception as e:
            return f"❌ An error occurred: {str(e)}"

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_response = get_bot_response(prompt)
            st.markdown(bot_response)

        # Add bot response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": bot_response})

    # Sidebar with additional options
    with st.sidebar:
        st.header("Chat Options")

        # User info
        st.info(f"👤 Logged in as: **{st.session_state.username}**")

        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()

        # Backend status check
        st.header("Backend Status")
        if st.button("🔍 Check Connection"):
            try:
                health_response = requests.get(
                    f"{BACKEND_URL}", timeout=5)
                if health_response.status_code == 200:
                    st.success("✅ Backend is running!")
                else:
                    st.error("❌ Backend is not responding correctly")
            except:
                st.error("❌ Cannot connect to backend")

        # Chat statistics
        st.header("Chat Statistics")
        st.metric("Messages sent", len(
            [msg for msg in st.session_state.messages if msg["role"] == "user"]))
        st.metric("Bot responses", len(
            [msg for msg in st.session_state.messages if msg["role"] == "assistant"]))
