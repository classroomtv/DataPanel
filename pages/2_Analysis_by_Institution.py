import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import gettext
import streamlit_nested_layout
from utils.auxiliar_functions import to_excel, plotly_fig2array, nav_page, get_year_range
from streamlit_google_oauth import logout_button
########## libraries for building the pdf reports
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

_ = gettext.gettext

st.set_page_config(page_title=_("Stats by Institution"), page_icon=":bar_chart:", layout="wide")

language = st.sidebar.selectbox('', ['en', 'es'])
try:
    localizator = gettext.translation('Analysis_by_Institution', localedir='pages/locales', languages=[language])
    localizator.install()
    _ = localizator.gettext 
except:
    pass


# Load page only if logged in
code = st.experimental_get_query_params()['code'][0]
if code == '/logged_in':
    #hide_page('main')
    with st.sidebar:
        
        logout_button(_('Logout'))
else:
    nav_page('')

#Seleccionamos una institución, datos de la institución vs el tiempo, curvas de movimiento de usuarios, cursos, noticias.
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

courses_info_df = pd.read_csv("pages/Database/courses_info.csv", on_bad_lines='skip')
courses_info_df["create_time"] = pd.to_datetime(courses_info_df["create_time"], infer_datetime_format=True)
courses_info_df["view_count"] = courses_info_df["view_count"].astype('Int64')
courses_info_df["signed_users"] = courses_info_df["signed_users"].astype('Int64')
courses_info_df["user_finished_courses"] = courses_info_df["user_finished_courses"].astype('Int64')
courses_info_df["user_failed_courses"] = courses_info_df["user_failed_courses"].astype('Int64')

classes_info_df = pd.read_csv("pages/Database/classes_info.csv", on_bad_lines='skip')
classes_info_df["create_time"] = pd.to_datetime(classes_info_df["create_time"], infer_datetime_format=True)

scorms_info_df = pd.read_csv("pages/Database/scorms_info.csv", on_bad_lines='skip')
scorms_info_df["create_time"] = pd.to_datetime(scorms_info_df["create_time"], infer_datetime_format=True)

tests_info_df = pd.read_csv("pages/Database/tests_info.csv", on_bad_lines='skip')
tests_info_df.convert_dtypes()
tests_info_df["create_time"] = pd.to_datetime(tests_info_df["create_time"], infer_datetime_format=True)

texts_info_df = pd.read_csv("pages/Database/texts_info.csv", on_bad_lines='skip')
texts_info_df["create_time"] = pd.to_datetime(texts_info_df["create_time"], infer_datetime_format=True)

satisfaction_surveys_df = pd.read_csv("pages/Database/satisfaction_surveys.csv", on_bad_lines='skip')
satisfaction_surveys_df["item_create_time"] = pd.to_datetime(satisfaction_surveys_df["item_create_time"], infer_datetime_format=True)

# ---- SIDEBAR ----
name = 'bharath'
st.sidebar.title("{} {}".format(_("Welcome"), name))

available_institutions = institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique()
forus_id = np.where(available_institutions == "Forus")[0][0]
institution = st.sidebar.selectbox(
    _("Select an institution")+":",
    options=institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique(), index=int(forus_id))

df_institutions_selection = institutions_df.query(
    "name == @institution")

df_users_selection = users_df.query(
    "Cliente == @institution")

df_course_selection = courses_info_df.query(
    "name == @institution")

# Users metrics
total_users = int(df_users_selection["Usuarios totales"].sum()) 
total_active_users = int(df_users_selection["Usuarios activos"].sum()) 
total_collaborator_users = int(df_institutions_selection["collaborator_users"].sum()) 
total_admin_users = int(df_institutions_selection["admin_users"].sum())

# News metrics
total_created_news_count = int(df_institutions_selection["created_news_count"].sum())
total_news_likes_count = int(df_institutions_selection["likes_count"].sum())
total_news_views_count = int(df_institutions_selection["new_views_count"].sum())
total_news_comments_count = int(df_institutions_selection["comments_count"].sum())


# ---- MAINPAGE ----
st.title(":bar_chart: {} **{}** ".format(_("Metrics for"),institution))
st.markdown("##")


