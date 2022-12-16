import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
from utils.auxiliar_functions import to_excel, plotly_fig2array
import os
########## libraries for building the pdf reports
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl


#Seleccionamos una institución, datos de la institución vs el tiempo, curvas de movimiento de usuarios, cursos, noticias.
st.set_page_config(page_title="Stats by Institution", page_icon=":bar_chart:", layout="wide")

st.markdown(
    """
    <style>
        div[data-testid="column"]:nth-of-type(1)
        {
            text-align: center;
        } 

        div[data-testid="column"]:nth-of-type(2)
        {
            text-align: center;
        } 
    </style>
    """,unsafe_allow_html=True
)

institutions_df = pd.read_csv("pages/Database/institutions.csv" )
users_df = pd.read_csv("pages/Database/users_by_date.csv" )

logs_by_date_df = pd.read_csv("pages/Database/logs_by_date.csv")
logs_by_date_df["fecha"] = pd.to_datetime(logs_by_date_df["fecha"], infer_datetime_format=True)

users_created_by_date_df = pd.read_csv("pages/Database/users_created_by_date.csv")
users_created_by_date_df["fecha"] = pd.to_datetime(users_created_by_date_df["fecha"], infer_datetime_format=True)

admin_created_by_date_df = pd.read_csv("pages/Database/admin_created_by_date.csv")
admin_created_by_date_df["fecha"] = pd.to_datetime(admin_created_by_date_df["fecha"], infer_datetime_format=True)


# ---- SIDEBAR ----
# authenticator.logout("Logout", "sidebar")
name='bharath'
st.sidebar.title(f"Welcome {name}")

institution = st.sidebar.selectbox(
    "Select an institution:",
    options=institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique(),)


df_institutions_selection = institutions_df.query(
    "name == @institution")

df_users_selection = users_df.query(
    "Cliente == @institution")

# ---- MAINPAGE ----
st.title(":bar_chart: {} statistics".format( institution))
st.markdown("##")

# TOP KPI's
# TOP KPI's
total_users = int(df_users_selection["Usuarios totales"].sum()) 
total_active_users = int(df_users_selection["Usuarios activos"].sum()) 
total_collaborator_users = int(df_institutions_selection["collaborator_users"].sum()) 
total_admin_users = int(df_institutions_selection["admin_users"].sum())



first_col,second_col, third_col, fourth_col = st.columns(4)

with first_col:
    st.metric(label="Total Users", value='{:,}'.format(total_users).replace(',','.'), help='Total number of users')
with second_col:
    st.metric(label="Active Users", value='{:,}'.format(total_active_users).replace(',','.'), help='Total number of users that had any activity during the last year')
with third_col:
    st.metric(label="Collaborators Users", value='{:,}'.format(total_collaborator_users).replace(',','.'), help='Total number of collaborators')
with fourth_col:
    st.metric(label="Admin Users", value='{:,}'.format(total_admin_users).replace(',','.'), help='Total number of admin users')


#Users by year
years = [2018, 2019, 2020, 2021, 2022]
users_by_year = [df_users_selection["Usuarios cargados 2018"].sum(),df_users_selection["Usuarios cargados 2019"].sum(), df_users_selection["Usuarios cargados 2020"].sum(), df_users_selection["Usuarios cargados 2021"].sum(),df_users_selection["Usuarios cargados 2022"].sum()]

