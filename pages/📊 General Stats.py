import pickle
from pathlib import Path
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit



# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="General Stats", page_icon=":bar_chart:", layout="wide")

df = pd.read_csv("pages/Database/institutions.csv" )
users_df = pd.read_csv("pages/Database/users_by_date.csv" )

# ---- SIDEBAR ----
# authenticator.logout("Logout", "sidebar")
name='bharath'
st.sidebar.title(f"Welcome {name}")
st.sidebar.header("Please Filter Here:")


institution = st.sidebar.multiselect(
    "Select the institutions:",
    options=df[df["collaborator_users"]>=3]["name"].unique(),
    default=df[df["collaborator_users"]>=3]["name"].unique(),
)


df_selection = df.query(
    "name == @institution")
df_users_selection = users_df.query(
    "Cliente == @institution")

# ---- MAINPAGE ----
total_institutions = int(df_selection.shape[0])

st.title(":bar_chart: General Institutions Stats")
st.subheader(f"Total Institutions: {total_institutions:,}")
st.markdown("""---""")
st.markdown("##")

# TOP KPI's
total_users = int(df_users_selection["Usuarios totales"].sum()) 
total_active_users = int(df_users_selection["Usuarios activos"].sum()) 
total_collaborator_users = int(df_selection["collaborator_users"].sum()) 
total_admin_users = int(df_selection["admin_users"].sum())


first_col,second_col, third_col, fourth_col = st.columns(4)

with first_col:
    st.subheader(f"Total Users: {total_users:,}")
with second_col:
    st.subheader(f"Active Users: {total_active_users:,}")
with third_col:
    st.subheader(f"Collaborators Users: {total_collaborator_users:,}")
with fourth_col:
    st.subheader(f"Admin Users: {total_admin_users:,}")

#Users by year
years = [2018, 2019, 2020, 2021, 2022]
users_by_year = [df_users_selection["Usuarios cargados 2018"].sum(),df_users_selection["Usuarios cargados 2019"].sum(), df_users_selection["Usuarios cargados 2020"].sum(), df_users_selection["Usuarios cargados 2021"].sum(),df_users_selection["Usuarios cargados 2022"].sum()]

fig_users_by_city = px.bar(
    users_by_year,
    x=years ,
    y=users_by_year,
    orientation="v",
    title="<b>Users by Year</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_users_by_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

#Users loggin
years2 = [2019, 2020, 2021, 2022]
users_by_year = [df_users_selection["Usuarios con ingreso a plataforma 2019"].sum(),df_users_selection["Usuarios con ingreso a plataforma 2020"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2021"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2022"].sum()]

fig_admin_by_city = px.bar(
    users_by_year,
    x=years[1:] ,
    y=users_by_year,
    orientation="v",
    title="<b>Users with logging</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_admin_by_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_users_by_city, use_container_width=True)
right_column.plotly_chart(fig_admin_by_city, use_container_width=True)
#Collaborators Users by institution
users_by_city = (
    df_selection.groupby(by=["name"]).sum()[["collaborator_users"]].sort_values(by="collaborator_users").tail(15)
)
fig_users_by_city = px.bar(
    users_by_city,
    x="collaborator_users",
    y=users_by_city.index,
    orientation="h",
    title="<b>Collaborators Users by Institution</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_city),
    template="plotly_white",
)
fig_users_by_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

#Admin by institution
admin_by_city = (
    df_selection.groupby(by=["name"]).sum()[["admin_users"]].sort_values(by="admin_users").tail(15)
)
fig_admin_by_city = px.bar(
    admin_by_city,
    x="admin_users",
    y=admin_by_city.index,
    orientation="h",
    title="<b>Admin users by Institution</b>",
    color_discrete_sequence=["#0083B8"] * len(admin_by_city),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_admin_by_city.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_users_by_city, use_container_width=True)
right_column.plotly_chart(fig_admin_by_city, use_container_width=True)



#Información de cursos
st.markdown("""---""")


first_col,second_col, third_col, fourth_col, fifth_col = st.columns(5)
sixth_col, seventh_col, eighth_col, ninth_col, tenth_col = st.columns(5)
eleventh_col, twelth_col, thirteenth_col, fourteenth_col, fifteenth_col = st.columns(5)

total_contents = int(df_selection["classes_count"].sum()) + int(df_selection["text_count"].sum()) + int(df_selection["scorm_count"].sum())
total_programs_count = int(df_selection["programs_count"].sum())
total_created_tests_count = int(df_selection["created_tests_count"].sum())
total_created_news_count = int(df_selection["created_news_count"].sum())
total_created_questions = int(df_selection["created_questions"].sum())
total_courses_count = int(df_selection["courses_count"].sum())
total_finished_courses = int(df_selection["finished_courses"].sum())
total_answered_questions_count = int(df_selection["answered_questions_count"].sum())
total_correct_answers_count = int(df_selection["correct_answers_count"].sum())
total_incorrect_answers_count = int(df_selection["incorrect_answers_count"].sum())
total_likes_count = int(df_selection["likes_count"].sum())
total_new_views_count = int(df_selection["new_views_count"].sum())
total_comments_count = int(df_selection["comments_count"].sum())
total_attempts_count = int(df_selection["attempts_count"].sum())


with first_col:
    st.subheader(f"Created Programs: {total_programs_count:,}")
with second_col:
    st.subheader(f"Created Contents: {total_contents:,}")
with third_col:
    st.subheader(f"Created Courses: {total_courses_count:,}")
with fourth_col:
    st.subheader(f"Finished Courses: {total_finished_courses:,}")
with fifth_col:
    st.subheader(f"Comments Count: {total_comments_count:,}")
with sixth_col:
    st.subheader(f"Created Tests: {total_created_tests_count:,}")
with seventh_col:
    st.subheader(f"Created Questions: {total_created_questions:,}")
with eighth_col:
    st.subheader(f"Answered Questions: {total_answered_questions_count:,}")
with ninth_col:
    st.subheader(f"Correct Answers: {total_correct_answers_count:,}")
with tenth_col:
    st.subheader(f"Incorrect Answers: {total_incorrect_answers_count:,}")
with eleventh_col:
    st.subheader(f"Attempts Count: {total_attempts_count:,}")
with twelth_col:
    st.subheader(f"Created News: {total_created_news_count:,}")
with thirteenth_col:
    st.subheader(f"News Views: {total_new_views_count:,}")
with fourteenth_col:
    st.subheader(f"News Likes Count: {total_likes_count:,}")





# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)