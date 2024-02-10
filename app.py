from langchain import OpenAI 
from langchain.chains import ConversationChain 
from langchain.chains.conversation.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
import streamlit as st 
from streamlit_chat import message #this will enable us to have a chat-like kind of conversation

#session to session variables 
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None 

#session to session messages 
#The code below initializes an empty list for messages to which we will later append the user 
#input and the model response so that we can show it on the screen of the application 
#as the user interacts with the AI 
if 'messages' not in st.session_state:
    st.session_state['messages']=[]


#Create a new session variable called api key to allow the user to input their own api key 
if 'API_key' not in st.session_state:
    st.session_state['API_key']='' #This will be an empty string type api key to be filled by the user 

#IMPLEMENTATION OF UI INTERPHASE 

#Setting page title and header 
st.set_page_config(page_title = "Chat GPT Clone" , page_icon = ":robot_face:")
st.markdown("<h1 style = 'text-align: center;'>How can I help you?</h1>", unsafe_allow_html=True)

#The following allows us to set the sidebar implemented.
st.sidebar.title("😎")
st.session_state['API_key'] = st.sidebar.text_input("What is your API key?", type = "password")
summarize_button = st.sidebar.button("Summarize the conversation", key = 'summarize')

if summarize_button: 
    summarize_placeholder = st.sidebar.write("Nice chatting with you! :\n\n" + st.session_state['conversation'].memory.buffer)

#import os 
#os.environ['OPENAI_API_KEY']="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"

def get_response(userInput, api_key):

    if st.session_state['conversation'] is None: 
        #The following will be executed (initialized) only when the session state of conversation is None. 
        #if we do not do that, then everytime the user asks a question, the variables below will be initialized 
        #again and therefore we will not be able to retain the information given by the user 
        llm = OpenAI(
            temperature = 0, 
            openai_api_key = api_key,
            model_name = "gpt-3.5-turbo-instruct"
        )

        #We are using session variables in here because we want to retain the information 
        #from session to session 
        st.session_state['conversation'] = ConversationChain(
            llm = llm,
            verbose = True,
            memory = ConversationSummaryMemory(llm = llm)
        )

    response = st.session_state['conversation'].predict(input = userInput)
    print(st.session_state['conversation'].memory.buffer)

    return response

#CONTAINERS 
#This function allows us to have containers which will package all the things we want in one block 
response_container = st.container() #for response

container = st.container() #for input 

with container: #which container you want to populate 
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key='input', height = 50)
        submit_button = st.form_submit_button(label = "Send")

        if submit_button: 
            #The three lines of code below allows us to save the chat history between the AI and the user 
            #Without it we will only be able to see one response at a time
            st.session_state['messages'].append(user_input)
            model_response=get_response(user_input, st.session_state['API_key'])
            st.session_state['messages'].append(model_response)
            with response_container: 
                #make it beautiful in a conversational way 
                for i in range(len(st.session_state["messages"])):
                    if (i%2)==0:
                        #message is used instead of write to allow us to have a beautifully written conversation
                        #This is coming from the streamlit_chat module 
                        message(st.session_state['messages'][i], is_user=True, key = str(i) + "_user")
                    else: 
                        message(st.session_state['messages'][i], key=str(i)+"_AI")





#NOTES TO REMEMBER 

#Remember that you always have to think about what is called code Modularization 
#if you do not care about the code modularization, you will have a high bill on your credit card 
#because everytime you refresh the page the code will run and you will be charged for your tokens 

#Always start simple with hardcoded values
#Then build the UI interphase 
#Make sure that you account for code modularization 
#Then make the inputs dynamic!

#Be careful of MODEL HALLUCINATIONS 
#In our example, we should finetune our prompt so that if you ask the AI what your name is,
#it actually says I do not know instead of giving you a random name 

#Be sure that the model is able to retain earlier information
#To retain the values from session to session on streamlit, we have to use SESSION VARIABLES

#SO TO HANDLE THE DATA MANAGEMENT, use SESSION VARIABLES IN STREAMLIT 

#THE MESSAGE library from streamlit_chat can be used to have the conversation between the human and the AI 
#more beautiful!!!!! 


