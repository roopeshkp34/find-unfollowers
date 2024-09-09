from collections import defaultdict
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

from instagram import Instagram


st.set_page_config(
    layout="centered",
    initial_sidebar_state="auto",
    page_title="Find Un-followers",
)
col1, col2 = st.columns([6, 1])
# with col1:
#     # st.image("./media/MAIA.svg", width=94)
#     ...
with col1:
    st.markdown(
        "<h1 style='display: flex; align-items: center; height: 50px; margin-left: -5px; margin-top: -15px; font-size: x-large;'>Find Un followers</h1>",
        unsafe_allow_html=True,
    )

st.markdown(
    "<p>Our app makes it easy to find people on Instagram who are not following you back. By using Instagram's data download feature, you can get a list of your activity, including the accounts you follow. Simply upload the downloaded data in either HTML or JSON format into our app, and it will analyze the information to show you who isn't following you back. This ensures that your data remains secure, as everything is processed locally without requiring your Instagram password. Stay in control of your social circle with just a few simple steps!.</p>",
    unsafe_allow_html=True,
)

st.markdown(
    """
    ### How to Request Followers/Unfollowers List from Instagram via Meta:
    1. Access Instagram Settings:
        * Open the Instagram app on your mobile device or log in via a web browser.
        * Navigate to your profile by tapping your profile picture in the bottom right corner.
        * Tap on the three horizontal lines (menu) in the top right corner to open the settings menu.
    2. Go to Account Settings:
        * In the settings menu, tap on "Settings and Privacy".
        * Scroll down and select “Your Activity and Account”.
    3. Request Your Data:
        * In the "Your Activity and Account" section, look for "Download your Information".
        * Tap on it to start the data download request process.
    4. Choose Data Format:
        * Instagram will ask you to choose a format for your data. You can choose between HTML (easier to view in a browser) or JSON (for developers or importing into another system). If you are specifically looking for a followers/unfollowers list, HTML format might be easier to browse.
    5. Submit Your Request:
        * After selecting the format, tap "Request Download."
        * Instagram will prompt you to enter your account password to verify your identity.
        * Once you enter your password, the request will be submitted.
    6. Wait for the Download Link:
        * Instagram will compile your data, which might take up to 48 hours. You will receive an email with a link to download your data when it's ready.
        * The email will be sent to the email address associated with your Instagram account.
    7. Download and Access Your Data:
        * Once you receive the email, click on the provided link to download your data.
        * The downloaded file will be in a compressed (.zip) format. Unzip the file to view its contents.
    8. Locate Followers/Unfollowers Information:
        * Inside the unzipped folder, you will find multiple files related to your Instagram activity.
        * Look for files related to "followers_and_following" or similar naming conventions. These files will contain a list of your current followers and accounts you follow.
    """
)

followers_file = st.file_uploader(f"Upload Followers file", type=["html", "json"])

if followers_file:
    following_file = st.file_uploader(f"Upload Following file", type=["html", "json"])
    if following_file:
        users_df = Instagram().master(followers_file=followers_file, following_file=following_file)
        st.write(users_df.to_html(escape=False), unsafe_allow_html=True)
