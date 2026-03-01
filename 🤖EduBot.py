import os

import streamlit as st
from streamlit_google_auth import Authenticate

from openai_key import get_openai_key
from chatbot import render_chatbot
from modules.sqlrag_module import get_tables 
from settings import initialize_settings, save_prompt
from modules.sqlrag_module import create_users_table, get_engine, upsert_user, get_user_by_email, create_pjs_points_table
from openai_key import get_google_key
from dotenv import load_dotenv

load_dotenv()

# import logging
# logging.basicConfig(level=logging.DEBUG)

st.set_page_config(
    page_title="EduBot",
    page_icon="🤖",
)

st.title('🤖🎓EduBot')

st.sidebar.title('🤖🎓EduBot')
st.sidebar.markdown("**Chatbot for personalizing teaching materials**")

st.sidebar.markdown(
    "EduBot🤖🎓 is a chatbot for students and teachers at the Faculty of Informatics in Pula. It uses Large Language Models (LLMs) and modern RAG techniques to retrieve relevant information and generate answers.\n\n"
    "EduBot can answer questions from documents stored in the knowledge base (📚Files). The user can add, delete, and define which files will be used to enrich EduBot's knowledge.\n\n"
    "The user can store information about themselves (👤User Profile) so that EduBot can adapt its answers, e.g., according to the user's programming knowledge.\n\n"
)


authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='edubot_cookie',
    cookie_key=os.getenv('COOKIE_KEY'),
    cookie_expiry_days=30,
    redirect_uri='http://localhost:8501',
)

authenticator.check_authentification()


if st.session_state['connected']:
    initialize_settings()
    get_google_key()
    
    #st.session_state["llm_selection"]["selected_model"]
    #st.session_state["llm_selection"]["selected_gpt"]
    #st.session_state["llm_selection"]["selected_embedding_model"]
    #st.session_state["intent_agent_settings"]["retriever_mode"]
    #st.session_state["intent_agent_settings"]["similarity_top_k"]
    #st.session_state["user_context_included"]
  
    email = st.session_state['user_info'].get('email')
    user_details = get_user_by_email(email) 
            
    if 'study_year' not in st.session_state["user_info"]:
        st.session_state["user_info"]["study_year"] = "1. prijediplomski"
    if 'about_me' not in st.session_state["user_info"]:
        st.session_state["user_info"]["about_me"] = ""
    if 'programming_knowledge' not in st.session_state["user_info"]:
        st.session_state["user_info"]["programming_knowledge"] = 0
    
    
    study_year = user_details.get('study_year') if user_details else "1. prijediplomski"
    about_me = user_details.get('about_me') if user_details else ""
    programming_knowledge = user_details.get('programming_knowledge') if user_details else 0

    st.session_state["user_info"]["study_year"] = study_year
    st.session_state["user_info"]["about_me"] = about_me
    st.session_state["user_info"]["programming_knowledge"] = programming_knowledge
    
def raptor_settings():
    st.radio(
        "RAPTOR Retriever Mode",
        options=["collapsed", "tree_traversal",],
        help="Choose how to search clusters in RAPTOR. The 'collapsed' approach places all nodes on the same level and evaluates node similarity simultaneously. The 'tree_traversal' approach uses a tree to search clusters and evaluates node similarity by tree level.",
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"retriever_mode": st.session_state["temp_retriever_mode"]}
        ),
        key="temp_retriever_mode"
    )
    st.number_input("Enter top-k", 
                    min_value=1, 
                    max_value=10,
                    help="Select the number of most relevant clusters RAPTOR will use for search.",  
                    key="temp_similarity_top_k",
                    value=st.session_state["intent_agent_settings"]["similarity_top_k"],
                    on_change=lambda: st.session_state["intent_agent_settings"].update(
                        {"similarity_top_k": st.session_state["temp_similarity_top_k"]} 
                    )
    )
    
    selected_embedding_model = st.radio(
                "Select the embedding model you want to use",
                ('models/text-embedding-004',),
                help="Embedding model that will be used for embedding clusters when building the RAPTOR tree and calling the RAPTOR Retriever. (Gemini-optimized)",
                
                on_change=lambda: st.session_state["llm_selection"].update(
                    {"selected_embedding_model": st.session_state["temp_selected_embedding_model"]}
                ),
                key="temp_selected_embedding_model",
            )