# Plot 1: Amount of users by year
#year_list = get_year_range(2018)
year_list = [2018, 2019, 2020, 2021, 2022]
users_by_year = [df_users_selection["Usuarios cargados 2018"].sum(),df_users_selection["Usuarios cargados 2019"].sum(), df_users_selection["Usuarios cargados 2020"].sum(), df_users_selection["Usuarios cargados 2021"].sum(),df_users_selection["Usuarios cargados 2022"].sum()]

fig_users_by_year = px.bar(
    users_by_year,
    x=year_list ,
    y=users_by_year,
    orientation="v",
    title="<b>{}</b>".format(_("Users Created by Year")),
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_users_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

# Plot 2: Amount of logged users by year
users_by_year = [df_users_selection["Usuarios con ingreso a plataforma 2019"].sum(),df_users_selection["Usuarios con ingreso a plataforma 2020"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2021"].sum(), df_users_selection["Usuarios con ingreso a plataforma 2022"].sum()]

fig_admins_by_year = px.bar(
    users_by_year,
    x=year_list[1:] ,
    y=users_by_year,
    orientation="v",
    title="<b>{}</b>".format(_("Logged Users by Year")),
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={"x": _("Year"), "y":_('Users')}
)
fig_admins_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

st.title("Users")

with st.expander("**"+ _("Metrics")+"**", expanded=True):
    # Defining the grid to display the users metrics
    users_metric_grid = []
    for row in range(1):
        users_metric_grid.extend(st.columns(4))

    with users_metric_grid[0]:
        st.metric(label=_("Total Users"), value='{:,}'.format(total_users).replace(',','.'), help=_("Total number of users"))
    with users_metric_grid[1]:
        st.metric(label=_("Active Users"), value='{:,}'.format(total_active_users).replace(',','.'), help=_("Total number of active users"))
    with users_metric_grid[2]:
        st.metric(label=_("Collaborators Users"), value='{:,}'.format(total_collaborator_users).replace(',','.'), help=_("Total number of collaborators"))
    with users_metric_grid[3]:
        st.metric(label=_("Admin Users"), value='{:,}'.format(total_admin_users).replace(',','.'), help=_("Total number of admins"))

    tab1, tab2, tab3 = st.tabs(["All users", "Collaborators", "Admins"])
    with tab1:
        st.header(_("All users"))
    with tab2:
        st.header(_("Collaborators"))
    with tab3:
        st.header(_("Admins"))

    left_column, right_column = st.columns(2)

    left_column.plotly_chart(fig_users_by_year, use_container_width=True)
    right_column.plotly_chart(fig_admins_by_year, use_container_width=True)


    #Filter by date
    min_date = pd.to_datetime("today") - dt.timedelta(days=365)
    max_date = pd.to_datetime("today")

    #logs by date
    st.header(_("Logged users by date"))
    logs_range_dates = st.date_input(_("Select the date range for the logged users"), (min_date, max_date))
    logs_start_date = np.datetime64(logs_range_dates[0])
    logs_end_date = pd.to_datetime("today")
    if len(logs_range_dates)!=1:
        logs_end_date = np.datetime64(logs_range_dates[1])

    logs_selected_institution = logs_by_date_df[logs_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    logs_date_range = (logs_selected_institution["fecha"] >= logs_start_date) & (logs_selected_institution["fecha"] <= logs_end_date)
    logged_users_df = logs_selected_institution.loc[logs_date_range]
    left_column, right_column = st.columns(2)

    if len(logged_users_df.index) == 0:
        st.markdown("##### {}".format(_("There were no created users on this time period")))

    if len(logged_users_df.index) == 1:
        st.markdown("##### {} {} {} {}".format(_("There were"),_("users created on"),logged_users_df.iloc[0]["logged_users"],logged_users_df.iloc[0]["fecha"]))

    if len(logged_users_df.index) > 1:
        with left_column:
            date_users_df = logged_users_df[["fecha", "logged_users"]]
            st.dataframe(date_users_df)

        with right_column:
            st.markdown("##### {} ".format(_("Quantity of logged users by date")))
            fig_logged_users = plt.plot(logged_users_df["fecha"], logged_users_df["logged_users"])
            st.line_chart(data = date_users_df, x="fecha", y="logged_users", use_container_width=True)

    st.markdown("""---""")

    #Created users by date
    st.header(_("Created users by date"))
    users_created_range_dates = st.date_input(_("Select the date range for the created users"), (min_date, max_date))
    users_created_start_date = np.datetime64(users_created_range_dates[0])
    users_created_end_date = pd.to_datetime("today")
    if len(users_created_range_dates)!=1:
        users_created_end_date = np.datetime64(users_created_range_dates[1])
    users_created_selected_institution = users_created_by_date_df[users_created_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    users_created_date_range = (users_created_selected_institution["fecha"] >= users_created_start_date) & (users_created_selected_institution["fecha"] <= users_created_end_date)
    users_created_df = users_created_selected_institution.loc[users_created_date_range]
    left_column, right_column = st.columns(2)

    if len(users_created_df.index) == 0:
        st.markdown("##### {}".format(_("There were no created users on this time period")))

    if len(users_created_df.index) == 1:
        st.markdown("##### {} {} {} {}".format(_("There were"),_("users created on"),users_created_df.iloc[0]["created_users"],users_created_df.iloc[0]["fecha"]))

    if len(users_created_df.index) > 1:
        with left_column:
            date_users_df = users_created_df[["fecha", "created_users"]]
            st.dataframe(date_users_df)

        with right_column:
            st.markdown("##### {} ".format(_("Quantity of created users by date")))
            fig_created_users = plt.plot(users_created_df["fecha"], users_created_df["created_users"])
            st.line_chart(data = date_users_df, x="fecha", y="created_users", use_container_width=True)

    st.markdown("""---""")

    #Admin users created by date
    st.header(_("Created admin users by date"))
    admin_created_range_dates = st.date_input(_("Select the date range for the admin created users"), (min_date, max_date))
    admin_created_start_date = np.datetime64(admin_created_range_dates[0])
    admin_created_end_date = pd.to_datetime("today")
    if len(admin_created_range_dates)!=1:
        admin_created_end_date = np.datetime64(admin_created_range_dates[1])

    admin_created_selected_institution = admin_created_by_date_df[admin_created_by_date_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    admin_created_date_range = (admin_created_selected_institution["fecha"] >= users_created_start_date) & (admin_created_selected_institution["fecha"] <= admin_created_end_date)
    admin_created_df = admin_created_selected_institution.loc[admin_created_date_range]
    left_column, right_column = st.columns(2)

    if len(admin_created_df.index) == 0:
        st.markdown("##### {}".format(_("There're no created admin users on this time period")))

    if len(admin_created_df.index) == 1:
        st.markdown("##### {} {} {} {}".format(_("There were"),_("users created on"),admin_created_df.iloc[0]["created_admins"],admin_created_df.iloc[0]["fecha"]))

    if len(admin_created_df.index) > 1:
        with left_column:
            date_users_df = admin_created_df[["fecha", "created_admins"]]
            st.dataframe(date_users_df)

        with right_column:
            st.markdown("##### {} ".format(_("Quantity of created admin users by date")))
            fig_created_users = plt.plot(admin_created_df["fecha"], admin_created_df["created_admins"])
            st.line_chart(data = date_users_df, x="fecha", y="created_admins", use_container_width=True)
        
st.header(_("Learning Contents"))
with st.expander("**"+ _("Metrics")+"**", expanded=True):
    # Subjects information
    total_contents = int(df_institutions_selection["classes_count"].sum()) + int(df_institutions_selection["text_count"].sum()) + int(df_institutions_selection["scorm_count"].sum())
    total_programs_count = int(df_institutions_selection["programs_count"].sum())
    total_created_tests_count = int(df_institutions_selection["created_tests_count"].sum())
    total_created_questions = int(df_institutions_selection["created_questions"].sum())
    total_courses_count = int(df_institutions_selection["courses_count"].sum())
    total_finished_courses = int(df_institutions_selection["finished_courses"].sum())
    total_answered_questions_count = int(df_institutions_selection["answered_questions_count"].sum())
    total_correct_answers_count = int(df_institutions_selection["correct_answers_count"].sum())
    total_incorrect_answers_count = int(df_institutions_selection["incorrect_answers_count"].sum())
    total_attempts_count = int(df_institutions_selection["attempts_count"].sum())
    total_courses_views_count = int(df_course_selection["view_count"].sum())


    # Defining the grid to display the metrics
    rows = 3
    cols = 4

    learning_metrics_grid = []
    for row in range(rows):
        learning_metrics_grid.extend(st.columns(cols))

    st.markdown("""
        <style>
        [data-testid=column] [data-testid=stVerticalBlock]{
            gap: 0rem;
        }
        </style>
        """,unsafe_allow_html=True)

    learning_checkboxes = {}
    
    # Adding the metrics to the grid
    with learning_metrics_grid[0]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Created Programs"] = st.checkbox('', key="Created Programs", label_visibility="collapsed")
        st.metric(label=_("Created Programs"), value='{:,}'.format(total_programs_count).replace(',','.'), help=_('Total number of programs created'))
    with learning_metrics_grid[1]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Created Contents"] = st.checkbox('', key="Created Contents", label_visibility="collapsed")
        st.metric(label=_("Created Contents"), value='{:,}'.format(total_contents).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[2]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Created Courses"] = st.checkbox('', key="Created Courses", label_visibility="collapsed")
        st.metric(label=_("Created Courses"), value='{:,}'.format(total_courses_count).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[3]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Finished Courses"] = st.checkbox('', key="Finished Courses", label_visibility="collapsed")
        st.metric(label=_("Finished Courses"), value='{:,}'.format(total_finished_courses).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[4]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Courses Views"] = st.checkbox('', key="Courses Views", label_visibility="collapsed")
        st.metric(label=_("Courses Views"), value='{:,}'.format(total_courses_views_count).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[5]:
        left, center, right = st.columns([1, 3, 3])
        with center:
            learning_checkboxes["Created Tests"] = st.checkbox('', key="Created Tests", label_visibility="collapsed")
        st.metric(label=_("Created Tests"), value='{:,}'.format(total_created_tests_count).replace(',','.'), help=_('Total number of content items created'))

    for key, value in learning_checkboxes.items():
        if value == True:
            st.header("{} {}".format(key,_("by date")))
            # Include plot and other details here

    # Created Courses plots
    st.header(_("Course information by date"))
    course_views_selected_institution = courses_info_df[courses_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    course_views_range_dates = st.date_input(_("Select the date range to deploy the course information"), (min_date, max_date))
    course_views_start_date = np.datetime64(course_views_range_dates[0])
    course_views_end_date = pd.to_datetime("today")
    if len(course_views_range_dates)!=1:
        course_views_end_date = np.datetime64(course_views_range_dates[1])
    course_views_date_range = (course_views_selected_institution["create_time"] >= course_views_start_date) & (course_views_selected_institution["create_time"] <= course_views_end_date)
    course_views_df = course_views_selected_institution.loc[course_views_date_range]
    left_column, right_column = st.columns(2)
    created_courses_by_date = course_views_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")


    if len(course_views_df.index) == 0:
        st.markdown("##### {}".format(_("There're no created courses on this time period")))

    if len(course_views_df.index) == 1:
        st.markdown("##### {} {}".format(_("There was one created course on"),course_views_df.iloc[0]["create_time"]))

    if len(course_views_df.index) > 1:
        with left_column:
            st.dataframe(course_views_df[["title","create_time", "view_count", "author_id", "signed_users","user_finished_courses", "user_failed_courses"]].sort_values(by="create_time"))

        with right_column:
            st.markdown("##### {}".format(_("Courses created by date")))
            fig_created_users = plt.plot(created_courses_by_date)
            st.line_chart(data = created_courses_by_date, use_container_width=True)

# Questions metrics
st.header(_("Test Questions"))
with st.expander("**"+ _("Metrics")+"**"):
    questions_metrics_grid = []
    for row in range(2):
        questions_metrics_grid.extend(st.columns(4))
    with questions_metrics_grid[0]:
        st.metric(label=_("Created Questions"), value='{:,}'.format(total_created_questions).replace(',','.'), help=_('Total number of content items created'))
    with questions_metrics_grid[1]:
        st.metric(label=_("Answered Questions"), value='{:,}'.format(total_answered_questions_count).replace(',','.'), help=_('Total number of answers for all questions'))
    with questions_metrics_grid[2]:
        st.metric(label=_("Correct Answers"), value='{:,}'.format(total_correct_answers_count).replace(',','.'), help=_('Total number of correct answers for all questions'))
    with questions_metrics_grid[3]:
        st.metric(label=_("Incorrect Answers"), value='{:,}'.format(total_incorrect_answers_count).replace(',','.'), help=_('Total number of incorrect answers for all questions'))
    with questions_metrics_grid[4]:
        st.metric(label=_("Total Tries"), value='{:,}'.format(total_attempts_count).replace(',','.'), help=_('Total number of times a ___ has been tried to be answered'))


# Defining the grid to display the metrics
rows = 3
cols = 5

column_list = []
for row in range(rows):
    column_list.extend(st.columns(cols))


# Adding the metrics to the grid
with column_list[0]:
    st.metric(label=_("Created Programs"), value='{:,}'.format(total_programs_count).replace(',','.'), help=_('Total number of programs created'))
with column_list[1]:
    st.metric(label=_("Created Contents"), value='{:,}'.format(total_contents).replace(',','.'), help=_('Total number of content items created'))
with column_list[2]:
    st.metric(label=_("Created Courses"), value='{:,}'.format(total_courses_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[3]:
    st.metric(label=_("Finished Courses"), value='{:,}'.format(total_finished_courses).replace(',','.'), help=_('Total number of content items created'))
with column_list[4]:
    st.metric(label=_("Courses Views"), value='{:,}'.format(total_courses_views_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[5]:
    st.metric(label=_("Created Tests"), value='{:,}'.format(total_created_tests_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[6]:
    st.metric(label=_("Created Questions"), value='{:,}'.format(total_created_questions).replace(',','.'), help=_('Total number of content items created'))
with column_list[7]:
    st.metric(label=_("Answered Questions"), value='{:,}'.format(total_answered_questions_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[8]:
    st.metric(label=_("Correct Answers"), value='{:,}'.format(total_correct_answers_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[9]:
    st.metric(label=_("Incorrect Answers"), value='{:,}'.format(total_incorrect_answers_count).replace(',','.'), help=_('Total number of content items created'))
with column_list[10]:
    st.metric(label=_("Attempts Count"), value='{:,}'.format(total_attempts_count).replace(',','.'), help=_('Total number of content items created'))


st.markdown("""---""")


    
st.markdown("""---""")


st.header(_("Classes information by date"))
classes_views_selected_institution = classes_info_df[classes_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
classes_views_range_dates = st.date_input(_("Select the date range to deploy the classes information"), (min_date, max_date))
classes_views_start_date = np.datetime64(classes_views_range_dates[0])
classes_views_end_date = pd.to_datetime("today")
if len(classes_views_range_dates)!=1:
    classes_views_end_date = np.datetime64(course_views_range_dates[1])
classes_views_date_range = (classes_views_selected_institution["create_time"] >= classes_views_start_date) & (classes_views_selected_institution["create_time"] <= classes_views_end_date)
classes_views_df = classes_views_selected_institution.loc[classes_views_date_range]
left_column, right_column = st.columns(2)
created_classes_by_date = classes_views_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")




# News metrics
st.header(_("News"))
with st.expander("**"+ _("Metrics")+"**"):
    news_metrics_grid = []
    for row in range(1):
        news_metrics_grid.extend(st.columns(4))
    with news_metrics_grid[0]:
        st.metric(label=_("Created News"), value='{:,}'.format(total_created_news_count).replace(',','.'), help=_('Total number of news items created'))
    with news_metrics_grid[1]:
        st.metric(label=_("Total Views"), value='{:,}'.format(total_news_views_count).replace(',','.'), help=_('Total number of views'))
    with news_metrics_grid[2]:
        st.metric(label=_("Total Likes"), value='{:,}'.format(total_news_likes_count).replace(',','.'), help=_('Total number of likes'))
    with news_metrics_grid[3]:
        st.metric(label=_("Total Comments"), value='{:,}'.format(total_news_comments_count).replace(',','.'), help=_('Total number of comments'))

if len(classes_views_df.index) == 0:
    st.markdown("##### {}".format(_("There're no created classes on this time period")))

if len(classes_views_df.index) == 1:
    st.markdown("##### {} {}".format(_("There was one created classes on"),classes_views_df.iloc[0]["create_time"]))

if len(classes_views_df.index) > 1:
    with left_column:
        st.dataframe(classes_views_df[["title","create_time", "view_count"]].sort_values(by="create_time"))

    with right_column:
        st.markdown("##### {}".format(_("Classes created by date")))
        fig_created_classes = plt.plot(created_classes_by_date)
        st.line_chart(data = created_classes_by_date, use_container_width=True)
    
st.markdown("""---""")

st.header(_("Scorms information by date"))
scorms_views_selected_institution = scorms_info_df[scorms_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
scorms_views_range_dates = st.date_input(_("Select the date range to deploy the scorms information"), (min_date, max_date))
scorms_views_start_date = np.datetime64(scorms_views_range_dates[0])
scorms_views_end_date = pd.to_datetime("today")
if len(scorms_views_range_dates)!=1:
    scorms_views_end_date = np.datetime64(scorms_views_range_dates[1])
scorms_views_date_range = (scorms_views_selected_institution["create_time"] >= scorms_views_start_date) & (scorms_views_selected_institution["create_time"] <= scorms_views_end_date)
scorms_views_df = scorms_views_selected_institution.loc[scorms_views_date_range]
left_column, right_column = st.columns(2)
created_scorms_by_date = scorms_views_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")


if len(scorms_views_df.index) == 0:
    st.markdown("##### {}".format(_("There're no created scorms on this time period")))

if len(scorms_views_df.index) == 1:
    st.markdown("##### {} {}".format(_("There was one created scorm on"),scorms_views_df.iloc[0]["create_time"]))

if len(scorms_views_df.index) > 1:
    with left_column:
        st.dataframe(scorms_views_df[["title","create_time", "view_count"]].sort_values(by="create_time"))

    with right_column:
        st.markdown("##### {}".format(_("Scorms created by date")))
        fig_created_scorms = plt.plot(created_scorms_by_date)
        st.line_chart(data = created_scorms_by_date, use_container_width=True)
    
st.markdown("""---""")

st.header(_("Texts information by date"))
texts_views_selected_institution = texts_info_df[texts_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
texts_views_range_dates = st.date_input(_("Select the date range to deploy the texts information"), (min_date, max_date))
texts_views_start_date = np.datetime64(texts_views_range_dates[0])
texts_views_end_date = pd.to_datetime("today")
if len(texts_views_range_dates)!=1:
    texts_views_end_date = np.datetime64(texts_views_range_dates[1])
texts_views_date_range = (texts_views_selected_institution["create_time"] >= texts_views_start_date) & (texts_views_selected_institution["create_time"] <= texts_views_end_date)
texts_views_df = texts_views_selected_institution.loc[texts_views_date_range]
left_column, right_column = st.columns(2)
created_texts_by_date = texts_views_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")


if len(texts_views_df.index) == 0:
    st.markdown("##### {}".format(_("There're no created texts on this time period")))

if len(texts_views_df.index) == 1:
    st.markdown("##### {} {}".format(_("There was one created text on"),texts_views_df.iloc[0]["create_time"]))

if len(texts_views_df.index) > 1:
    with left_column:
        st.dataframe(texts_views_df[["title","create_time", "author_id"]].sort_values(by="create_time"))

    with right_column:
        st.markdown("##### {}".format(_("Texts created by date")))
        fig_created_texts = plt.plot(created_texts_by_date)
        st.line_chart(data = created_texts_by_date, use_container_width=True)

st.header(_("Tests information by date"))
tests_views_selected_institution = tests_info_df[tests_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
tests_views_range_dates = st.date_input(_("Select the date range to deploy the tests information"), (min_date, max_date))
tests_views_start_date = np.datetime64(tests_views_range_dates[0])
tests_views_end_date = pd.to_datetime("today")
if len(tests_views_range_dates)!=1:
    tests_views_end_date = np.datetime64(tests_views_range_dates[1])
tests_views_date_range = (tests_views_selected_institution["create_time"] >= tests_views_start_date) & (tests_views_selected_institution["create_time"] <= tests_views_end_date)
tests_views_df = tests_views_selected_institution.loc[tests_views_date_range]
left_column, right_column = st.columns(2)
created_tests_by_date = tests_views_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")


if len(tests_views_df.index) == 0:
    st.markdown("##### {}".format(_("There're no created tests on this time period")))

if len(tests_views_df.index) == 1:
    st.markdown("##### {} {}".format(_("There was one created test on"),tests_views_df.iloc[0]["create_time"]))

if len(tests_views_df.index) > 1:
    with left_column:
        st.dataframe(tests_views_df[["title","create_time", "author_id"]].sort_values(by="create_time"))

    with right_column:
        st.markdown("##### {}".format(_("Tests created by date")))
        fig_created_tests = plt.plot(created_tests_by_date)
        st.line_chart(data = created_tests_by_date, use_container_width=True)
        
st.markdown("""---""")

st.header(_("Satisfaction surverys information by date"))
satisfaction_surveys_selected_institution = satisfaction_surveys_df[texts_info_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]
satisfaction_surveys_range_dates = st.date_input(_("Select the date range to deploy the satisfaction surveys information"), (min_date, max_date))
satisfaction_surveys_start_date = np.datetime64(satisfaction_surveys_range_dates[0])
satisfaction_surveys_end_date = pd.to_datetime("today")
if len(satisfaction_surveys_range_dates)!=1:
    satisfaction_surveys_end_date = np.datetime64(satisfaction_surveys_range_dates[1])
satisfaction_surveys_date_range = (satisfaction_surveys_selected_institution["item_create_time"] >= satisfaction_surveys_start_date) & (satisfaction_surveys_selected_institution["item_create_time"] <= texts_views_end_date)
satisfaction_surveys_df = satisfaction_surveys_selected_institution.loc[satisfaction_surveys_date_range]
left_column, right_column = st.columns(2)
satisfaction_surveys_by_date = satisfaction_surveys_df.groupby(by=["item_create_time"]).agg("count")[["test_title"]].sort_values(by="item_create_time")


if len(satisfaction_surveys_df.index) == 0:
    st.markdown("##### {}".format(_("There're no created satisfaction surveys on this time period")))

if len(satisfaction_surveys_df.index) == 1:
    st.markdown("##### {} {}".format(_("There was one created satisfaction_surveys on"),satisfaction_surveys_df.iloc[0]["item_create_time"]))

if len(satisfaction_surveys_df.index) > 1:
    with left_column:
        st.dataframe(satisfaction_surveys_df[["test_title","course_title","reactivo","item_create_time","respuesta","max_ptje", "min_ptje", "author_id"]].sort_values(by="item_create_time"))

    with right_column:
        st.markdown("##### {}".format(_("Satisfaction surveys created by date")))
        fig_satisfaction_surveys = plt.plot(satisfaction_surveys_by_date)
        st.line_chart(data = satisfaction_surveys_by_date, use_container_width=True)
    
st.markdown("""---""")


metrics_keys = [
    "Total Users",
    "Active Users",
    "Collaborator Users",
    "Admin Users",
    "Created Programs",
    "Created Contents",
    "Created Courses",
    "Courses views",
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
    total_courses_views_count,
    total_finished_courses,
    total_answered_questions_count,
    total_correct_answers_count,
    total_incorrect_answers_count,
    total_news_likes_count,
    total_news_views_count,
    total_news_comments_count,
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
                    _("Download .csv"),
                    data=metrics_df.to_csv(index=False),
                    file_name=f"metrics.csv",
                    mime="text/csv",
                    key='download-csv'
                    )

# Botón de descarga en formato excel
with col2:
    st.download_button(
                    _("Download (excel format)"),
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
                _("Download Report (pdf)"),
                data=canvas.getpdfdata(),
                file_name=f"report_{institution}.pdf",
                mime="application/pdf",
                )
