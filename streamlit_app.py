import os
import streamlit as st
from openai import OpenAI

# Show title and description.
st.set_page_config(page_title="Chatbot", page_icon="💬")
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that demonstrates model selection, system prompts, temperature and token limits. "
    "Provide an OpenAI API key to use the app."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
# fallback to environment variable if provided
if not openai_api_key:
    openai_api_key = os.environ.get("OPENAI_API_KEY", "")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Track selected model, system prompt and user-configurable settings.
    MODEL_OPTIONS = [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0613",
    ]

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = (
            "You are a helpful assistant. Answer concisely and clearly."
        )
    if "model" not in st.session_state:
        st.session_state.model = "gpt-3.5-turbo"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "max_tokens" not in st.session_state:
        st.session_state.max_tokens = 512
    if "streaming" not in st.session_state:
        st.session_state.streaming = True

    # Sidebar: model settings in an expander (collapsible)
    with st.sidebar.expander("Model Settings", expanded=True):
        st.session_state.model = st.selectbox("Model", MODEL_OPTIONS, index=MODEL_OPTIONS.index(st.session_state.model) if st.session_state.model in MODEL_OPTIONS else 1)
        st.session_state.system_prompt = st.text_area("System prompt", st.session_state.system_prompt, height=150)
        st.session_state.temperature = st.slider("Temperature", min_value=0.0, max_value=1.5, step=0.01, value=float(st.session_state.temperature))
        st.session_state.max_tokens = st.slider("Max tokens", min_value=64, max_value=4096, step=1, value=int(st.session_state.max_tokens))
        st.session_state.streaming = st.checkbox("Enable streaming responses", value=st.session_state.streaming)
        st.button("Reset Conversation", on_click=lambda: st.session_state.messages.clear())

    # Ensure the first message is the system prompt so that model sees it as system.
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "system", "content": st.session_state.system_prompt})
    else:
        # make sure system prompt remains first (update if changed)
        if st.session_state.messages[0]["role"] == "system":
            st.session_state.messages[0]["content"] = st.session_state.system_prompt

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    # Input prompt field
    if prompt := st.chat_input("Type a message and press Enter..."):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the selected model and settings.
        response_args = dict(
            model=st.session_state.model,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            temperature=float(st.session_state.temperature),
            max_tokens=int(st.session_state.max_tokens),
        )
        # Stream or non-stream response
        try:
            if st.session_state.streaming:
                stream = client.chat.completions.create(stream=True, **response_args)
            else:
                stream = client.chat.completions.create(stream=False, **response_args)
        except Exception as e:
            st.error(f"Error from API: {e}")
            st.stop()

        # Stream the response to the chat using `st.write_stream`, then store it in
        # session state. If streaming disabled, the result is a single response.
        with st.chat_message("assistant"):
            if st.session_state.streaming:
                response = st.write_stream(stream)
            else:
                # The client returns the whole response at once - extract text.
                def _extract_text(resp):
                    try:
                        return resp.choices[0].message.content
                    except Exception:
                        try:
                            return resp["choices"][0]["message"]["content"]
                        except Exception:
                            return str(resp)

                response_text = _extract_text(stream)
                response = response_text
                st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response})
