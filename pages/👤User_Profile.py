import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_google_auth import Authenticate
from sqlalchemy import MetaData, Table, insert

from modules.sqlrag_module import create_users_table, get_engine, upsert_user, get_user_by_email, create_pjs_points_table

st.set_page_config(
    page_title="EduBot - User Profile",
    page_icon="🤖",
)

load_dotenv()

authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='edubot_cookie',
    cookie_key=os.getenv('COOKIE_KEY'),
    cookie_expiry_days=30,
    redirect_uri='http://localhost:8501',
)

authenticator.check_authentification()

create_users_table()

email = st.session_state['user_info'].get('email')
user_details = get_user_by_email(email) 

if st.session_state['connected']:
    st.title('👤User Profile')
    st.markdown(f'Hey {st.session_state["user_info"].get("name")} 👋')
    st.markdown('Here you can update some of your personal information.')

    study_year = user_details.get('study_year') if user_details else "1st Undergraduate"
    about_me = user_details.get('about_me') if user_details else ""
    programming_knowledge = user_details.get('programming_knowledge') if user_details else 0

    with st.form(key="profile_form"):
        name = st.text_input("Full Name", value=st.session_state['user_info'].get('name'), disabled=True)
        email = st.text_input("Email", value=st.session_state['user_info'].get('email'), disabled=True)
        study_year = st.selectbox("Year of Study", ["1st Undergraduate", "2nd Undergraduate", "3rd Undergraduate", "1st Graduate", "2nd Graduate"], index=["1st Undergraduate", "2nd Undergraduate", "3rd Undergraduate", "1st Graduate", "2nd Graduate"].index(study_year), key="study_year")
        about_me = st.text_area("About Me", value=about_me, key="about_me", help="Describe what kind of student you are and how you learn best.")
        programming_knowledge = st.slider("Programming Knowledge",
                                          min_value=0,
                                          max_value=10,
                                          value=programming_knowledge,
                                          key="programming_knowledge",
                                          help="Rate your programming knowledge from 0 to 10. Depending on your knowledge, I will adjust my answers. [0] - absolute beginner, [10] - expert/can write my own language")
        submit_button = st.form_submit_button("Update", type="primary")

        if submit_button:
            user_info = {
                "first_name": name.split(" ")[0],
                "last_name": name.split(" ")[1],
                "email": email,
                "study_year": study_year,
                "about_me": about_me,
                "programming_knowledge": programming_knowledge
            }
            upsert_user(user_info)  
            st.success("Data successfully updated!")

else:
    st.error("You must be logged in for this!")