def sql_rag_settings():
    st.write("Check the database tables that will be used for SQL-RAG")
    
    # Tables which will be used for SQL-RAG        
    tables = get_tables()
    selected_tables = {}
    
    for table in tables:
        selected_tables[table] = st.checkbox(table, 
                                                key=f"sql_rag_table_{table}", 
                                                on_change= lambda: st.session_state["sql_rag_tables"].update(
                                                    {table: st.session_state[f"sql_rag_table_{table}"]}),
                                                value=st.session_state["sql_rag_tables"][table]
                                                )

def web_scraper_settings():
    st.write("Web Scraper Settings (To-Do)")
    
    
    slider_value = st.slider(
        "Select the maximum number of the latest posts you want me to study from the University/Faculty pages",
        min_value=1, 
        max_value=100,
        value=st.session_state["web_scraper_settings"]["max_number_of_posts"],
        key="temp_web_scraper_max_number_of_posts",
        on_change= lambda: st.session_state["web_scraper_settings"].update(
            {"max_number_of_posts": st.session_state["temp_web_scraper_max_number_of_posts"]}
        )
    )
    
    selected_web_url = st.radio(
        label="Select News Source",
        options=["https://www.elsevier.com/products/journals"],
        help="Select the page of the University of Pula component you want me to study.",
        on_change=lambda: st.session_state["web_scraper_settings"].update(
            {"selected_web_url": st.session_state["temp_selected_web_url"]}
        ),
        key="temp_selected_web_url",
    )

def intent_recognition_settings():
    st.checkbox("Use whole conversation as context", key="use_full_conversation", value=False)
    st.checkbox("Use user data as context", key="user_context_included", value=True)
    st.text_area(
        label="Direct LLM Prompt",
        value=st.session_state["intent_agent_settings"]["direct_llm_prompt"],
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"direct_llm_prompt": st.session_state["temp_direct_llm_prompt"]}
        ),
        key="temp_direct_llm_prompt", 
        height=200
    )
    st.button(label="Save", key="btn_save_direct_llm_settings", type="primary", on_click=lambda: save_prompt("./prompts/DIRECT_LLM_PROMPT.txt", st.session_state["temp_direct_llm_prompt"]))

    st.text_area(
        label="Query Engine Description",
        value=st.session_state["intent_agent_settings"]["llm_query_tool_description"],
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"llm_query_tool_description": st.session_state["temp_llm_query_tool_description"]}
        ),
        key="temp_llm_query_tool_description", 
        height=200
    )
    st.button(label="Save", key="btn_save_query_engine_desc", type="primary", on_click=lambda: save_prompt("./prompts/LLM_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_llm_query_tool_description"]))

    st.divider()
    
    use_raptor = st.checkbox("Use RAPTOR Engine", 
                                value= st.session_state["intent_agent_settings"]["use_raptor"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_raptor": st.session_state["temp_use_raptor"]}
                                ), 
                                key="temp_use_raptor")
    if use_raptor:
        st.text_area(
            label="RAPTOR Engine Description",
            value=st.session_state["intent_agent_settings"]["raptor_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"raptor_query_tool_description": st.session_state["temp_raptor_query_tool_description"]}
            ),
            key="temp_raptor_query_tool_description",
            height=200
        )
    st.button(label="Save", key="btn_save_raptor_settings", type="primary", on_click=lambda: save_prompt("./prompts/RAPTOR_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_raptor_query_tool_description"]))
    st.divider()
    
    use_sql_rag = st.checkbox("Use SQL-RAG Engine", 
                                value= st.session_state["intent_agent_settings"]["use_sql_rag"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_sql_rag": st.session_state["temp_use_sql_rag"]}
                                ), 
                                key="temp_use_sql_rag")
    if use_sql_rag:
        st.text_area(
            label="SQL-RAG Engine Description",
            value=st.session_state["intent_agent_settings"]["sql_rag_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"sql_rag_query_tool_description": st.session_state["temp_sql_rag_query_tool_description"]}
            ),
            key="temp_sql_rag_query_tool_description",
            height=200
        )
        
    st.button(label="Save", key="btn_save_sqlrag_settings", type="primary", on_click=lambda: save_prompt("./prompts/SQL_RAG_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_sql_rag_query_tool_description"]))

    use_web_scraper = st.checkbox("Use Web Scraper Engine", 
                                value= st.session_state["intent_agent_settings"]["use_web_scraper"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_web_scraper": st.session_state["temp_use_web_scraper"]}
                                ), 
                                key="temp_use_web_scraper")
    if use_web_scraper:
        st.text_area(
            label="Web Scraper Engine Description",
            value=st.session_state["intent_agent_settings"]["web_scraper_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"sql_web_scraper_query_tool_description": st.session_state["temp_web_scraper_query_tool_description"]}
            ),
            key="temp_web_scraper_query_tool_description",
            height=200
        )
        
    st.button(label="Save", key="btn_save_webscraper_settings", type="primary", on_click=lambda: save_prompt("./prompts/WEB_SCRAPER_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_web_scraper_query_tool_description"]))
    
