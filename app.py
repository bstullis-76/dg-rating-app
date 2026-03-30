import streamlit as st
import pandas as pd
import datetime
import os

# 1. Load the course database
@st.cache_data
def load_data():
    df = pd.read_csv("dg_database.csv", dtype={'Region': str})
    df = df.dropna(subset=['Region', 'Course'])
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
            name_in = st.text_input("Friend's Name")
            reg_list = sorted([str(r) for r in df_courses["Region"].unique()])
            sel_reg = st.selectbox("Select Region", reg_list)
            c_list = df_courses[df_courses["Region"] == sel_reg]["Course"].tolist()
            sel_c = st.selectbox("Select Course", sorted(c_list))
        with col2:
            log_d = st.date_input("Date", datetime.date.today())
            # Logic to get course data
            c_info = df_courses[df_courses["Course"] == sel_c].iloc[0]
            val_ssa = int(c_info["SSA"])
            score_in = st.number_input("Score", min_value=18, max_value=150, value=val_ssa)
            
        submitted = st.form_submit_button("Save Round")
        
        if submitted and name_in:
            calc_r = 1000 - ((score_in - c_info["SSA"]) * c_info["PPS"])
            new_r = pd.DataFrame([[log_d, name_in, sel_c, score_in, int(calc_r)]], 
                                 columns=["Date", "Name", "Course", "Score", "Rating"])
            new_r.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Saved! {name_in} got a {int(calc_r)}.")

# --- SECTION 2: RATING HISTORY ---
st.subheader("📈 Performance History")
hist_df = pd.read_csv(HISTORY_FILE)

if hist_df.empty:
    st.info("No rounds logged yet.")
    st.stop()

hist_df['Date'] = pd.to_datetime(hist_df['Date'])
u_names = hist_df["Name"].unique()
friends = st.multiselect("Select Friends:", u_names, default=u_names)
filt_h = hist_df[hist_df["Name"].isin(friends)]

if not filt_h.empty:
    st.line_chart(filt_h, x="Date", y="Rating", color="Name")
    with st.expander("View Raw Scorecard"):
        st.dataframe(filt_h.sort_values(by="Date", ascending=False), use_container_width=True)
        
        if submitted and name_input:
            calc_rating = 1000 - ((in_score - c_info["SSA"]) * c_info["PPS"])
            new_entry = pd.DataFrame([[log_date, name_input, sel_course, in_score, int(calc_rating)]], 
                                     columns=["Date", "Name", "Course", "Score", "Rating"])
            new_entry.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Saved! {name_input} got a {int(calc_rating)}.")

# --- SECTION 2: RATING HISTORY ---
st.subheader("📈 Performance History")
hist_df = pd.read_csv(HISTORY_FILE)

# If no data, show info and stop the script here
if hist_df.empty:
    st.info("No rounds logged yet.")
    st.stop()

# If we get here, data exists
hist_df['Date'] = pd.to_datetime(hist_df['Date'])
unique_names = hist_df["Name"].unique()
sel_friends = st.multiselect("Select Friends:", unique_names, default=unique_names)

plot_df = hist_df[hist_df["Name"].isin(sel_friends)]

if not plot_df.empty:
    st.line_chart(plot_df, x="Date", y="Rating", color="Name")
    with st.expander("View Raw Scorecard"):
        st.dataframe(plot_df.sort_values(by="Date", ascending=False), use_container_width=True)
            score = st.number_input("Score", min_value=18, max_value=150, value=int(c_row["SSA"]))
            
        if st.form_submit_button("Save Round") and name:
            ssa, pps = c_row["SSA"], c_row["PPS"]
            rating = 1000 - ((score - ssa) * pps)
            new_r = pd.DataFrame([[date, name, course_sel, score, int(rating)]], 
                                 columns=["Date", "Name", "Course", "Score", "Rating"])
            new_r.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
            st.success(f"Saved! {name} got a {int(rating)}.")

# --- SECTION 2: RATING HISTORY ---
st.subheader("📈 Performance History")
hist_df = pd.read_csv(HISTORY_FILE)

if hist_df.empty:
    st.info("No rounds logged yet.")
else:
    hist_df['Date'] = pd.to_datetime(hist_df['Date'])
    u_names = hist_df["Name"].unique()
    friends = st.multiselect("Select Friends:", u_names, default=u_names)
    filt_h = hist_df[hist_df["Name"].isin(friends)]
    
    if not filt_h.empty:
        st.line_chart(filt_h, x="Date", y="Rating", color="Name")
        with st.expander("View Raw Scorecard"):
            st.dataframe(filt_h.sort_values(by="Date", ascending=False), use_container_width=True)
            # Get data for selected course
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

# --- SECTION 2: RATING HISTORY ---
st.subheader("📈 Performance History")
if os.path.exists(HISTORY_FILE):
    history_df = pd.read_csv(HISTORY_FILE)
    if not history_df.empty:
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        friends = st.multiselect("Select Friends:", history_df["Name"].unique(), default=history_df["Name"].unique())
        filtered_history = history_df[history_df["Name"].isin(friends)]
        if not filtered_history.empty:
            st.line_chart(filtered_history, x="Date", y="Rating", color="Name")
            with st.expander("View Raw Scorecard"):
                st.dataframe(filtered_history.sort_values(by="Date", ascending=False), use_container_width=True)
    else:
        st.info("No rounds logged yet.")

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
