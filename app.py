import streamlit as st
import openai


# Define the chatbot function
def chat_with_model(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
    )
    return response.choices[0].message.content

# Streamlit app code
def main():
    st.title("Chatbot Demo")

    # Initialize session state for messages if it doesn't exist
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

        # Set initial system message with a specific role (e.g., Assistant)
        initial_message = {
            "role": "system",
            "content": "You are Batman. Your job is to save Gotham City from the Joker. The user is Gotham City's police chief. Help him with the job."
        }
        st.session_state['messages'].append(initial_message)

    # Render chat history container first	
    chat_history_container = st.container()

    # Display existing conversation		
    with chat_history_container:
        for message in st.session_state["messages"]:
            if(message["role"]=="user"):
                st.markdown(f"**You**: {message['content']}")
            elif (message["role"]=="assistant"):
                st.markdown(f"_Assistant_: {message['content']}")	    		

    # Add user input at the bottom of the page		    
    st.write("Type your message below:")
    user_input = st.text_input("Enter", key=len(st.session_state["messages"]))

    if user_input:
        # Append user message to the conversation
        new_message = {"role": "user", "content": user_input}
        st.session_state['messages'].append(new_message)

        # Get chatbot's response and append it to the conversation
        bot_response = chat_with_model(st.session_state['messages'])

        assistant_response = {"role": "assistant", "content": bot_response}
        st.session_state["messages"].append(assistant_response)

        # We need to manually rerun the Streamlit script so that Streamlit can process the new state and display it
        st.experimental_rerun()

if __name__ == "__main__":
    main()
