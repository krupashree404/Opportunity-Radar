import streamlit as st
import pandas as pd
from pathlib import Path

# PAGE SETTINGS
st.set_page_config(
    page_title="Opportunity Radar",
    page_icon="🧭",
    layout="wide"
)

# LOAD DATA

DATA_FILE = Path(__file__).parent / "opportunities.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

# HEADER
st.title("🧭 Opportunity Radar")
st.subheader("Discover Opportunities. Explore Your Future.")
st.write(
    "Find internships, scholarships, hackathons, "
    "courses and competitions in one place."
)

st.info(
    "MVP demonstration using sample opportunity data. "
    "Verify details through official sources."
)

# SIDEBAR
st.sidebar.title("🔍 Find Opportunities")

name = st.sidebar.text_input("Enter your name")

interests = st.sidebar.multiselect(
    "Select your interests",
    [
        "Technology",
        "AI/ML",
        "Python",
        "Web Development",
        "Business",
        "Design",
        "Cybersecurity",
        "Data Science",
        "Research"
    ]
)

categories = st.sidebar.multiselect(
    "Select opportunity category",
    sorted(df["type"].unique()),
    default=sorted(df["type"].unique())
)

search = st.sidebar.text_input("Search opportunities")

# FILTER DATA
result = df[df["type"].isin(categories)].copy()

if search:
    mask = (
        result["title"].str.contains(
            search, case=False, na=False
        )
        |
        result["description"].str.contains(
            search, case=False, na=False
        )
        |
        result["skills"].str.contains(
            search, case=False, na=False
        )
    )
    result = result[mask].copy()

# RECOMMENDATION LOGIC
def calculate_score(row):
    score = 0

    text = (
        str(row["title"]) + " " +
        str(row["description"]) + " " +
        str(row["skills"])
    ).lower()

    for interest in interests:
        if interest.lower() in text:
            score += 1

    return score

result["score"] = result.apply(
    calculate_score, axis=1
)

result = result.sort_values(
    by="score", ascending=False
)

# DASHBOARD
st.markdown("---")
st.header("📊 Opportunity Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("Total Opportunities", len(df))
c2.metric("Matching Results", len(result))
c3.metric("Selected Interests", len(interests))

# PERSONAL GREETING
if name:
    st.success(f"Welcome {name}! Explore your opportunities.")

# RECOMMENDATIONS
st.markdown("---")
st.header("⭐ Recommended Opportunities")

if result.empty:
    st.warning("No opportunities found. Change your filters.")

else:
    for _, row in result.iterrows():

        with st.container(border=True):

            st.subheader(row["title"])

            st.write(row["description"])

            a, b = st.columns(2)

            with a:
                st.write("*Category:*", row["type"])
                st.write("*Skills:*", row["skills"])

            with b:
                st.write("*Eligibility:*", row["eligibility"])
                st.write("*Deadline:*", row["deadline"])

            st.write(
                "Interest match:",
                f"{row['score']} matching keywords"
            )

            if st.button(
                "⭐ Save Opportunity",
                key=f"save_{row['id']}"
            ):

                saved = st.session_state.get(
                    "saved", []
                )

                if row["id"] not in saved:
                    saved.append(row["id"])

                st.session_state["saved"] = saved

                st.success("Opportunity saved!")

# SAVED OPPORTUNITIES
st.markdown("---")
st.header("❤️ My Saved Opportunities")

saved_ids = st.session_state.get("saved", [])

saved_data = df[df["id"].isin(saved_ids)]

if saved_data.empty:
    st.write("No saved opportunities yet.")

else:
    for _, row in saved_data.iterrows():
        st.write(
            f"⭐ {row['title']} - {row['type']}"
        )

# PROJECT INFORMATION
st.markdown("---")
st.header("💡 How Opportunity Radar Works")

st.write("""
1. Users select their interests.
2. The system filters opportunities.
3. A keyword matching algorithm calculates relevance.
4. Matching opportunities are ranked.
5. Users can save interesting opportunities.
""")

st.success(
    "Opportunity Radar MVP is running successfully!"
)

st.caption(
    "Future scope: Live APIs, AI-based matching, "
    "user accounts and database integration."
)