fig_users_by_year = px.bar(
    users_by_year,
    x=years ,
    y=users_by_year,
    orientation="v",
    title="<b>Users by Year</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_users_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

#Users loggin
years2 = [2019, 2020, 2021, 2022]
users_by_year = [df_users_selection["Usuarios con ingreso a plataforma 2019"].sum(),df_users_selection["Usuarios con ingreso a plataforma 2020"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2021"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2022"].sum()]

fig_admins_by_year = px.bar(
    users_by_year,
    x=years[1:] ,
    y=users_by_year,
    orientation="v",
    title="<b>Users with logging</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_admins_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_users_by_year, use_container_width=True)
right_column.plotly_chart(fig_admins_by_year, use_container_width=True)


#Filter by date
st.markdown("""---""")

st.title("Stats by date")

min_date = dt.datetime(2017,1,1)
max_date = pd.to_datetime("today")

#logs by date
st.header("Logged users by date")
logs_range_dates = st.date_input("Select the date range for the logged users", (min_date, max_date))
logs_start_date = np.datetime64(logs_range_dates[0])
logs_end_date = pd.to_datetime("today")
if len(logs_range_dates)!=1:
    logs_end_date = np.datetime64(logs_range_dates[1])
logs_selected_institution = logs_by_date_df[logs_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
logs_date_range = (logs_selected_institution["fecha"] >= logs_start_date) & (logs_selected_institution["fecha"] <= logs_end_date)
logged_users_df = logs_selected_institution.loc[logs_date_range]
left_column, right_column = st.columns(2)

with left_column:
    date_users_df = logged_users_df[["fecha", "logged_users"]]
    st.dataframe(date_users_df)

with right_column:
    fig_logged_users = plt.plot(logged_users_df["fecha"], logged_users_df["logged_users"])
    st.line_chart(data = date_users_df, x="fecha", y="logged_users", use_container_width=True)

st.markdown("""---""")

#Created users by date
st.header("Created users by date")
users_created_range_dates = st.date_input("Select the date range for the created users", (min_date, max_date))
users_created_start_date = np.datetime64(users_created_range_dates[0])
users_created_end_date = pd.to_datetime("today")
if len(users_created_range_dates)!=1:
    users_created_end_date = np.datetime64(users_created_range_dates[1])
users_created_selected_institution = users_created_by_date_df[users_created_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
users_created_date_range = (users_created_selected_institution["fecha"] >= users_created_start_date) & (users_created_selected_institution["fecha"] <= users_created_end_date)
users_created_df = users_created_selected_institution.loc[users_created_date_range]
left_column, right_column = st.columns(2)

with left_column:
    date_users_df = users_created_df[["fecha", "created_users"]]
    st.dataframe(date_users_df)

with right_column:
    fig_created_users = plt.plot(users_created_df["fecha"], users_created_df["created_users"])
    st.line_chart(data = date_users_df, x="fecha", y="created_users", use_container_width=True)

st.markdown("""---""")

#Admin users created by date
st.header("Created admin users by date")
admin_created_range_dates = st.date_input("Select the date range for the admin created users", (min_date, max_date))
admin_created_start_date = np.datetime64(admin_created_range_dates[0])
admin_created_end_date = pd.to_datetime("today")
if len(admin_created_range_dates)!=1:
    admin_created_end_date = np.datetime64(admin_created_range_dates[1])
admin_created_selected_institution = admin_created_by_date_df[admin_created_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
admin_created_date_range = (admin_created_selected_institution["fecha"] >= users_created_start_date) & (admin_created_selected_institution["fecha"] <= admin_created_end_date)
admin_created_df = admin_created_selected_institution.loc[admin_created_date_range]
left_column, right_column = st.columns(2)

with left_column:
    date_users_df = admin_created_df[["fecha", "created_admins"]]
    st.dataframe(date_users_df)

with right_column:
    fig_created_users = plt.plot(admin_created_df["fecha"], admin_created_df["created_admins"])
    st.line_chart(data = date_users_df, x="fecha", y="created_admins", use_container_width=True)
    
st.markdown("""---""")

st.header("General stats summary")

#Subjects information

total_contents = int(df_institutions_selection["classes_count"].sum()) + int(df_institutions_selection["text_count"].sum()) + int(df_institutions_selection["scorm_count"].sum())
total_programs_count = int(df_institutions_selection["programs_count"].sum())
total_created_tests_count = int(df_institutions_selection["created_tests_count"].sum())
total_created_news_count = int(df_institutions_selection["created_news_count"].sum())
total_created_questions = int(df_institutions_selection["created_questions"].sum())
total_courses_count = int(df_institutions_selection["courses_count"].sum())
total_finished_courses = int(df_institutions_selection["finished_courses"].sum())
total_answered_questions_count = int(df_institutions_selection["answered_questions_count"].sum())
total_correct_answers_count = int(df_institutions_selection["correct_answers_count"].sum())
total_incorrect_answers_count = int(df_institutions_selection["incorrect_answers_count"].sum())
total_likes_count = int(df_institutions_selection["likes_count"].sum())
total_new_views_count = int(df_institutions_selection["new_views_count"].sum())
total_comments_count = int(df_institutions_selection["comments_count"].sum())
total_attempts_count = int(df_institutions_selection["attempts_count"].sum())


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




metrics_keys = [
    "Total Users",
    "Active Users",
    "Collaborator Users",
    "Admin Users",
    "Created Programs",
    "Created Contents",
    "Created Courses",
    "Finished Courses",
    "Comments Count",
    "Created Tests",
    "Created Questions",
    "Answered Questions",
    "Correct Answers",
    "Incorrect Answers",
    "Attemps Count",
    "Created News",
    "News Views",
    "News Likes Count"
]

metrics_values = [
    total_users,
    total_active_users,
    total_collaborator_users,
    total_admin_users,
    total_programs_count,
    total_contents,
    total_created_tests_count,
    total_created_news_count,
    total_created_questions,
    total_courses_count,
    total_finished_courses,
    total_answered_questions_count,
    total_correct_answers_count,
    total_incorrect_answers_count,
    total_likes_count,
    total_new_views_count,
    total_comments_count,
    total_attempts_count
]

# Dataframe con concentración de métricas
metrics_data = []
for index_metric in range(len(metrics_keys)):
    metrics_data.append([metrics_keys[index_metric], metrics_values[index_metric]])

metrics_df = pd.DataFrame(metrics_data, columns=["Metric", "Value"], index=None)

col1, col2 = st.columns(2)
# Botón de descarga en formato csv
with col1:
    st.download_button(
                    "Download .csv",
                    data=metrics_df.to_csv(index=False),
                    file_name=f"metrics.csv",
                    mime="text/csv",
                    key='download-csv'
                    )

# Botón de descarga en formato excel
with col2:
    st.download_button(
                    "Descargar (formato excel)",
                    data = to_excel(metrics_df),
                    file_name=f"metrics.xlsx",
                    mime="application/vnd.ms-excel",
                    key='download-excel'
                    )


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

template = PdfReader("assets/template_report.pdf", decompress=False).pages[0]
template_obj = pagexobj(template)

canvas = Canvas('report')

xobj_name = makerl(canvas, template_obj)
canvas.doForm(xobj_name)

#canvas.setFont('psfontname', size, leading = None)


ystart = 0

# Title and institution count
canvas.drawCentredString(297, 773, f"{institution}")

# Users stats
canvas.drawString(45, 565, '{:,}'.format(total_users).replace(',','.'))
canvas.drawString(170, 567, '{:,}'.format(total_active_users).replace(',','.'))
canvas.drawString(335, 565, '{:,}'.format(total_collaborator_users).replace(',','.'))
canvas.drawString(490, 567, '{:,}'.format(total_admin_users).replace(',','.'))

# Plots
plot1 = plotly_fig2array(fig_users_by_year)
plot2 = plotly_fig2array(fig_admins_by_year)

plot_w = 120
plot_h = 120
canvas.drawInlineImage(plot1, 45, 400, width=plot_w, height=plot_h)
canvas.drawInlineImage(plot2, 45 + plot_w + 10, 400, width=plot_w, height=plot_h)

# Metrics
non_user_metrics = metrics_values[4:]
non_user_metrics_keys = metrics_keys[4:]

max_metrics_per_row = 4
non_user_metrics_width = 120
non_user_metrics_height = 300
for metric_index in range(1, len(non_user_metrics)):
    metric_name = non_user_metrics_keys[metric_index]
    metric = non_user_metrics[metric_index]
    canvas.drawString(45 + (non_user_metrics_width*(metric_index%max_metrics_per_row)), non_user_metrics_height + 14, metric_name)
    canvas.drawString(45 + (non_user_metrics_width*(metric_index%max_metrics_per_row)), non_user_metrics_height, '{:,}'.format(metric).replace(',','.'))
    if metric_index%max_metrics_per_row == 0:
        non_user_metrics_height -= 35


st.download_button(
                "Download Report (pdf)",
                data=canvas.getpdfdata(),
                file_name=f"report_{institution}.pdf",
                mime="application/pdf",
                )

