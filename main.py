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
    full_input = f"User story title: {title}\nDescription: {desc}\n\nEstimate story points (1, 2, 3, 5, 8, or 13) and explain briefly why. Format your answer like 'Points: X — Explanation...'"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_input}],
        temperature=0.5,
        max_tokens=20
    )
    
    output = response.choices[0].message.content.strip()
    point, explanation = output.split("—", 1)
    return point.strip(), explanation.strip()


# Handle form
if submitted and title:
    with st.spinner("Thinking..."):
        points, reason = estimate_points(title, description)
        st.success(f"Estimated Story Points: **{points}**")
        st.info(reason)

st.subheader("📥 Bulk Estimation from CSV")
csv_file = st.file_uploader("Upload CSV with 'title' and 'description' columns", type="csv")

if csv_file:
    import pandas as pd
    df = pd.read_csv(csv_file)
    results = []

    with st.spinner("Estimating..."):
        for i, row in df.iterrows():
            title = row.get("title", "")
            desc = row.get("description", "")
            points, reason = estimate_points(title, desc)
            results.append({"title": title, "points": points, "explanation": reason})

    result_df = pd.DataFrame(results)
    st.dataframe(result_df)

    csv_download = result_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download results as CSV", csv_download, "estimates.csv", "text/csv")
    import matplotlib.pyplot as plt

    counts = result_df["points"].value_counts().sort_index()
    fig, ax = plt.subplots()
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Story Point Distribution")
    ax.set_xlabel("Points")
    ax.set_ylabel("Count")
    st.pyplot(fig)

