import streamlit as st
import os
import streamlit_google_oauth as oauth
from dotenv import load_dotenv
from utils.auxiliar_functions import nav_page, set_code

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# streamlit run app.py --server.port 8080


load_dotenv()
client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]
print(redirect_uri)


if __name__ == "__main__":
    st.set_page_config(page_title="streamlit Dashboard", page_icon=":bar_chart:", layout="wide")

    hide_bar = """
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            visibility:hidden;
            width: 0px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
            visibility:hidden;
        }
        </style>
    """
    login_info = oauth.login(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
        login_button_text="Login with Google", logout_button_text="Logout",
    )
    if login_info:
        user_id, user_email = login_info
        #token = st.session_state.token.access_token
        #set_code(code=token)
        set_code(code="/logged_in")
        nav_page('General_Statistics')
    else:
        st.markdown(hide_bar, unsafe_allow_html=True)
