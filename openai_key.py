import streamlit as st
from dotenv import load_dotenv
import os

def get_openai_key():
    if 'use_openai_env' not in st.session_state:
        st.session_state.use_openai_env = True
    
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
        
    # Check if we should load from environment (default to True)
    if st.session_state.use_openai_env:
        load_dotenv(override=True)
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            st.error("Error: OpenAI API key is not set in the environment.")
            st.write("> Please set your OpenAI API key in the .env file or enter the key manually.")
            st.stop()
        else:
            # Clean the key: strip quotes and whitespace
            openai_api_key = openai_api_key.strip().strip("'").strip('"')
            st.session_state.openai_api_key = openai_api_key
    else:
        openai_api_key = st.text_input("OpenAI API key", type="password", value=st.session_state.openai_api_key)
        if not openai_api_key:
            st.write("> However, before you continue, please enter your OpenAI API key. If you don't have one, you can get it at [OpenAI](https://platform.openai.com/signup).")
            st.error("Error: I do not have the OpenAI API key.")
            st.stop()
        else:
            st.session_state.openai_api_key = openai_api_key
    
    os.environ['OPENAI_API_KEY'] = st.session_state.openai_api_key
    return st.session_state.openai_api_key

def get_google_key():
    if 'google_api_key' not in st.session_state:
        st.session_state.google_api_key = ""
        
    # If session state is empty, try loading from .env
    if not st.session_state.google_api_key:
        load_dotenv(override=True)
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if google_api_key:
            st.session_state.google_api_key = google_api_key.strip().strip("'").strip('"')
    
    # Always ensure the environment variable matches the sanitized session state
    if st.session_state.google_api_key:
        os.environ['GOOGLE_API_KEY'] = st.session_state.google_api_key
        
    return st.session_state.google_api_key

def get_groq_key():
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = ""
        
    # If session state is empty, try loading from .env
    if not st.session_state.groq_api_key:
        load_dotenv(override=True)
        groq_api_key = os.getenv('GROQ_API_KEY')
        if groq_api_key:
            st.session_state.groq_api_key = groq_api_key.strip().strip("'").strip('"')
    
    # Always ensure the environment variable matches the sanitized session state
    if st.session_state.groq_api_key:
        os.environ['GROQ_API_KEY'] = st.session_state.groq_api_key
        
    return st.session_state.groq_api_key
