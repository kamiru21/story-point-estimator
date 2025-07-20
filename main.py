import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Story Point Estimator")

st.title("📏 AI Story Point Estimator")
st.write("Enter a user story to get an estimated effort in story points.")

# Input form
with st.form("story_form"):
    title = st.text_input("User Story Title", placeholder="e.g. Reset password link")
    description = st.text_area("Description (optional)", placeholder="What should it do?")
    submitted = st.form_submit_button("Estimate Story Points")

# Setup OpenAI key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def estimate_points(title, desc):
    full_input = f"User story title: {title}\nDescription: {desc}\n\nEstimate story points (1, 2, 3, 5, 8, or 13):"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_input}],
        temperature=0.5,
        max_tokens=20
    )
    
    return response.choices[0].message.content.strip()

# Handle form
if submitted and title:
    with st.spinner("Thinking..."):
        points = estimate_points(title, description)
        st.success(f"Estimated Story Points: **{points}**")
