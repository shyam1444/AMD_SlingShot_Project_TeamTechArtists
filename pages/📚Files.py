import streamlit as st
import pandas as pd
import os
from openai_key import get_openai_key
import time
from modules.raptor_module import get_raptor

from settings import initialize_settings

st.set_page_config(
    page_title="EduBot - Files",
    page_icon="🤖",
)

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = get_openai_key()

UPLOAD_DIR = "uploaded_files"
STATE_FILE = "file_state.csv"


if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        with st.spinner(f'Saving {uploaded_file.name}...'):
            file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Saved file: {uploaded_file.name}")
        update_state_file(uploaded_file.name, False)

def update_state_file(file_name, is_used):
    df = load_state_file()

    if file_name not in df["File Name"].values:
        new_row = pd.DataFrame({"File Name": [file_name], "is_used": [is_used]})
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df.loc[df["File Name"] == file_name, "is_used"] = is_used

    df.to_csv(STATE_FILE, index=False)
    st.session_state["files_changed"] = True

def load_state_file():
    if os.path.exists(STATE_FILE):
        df = pd.read_csv(STATE_FILE)
        if "Naziv datoteke" in df.columns:
            df = df.rename(columns={"Naziv datoteke": "File Name"})
        return df
    else:
        return pd.DataFrame(columns=["File Name", "is_used"])

def list_uploaded_files():
    files = load_state_file()
    if files.empty:
        st.write("Empty! 😔")
        return files
    else:
        edited_df = st.data_editor(data=files,
                                   num_rows="dynamic",
                                   key="files",
                                   column_config={
            "File Name": {},
            "is_used": {"selector_type": "boolean"}
        }, 
        width=700, 
        height=300,
        disabled=["File Name"],
        on_change=on_files_changed
        )
        if "original_files" not in st.session_state:
            st.session_state["original_files"] = files.copy()

        return edited_df


def on_files_changed():
    st.session_state["files_changed"] = True
    st.session_state["saved_files_config"] = False
    

def save_state_changes(edited_df):
    edited_df.to_csv(STATE_FILE, index=False)

if st.session_state.get('connected'):
    initialize_settings()

    st.title("📚Files")
    st.write("Here you can upload scripts or other files you want to share with me so I can help you learn.")
    st.write("Once you upload your scripts, I will better understand the course material you ask me about and provide you with better answers 🤖")
    st.write("The uploaded files will be stored on this server and will only be available to you. Of course, you can delete them whenever you want.")

    uploaded_file = st.file_uploader(label="Upload files, presentations, scripts, whatever!", type=None, accept_multiple_files=False, help="By uploading files here, EduBot gains new knowledge and can help you understand the script/material that is not clear to you.")

    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)

    st.header("Uploaded Files")
    edited_df = list_uploaded_files()

    if "files_changed" not in st.session_state:
        st.session_state["files_changed"] = False

    if "saved_files_config" not in st.session_state:
        st.session_state["saved_files_config"] = False

    if st.session_state["files_changed"]:
        if st.button("Save changes", type= 'primary'):
            save_state_changes(edited_df)
            st.session_state["original_files"] = edited_df.copy()
            st.success("Changes saved!")
            st.session_state["saved_files_config"] = True
            st.session_state["disabled"] = False

    if st.session_state["files_changed"] and not st.session_state["saved_files_config"]:
        st.session_state["disabled"] = True

    elif not st.session_state["files_changed"] and not st.session_state["saved_files_config"]:
        st.session_state["disabled"] = False

    if st.button("Make me smarter! 🧠", type='secondary', disabled=st.session_state.get("disabled", True)):
        with st.spinner('Learning from your files...'):
            used_files = edited_df.loc[edited_df["is_used"] == True, "File Name"].tolist()
            used_files = [os.path.join(UPLOAD_DIR, file) for file in used_files] 
            st.session_state["raptor"] = get_raptor(files=used_files, force_rebuild=True)
        st.success("EduBot is now smarter!🔥")
        st.session_state["files_changed"] = False

else:
    st.error("You must be logged in for this!")