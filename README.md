# 💬 Chatbot template

A simple Streamlit app that shows how to build a chatbot using OpenAI's GPT-3.5.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://chatbot-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```bash
   pip install -r requirements.txt
   ```

2. Provide an OpenAI API Key

   You can either paste your API key in the app when prompted or set the `OPENAI_API_KEY` environment variable.

   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

3. Run the app

   ```bash
   streamlit run streamlit_app.py
   ```

Usage notes

- **Model Settings:** Open the sidebar and expand "Model Settings". There is a dropdown to change models on the fly.
- **System Prompt:** Use the text area to edit the system prompt (it updates the first message in the conversation).
- **Temperature:** Adjust the slider to change randomness (0-1.5).
- **Max tokens:** Control the returned token limit for the assistant.
- **Streaming:** Toggle live streaming in the sidebar. Reset conversation to clear messages.