if st.session_state['connected']:
    
    col1, col2 = st.columns([3, 1])

    if "google_api_key" not in st.session_state:
        st.session_state["google_api_key"] = os.getenv("GOOGLE_API_KEY") or ""
        
    if(st.session_state["llm_selection"]["selected_model"] == "GPT"):
        # Initialize key early
        st.session_state["openai_api_key"] = get_openai_key()
        
    with col1:
        st.write(f"Hey, {st.session_state['user_info'].get('name')}👋🏻")
        st.write("Login successful! Hurray! 🎉")
        st.write("If you don't understand the syllabus of a course, are looking for an explanation of theory from a script or have a problem with programming, feel free to ask me!😊")

    with col2:
        debug_mode_on = st.toggle("Under the hood", key="debug_mode", value=True)

    with st.sidebar:
        if st.button('Logout'):
            authenticator.logout()
        container = st.sidebar.container(border=True)
        
        with st.expander("Settings | Model Selection", expanded=False):
            st.radio(
                "Select the LLM you want to use to power EduBot🤖",
                options=["Gemini 2.0 Flash", "Gemini 2.5 Flash", "Gemini 2.5 Pro", "mistral:7b", "gemma:7b", "llama3:8b", "Claude 3 Opus", "Claude 3 Sonnet", "Claude 3 Haiku"],
                on_change=lambda: st.session_state["llm_selection"].update(
                    {"selected_model": st.session_state["temp_selected_model"]}
                ),
                help="",
                key="temp_selected_model",
            )
            if "Gemini" in st.session_state["llm_selection"]["selected_model"]:
                google_key = st.text_input("Google AI API Key", type="password", value=st.session_state["google_api_key"], help="Get your Gemini API key from Google AI Studio")
                if google_key:
                    st.session_state["google_api_key"] = google_key
                    os.environ["GOOGLE_API_KEY"] = google_key
                st.info("Powered by Google Gemini 🚀")

                
            elif(st.session_state["llm_selection"]["selected_model"] == "Mistral"):
                st.success("Mistral7B model selected - local deployment via Ollama🦙")
            elif(st.session_state["llm_selection"]["selected_model"] == "Gemma"):
                st.success("Gemma model selected - local deployment via Ollama🦙")
                
        with st.expander("Settings | Intent Recognition", expanded=False):
            intent_recognition_settings()

        with st.expander("Settings | RAPTOR", expanded=False):
            raptor_settings()
            
        with st.expander("Settings | SQL-RAG", expanded=False):
            sql_rag_settings()
        
        with st.expander("Settings | Web Scraper", expanded=False):
            web_scraper_settings()
            
    render_chatbot()

    # Reset conversation.
    if(st.button("Reset Conversation")):
        st.session_state["messages"] = [{"role": "assistant", "content": "I'm here! How can I help you?🤖"}]
        st.rerun()

else:
    st.write("Hi👋🏻 To use EduBot, you must log in.")
    
    authenticator.login(justify_content="start")
