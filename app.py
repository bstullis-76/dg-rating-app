import streamlit as st
import pandas as pd
import datetime
import os

# 1. Load the course database
@st.cache_data
def load_data():
    return pd.read_csv("dg_database.csv")

df_courses = load_data()

# 2. Setup History File
HISTORY_FILE = "rounds_history.csv"
if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["Date", "Name", "Course", "Score", "Rating"]).to_csv(HISTORY_FILE, index=False)

st.set_page_config(page_title="DG Rating Tracker", page_icon="🥏")
st.title("🥏 Friend Group Rating Tracker")

# --- SECTION 1: LOG A NEW ROUND ---
with st.expander("➕ Log a New Round"):
    with st.form("score_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Friend's Name")
            region = st.selectbox("Region", sorted(df_courses["Region"].unique()))
            course_list = df_courses[df_courses["Region"] == region]["Course"]
            course_name = st.selectbox("Course", course_list)
        with col2:
            date = st.date_input("Date", datetime.date.today())
            score = st.number_input("Score", min_value=18, max_value=150, value=54)
            
        submit = st.form_submit_button("Save Round")
        
        if submit and name:
            # Calculate Rating
            c_data = df_courses[df_courses["Course"] == course_name].iloc[0]
            rating = 1000 - ((score - c_data["SSA"]) * c_data["PPS"])
            
            # Save to CSV
            new_round = pd.DataFrame([[date, name, course_name, score, int(rating)]], 
                                     columns=["Date", "Name", "Course", "Score", "Rating"])
            new_round.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Round saved! {name} earned a {int(rating)} rating.")

# --- SECTION 2: RATING HISTORY CHART ---
st.subheader("📈 Performance History")
history_df = pd.read_csv(HISTORY_FILE)

if not history_df.empty:
    history_df['Date'] = pd.to_datetime(history_df['Date'])
    
    # Filter by specific friends
    friends = st.multiselect("Select Friends to Compare:", history_df["Name"].unique(), default=history_df["Name"].unique())
    filtered_history = history_df[history_df["Name"].isin(friends)]

    # Plotting the Chart
    st.line_chart(filtered_history, x="Date", y="Rating", color="Name")
    
    # Raw Data Table
    with st.expander("View Raw Scorecard"):
        st.dataframe(filtered_history.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No rounds logged yet. Use the form above to add your first score!")

st.divider()
st.caption("All data is saved locally to 'rounds_history.csv'.")
