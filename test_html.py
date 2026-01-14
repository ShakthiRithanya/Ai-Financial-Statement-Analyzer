import streamlit as st

st.set_page_config(page_title="HTML Test", layout="wide")

st.markdown("""
<h1 style="font-size: 5rem; font-weight: 900; color: #8b5cf6;">
    Test Title
</h1>
<p style="font-size: 1.3rem; color: #b0b0c0;">
    This is a test paragraph.
</p>
""", unsafe_allow_html=True)

st.write("If you see styled HTML above, it works!")
