import streamlit as st
import pandas as pd
import datetime
import os

# 1. Load the course database
@st.cache_data
def load_data():
    # We force the 'Region' column to be read as a string (str) immediately
    df = pd.read_csv("dg_database.csv", dtype={'Region': str})
    # Remove any rows where the Region or Course might be missing
    df = df.dropna(subset=['Region', 'Course'])
    # Remove hidden spaces
    df['Region'] = df['Region'].str.strip()
    return df

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
            
            # CLEANED SORTING: Converts unique values to a list and ensures they are strings
            regions = sorted([str(r) for r in df_courses["Region"].unique()])
            region_select = st.selectbox("Select Region", regions)
            
            # Filter courses based on selection
            filtered_courses = df_courses[df_courses["Region"] == region_select]["Course"].tolist()
            course_name = st.selectbox("Select Course", sorted(filtered_courses))

        with col2:
            date = st.date_input("Date", datetime.date.today())
            
            # Get data for the selected course to set default score
            course_row = df_courses[df_courses["Course"] == course_name].iloc[0]
            score = st.number_input("Score", min_value=18, max_value=150, value=int(course_row["SSA"]))
            
        submit = st.form_submit_button("Save Round")
        
        if submit and name:
            ssa = course_row["SSA"]
            pps = course_row["PPS"]
            rating = 1000 - ((score - ssa) * pps)
            
            new_round = pd.DataFrame([[date, name, course_name, score, int(rating)]], 
                                     columns=["Date", "Name", "Course", "Score", "Rating"])
            new_round.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Round saved! {name} earned a {int(rating)} rating.")

# --- SECTION 2: RATING HISTORY CHART ---
st.subheader("📈 Performance History")
if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE)

    if not history_df.empty:
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        friends = st.multiselect("Select Friends to Compare:", history_df["Name"].unique(), default=history_df["Name"].unique())
        filtered_history = history_df[history_df["Name"].isin(friends)]

        if not filtered_history.empty:
            st.line_chart(filtered_history, x="Date", y="Rating", color="Name")
            with st.expander("View Raw Scorecard"):
                st.dataframe(filtered_history.sort_values(by="Date", ascending=False), use_container_width=True)
    else:
        st.info("No rounds logged yet. Add a score above!")
            course_name = st.selectbox("Select Course", filtered_courses)

        with col2:
            date = st.date_input("Date", datetime.date.today())
            
            # Automatically set default score based on SSA of selected course
            course_data = df_courses[df_courses["Course"] == course_name].iloc[0]
            score = st.number_input("Score", min_value=18, max_value=150, value=int(course_data["SSA"]))
            
        submit = st.form_submit_button("Save Round")
        
        if submit and name:
            ssa = course_data["SSA"]
            pps = course_data["PPS"]
            rating = 1000 - ((score - ssa) * pps)
            
            new_round = pd.DataFrame([[date, name, course_name, score, int(rating)]], 
                                     columns=["Date", "Name", "Course", "Score", "Rating"])
            new_round.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Round saved! {name} earned a {int(rating)} rating.")

# --- SECTION 2: RATING HISTORY CHART ---
st.subheader("📈 Performance History")
history_df = pd.read_csv(HISTORY_FILE)

if not history_df.empty:
    history_df['Date'] = pd.to_datetime(history_df['Date'])
    friends = st.multiselect("Select Friends to Compare:", history_df["Name"].unique(), default=history_df["Name"].unique())
    filtered_history = history_df[history_df["Name"].isin(friends)]

    if not filtered_history.empty:
        st.line_chart(filtered_history, x="Date", y="Rating", color="Name")
        with st.expander("View Raw Scorecard"):
            st.dataframe(filtered_history.sort_values(by="Date", ascending=False), use_container_width=True)
else:
    st.info("No rounds logged yet. Add a score above!")
