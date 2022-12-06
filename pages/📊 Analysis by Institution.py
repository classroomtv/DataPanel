import pickle
from pathlib import Path

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit



#Seleccionamos una institución, datos de la institución vs el tiempo, curvas de movimiento de usuarios, cursos, noticias.
st.set_page_config(page_title="Stats by Institution", page_icon=":bar_chart:", layout="wide")


def get_data_from_excel():
    df = pd.read_csv("pages/Database/institutions.csv" )
    # Add 'hour' column to dataframe
    return df

df = get_data_from_excel()
users_df = pd.read_csv("pages/Database/users_by_date.csv" )


# ---- SIDEBAR ----
# authenticator.logout("Logout", "sidebar")
name='bharath'
st.sidebar.title(f"Welcome {name}")

institution = st.sidebar.selectbox(
    "Select a institution:",
    options=df[df["collaborator_users"]>=3]["name"].unique(),)


df_selection = df.query(
    "name == @institution")

df_users_selection = users_df.query(
    "Cliente == @institution")

# ---- MAINPAGE ----
st.title(":bar_chart: Stats by Institution")
st.markdown("##")

# TOP KPI's
# TOP KPI's
total_users = int(df_users_selection["Usuarios totales"].sum()) 
total_active_users = int(df_users_selection["Usuarios activos"].sum()) 
total_collaborator_users = int(df_selection["collaborator_users"].sum()) 
total_admin_users = int(df_selection["admin_users"].sum())



first_col,second_col, third_col, fourth_col = st.columns(4)

with first_col:
    st.metric(label="Total Users", value='{:,}'.format(total_users).replace(',','.'), help='Total number of users')
with second_col:
    st.metric(label="Active Users", value='{:,}'.format(total_active_users).replace(',','.'), help='Total number of users that had any activity during the year')
with third_col:
    st.metric(label="Collaborators Users", value='{:,}'.format(total_collaborator_users).replace(',','.'), help='Total number of collaborators')
with fourth_col:
    st.metric(label="Admin Users", value='{:,}'.format(total_admin_users).replace(',','.'), help='Total number of admin users')


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


# Defining the grid to display the metrics
rows = 3
cols = 5

column_list = []
for row in range(rows):
    column_list.extend(st.columns(cols))


# Adding the metrics to the grid
with column_list[0]:
    st.metric(label="Created Programs", value='{:,}'.format(total_programs_count).replace(',','.'), help='Total number of programs created')
with column_list[1]:
    st.metric(label="Created Contents", value='{:,}'.format(total_contents).replace(',','.'), help='Total number of content items created')
with column_list[2]:
    st.metric(label="Created Courses", value='{:,}'.format(total_courses_count).replace(',','.'), help='Total number of content items created')
with column_list[3]:
    st.metric(label="Finished Courses", value='{:,}'.format(total_finished_courses).replace(',','.'), help='Total number of content items created')
with column_list[4]:
    st.metric(label="Comments Count", value='{:,}'.format(total_comments_count).replace(',','.'), help='Total number of content items created')
with column_list[5]:
    st.metric(label="Created Tests", value='{:,}'.format(total_created_tests_count).replace(',','.'), help='Total number of content items created')
with column_list[6]:
    st.metric(label="Created Questions", value='{:,}'.format(total_created_questions).replace(',','.'), help='Total number of content items created')
with column_list[7]:
    st.metric(label="Answered Questions", value='{:,}'.format(total_answered_questions_count).replace(',','.'), help='Total number of content items created')
with column_list[8]:
    st.metric(label="Correct Answers", value='{:,}'.format(total_correct_answers_count).replace(',','.'), help='Total number of content items created')
with column_list[9]:
    st.metric(label="Incorrect Answers", value='{:,}'.format(total_incorrect_answers_count).replace(',','.'), help='Total number of content items created')
with column_list[10]:
    st.metric(label="Attempts Count", value='{:,}'.format(total_attempts_count).replace(',','.'), help='Total number of content items created')
with column_list[11]:
    st.metric(label="Created News", value='{:,}'.format(total_created_news_count).replace(',','.'), help='Total number of content items created')
with column_list[12]:
    st.metric(label="News Views", value='{:,}'.format(total_new_views_count).replace(',','.'), help='Total number of content items created')
with column_list[13]:
    st.metric(label="News Likes Count", value='{:,}'.format(total_likes_count).replace(',','.'), help='Total number of content items created')



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)