import streamlit as st
import openai
import random


# Define the chatbot function
def chat_with_model(messages):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages,
        temperature=0.9,
        max_tokens=500,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Streamlit app code
def main():
    st.title("AI Master Brewer")

    # Initialize session state for messages if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

        # Set initial system message with a specific role (e.g., Assistant)
        initial_message = {
            "role": "system",
            "content": "You are the AI Master Brewer. Your job is to answer questions from and share knowledge about whisky in shakespearian language to the user. The user is Spirited Drinker. Ask me about whisky!"
        }
        st.session_state['messages'].append(initial_message)

    # Render chat history container first
    chat_history_container = st.container()

    # Display existing conversation
    with chat_history_container:
        for message in st.session_state["messages"]:
            if message["role"] == "user":
                st.markdown(f"**Spirited Drinker**: {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"_AI Master Brewer_: {message['content']}")

    # Add user input at the bottom of the page
    st.write("Ask me about Whisky:")
    user_input = st.text_input("Enter", key=len(st.session_state["messages"]))

    if user_input:
        # Append user message to the conversation
        new_message = {"role": "user", "content": user_input}
        st.session_state['messages'].append(new_message)

        # Get chatbot's response and append it to the conversation
        conversation_history = "\n".join([message['content'] for message in st.session_state['messages']])
        bot_response = chat_with_model(conversation_history)

        assistant_response = {"role": "assistant", "content": bot_response}
        st.session_state["messages"].append(assistant_response)

        # We need to manually rerun the Streamlit script so that Streamlit can process the new state and display it
        st.experimental_rerun()


if __name__ == "__main__":
    main()
