"""
GrabyAI Platform Assistant - Main Streamlit Application
"""
import streamlit as st
import os

from config.settings import (
    PLATFORM_NAME, 
    SUPPORT_EMAIL, 
    RATE_LIMIT_REQUESTS, 
    RATE_LIMIT_WINDOW
)
from utils.validation import validate_api_key, sanitize_input
from utils.rate_limiter import RateLimiter
from utils.logger import setup_logger
from agent.agent_setup import initialize_agent

# Setup
logger = setup_logger(__name__)

st.set_page_config(
    page_title=f"{PLATFORM_NAME} Assistant", page_icon="𖣐", layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "rate_limiter" not in st.session_state:
    st.session_state.rate_limiter = RateLimiter()

# Sidebar
with st.sidebar:
    st.title("Configuration")  # Removed emoji
    api_key = st.text_input("OpenAI API Key", type="password")

    if api_key:
        if not validate_api_key(api_key):
            st.error("Invalid API key format")
        else:
            os.environ["OPENAI_API_KEY"] = api_key
            logger.info("API key configured")

    st.markdown("---")
    st.markdown("### Get Expert Help")
    st.markdown(
        f"""
    **Join our WhatsApp Community**
    
    Email: {SUPPORT_EMAIL}
    """
    )

    st.markdown("---")
    st.markdown("### Usage Stats")
    rate_limiter = st.session_state.rate_limiter
    st.metric("Total Queries", rate_limiter.get_total())
    st.metric("Remaining", f"{rate_limiter.get_remaining()}/{RATE_LIMIT_REQUESTS}")

    st.markdown("---")
    st.markdown(f"### About {PLATFORM_NAME}")
    st.markdown("""
    Your platform for designer resale arbitrage.
    
    **Security:**
    - Rate limiting
    - Input validation
    - No data storage
    
    All items verified by AI + authenticators.
    """)

# Main content
st.title(f"𖣐 {PLATFORM_NAME} Platform Assistant")
st.markdown("Your guide to designer resale success")

# Check API key
if not api_key:
    st.warning("Please enter your OpenAI API key in the sidebar")
    st.info("This is a demo for Turing College. In production, keys are managed server-side.")
    st.stop()

# Initialize agent
try:
    if st.session_state.agent is None:
        with st.spinner("Initializing assistant..."):
            agent, vectorstore = initialize_agent(api_key)
            st.session_state.agent = agent
            st.session_state.vectorstore = vectorstore
        st.success("Assistant is now ready.")
        logger.info("Agent initialized")
except Exception as e:
    st.error(f"Error initializing assistant: {str(e)}")
    logger.error(f"Initialization error: {str(e)}")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about GrabyAI, authentication, pricing..."):

    # Rate limiting
    if not st.session_state.rate_limiter.check_limit():
        st.error(f"""
        ⚠️ **Rate Limit Reached**
        
        You've exceeded {RATE_LIMIT_REQUESTS} requests in {RATE_LIMIT_WINDOW} seconds.
        Please wait before sending more messages.
        """)
        logger.warning("Rate limit exceeded")
        st.stop()

    # Sanitize input
    prompt = sanitize_input(prompt)

    if len(prompt) < 3:
        st.warning("Please enter a valid question (min 3 characters)")
        st.stop()

    logger.info(f"User query: {prompt[:100]}...")

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response_text = ""
                for event in st.session_state.agent.stream(
                    {"messages": [{"role": "user", "content": prompt}]},
                    stream_mode="values"
                ):
                    last_message = event["messages"][-1]
                    if hasattr(last_message, 'content') and last_message.content:
                        response_text = last_message.content

                logger.info("Response generated successfully")
                st.markdown(response_text)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text
                })

            except Exception as e:
                error_msg = "Error processing request. Please try again."
                logger.error(f"Response error: {str(e)}")
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })

# Sidebar examples
with st.sidebar:
    st.markdown("---")
    st.markdown("### Example Questions")

    examples = [
        "How does Graby AI work?",
        "How do I authenticate Margiela?",
        "Calculate profit: buy £200, sell £450",
        "What do Rick Owens jackets sell for?",
        "Tips for listing photos?",
    ]

    for example in examples:
        if st.button(example, key=example, use_container_width=True):
            # Add to messages
            st.session_state.messages.append({"role": "user", "content": example})

            # Trigger response immediately
            with st.spinner("Thinking..."):
                try:
                    response_text = ""
                    for event in st.session_state.agent.stream(
                        {"messages": [{"role": "user", "content": example}]},
                        stream_mode="values",
                    ):
                        last_message = event["messages"][-1]
                        if hasattr(last_message, "content") and last_message.content:
                            response_text = last_message.content

                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_text}
                    )
                except Exception as e:
                    logger.error(f"Error: {str(e)}")

            st.rerun()  # This makes it show immediately
