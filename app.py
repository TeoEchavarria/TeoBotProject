import streamlit as st

st.set_page_config(
    page_title="TeoBot",
    page_icon="👋",
)


from visual.teobot_page import TeoBotPage

TeoBotPage()