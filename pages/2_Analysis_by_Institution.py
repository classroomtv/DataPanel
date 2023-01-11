import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import gettext
import streamlit_nested_layout
from utils.auxiliar_functions import to_excel, plotly_fig2array, nav_page, get_year_range, show_data_by_date, load_database
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
print(st.experimental_get_query_params())
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


institutions_df = load_database("pages/Database/institutions.csv" )

users_df = load_database("pages/Database/users_by_date.csv" )

logs_by_date_df = load_database("pages/Database/logs_by_date.csv")

users_created_by_date_df = load_database("pages/Database/users_created_by_date.csv")

collaborators_created_by_date_df = users_created_by_date_df.loc[["is_admin"]==0]

admin_created_by_date_df = users_created_by_date_df.loc[["is_admin"]==1]

courses_info_df = load_database("pages/Database/courses_info.csv")

classes_info_df = load_database("pages/Database/classes_info.csv")

scorms_info_df = load_database("pages/Database/scorms_info.csv")

tests_info_df = load_database("pages/Database/tests_info.csv")

texts_info_df = load_database("pages/Database/texts_info.csv")

satisfaction_surveys_df = load_database("pages/Database/satisfaction_surveys.csv")

dataframes_dict = {
    "Created Programs": None,
    "Created Courses": courses_info_df,
    "Created Classes": classes_info_df,
    "Created Scorms": scorms_info_df,
    "Created Tests": tests_info_df,
    "Created Texts": texts_info_df,
    "Created Surveys": satisfaction_surveys_df
}
# ---- SIDEBAR ----
name = 'bharath'
st.sidebar.title("{} {}".format(_("Welcome"), name))

available_institutions = institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique()
forus_id = np.where(available_institutions == "Forus")[0][0]
institution = st.sidebar.selectbox(
    _("Select an institution")+":",
    options=available_institutions, index=int(forus_id))

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

fig_logged_users_by_year = px.bar(
    users_by_year,
    x=year_list[1:] ,
    y=users_by_year,
    orientation="v",
    title="<b>{}</b>".format(_("Logged Users by Year")),
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={"x": _("Year"), "y":_('Users')}
)
fig_logged_users_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

st.title("Users")


with st.expander("**"+ _("Metrics")+"**", expanded=False):
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
        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_users_by_year, use_container_width=True)
        right_column.plotly_chart(fig_logged_users_by_year, use_container_width=True)
        st.header(_("Logged users by date"))
        show_data_by_date("Logged Users", logs_by_date_df, df_institutions_selection,language, "Users")

    with tab2:
        st.header(_("Collaborators"))
        st.header(_("Created users by date"))
        show_data_by_date("Created Users", users_created_by_date_df, df_institutions_selection,language, "Users")

    with tab3:
        st.header(_("Admins"))
        st.header(_("Created admin users by date"))
        show_data_by_date("Created Admin", admin_created_by_date_df, df_institutions_selection,language, "Users")


        
st.header(_("Learning Contents"))
with st.expander("**"+ _("Metrics")+"**", expanded=False):
    # Subjects information
    total_programs_count = int(df_institutions_selection["programs_count"].sum())
    total_texts_count = int(df_institutions_selection["text_count"].sum())
    total_classes_count = int(df_institutions_selection["classes_count"].sum())
    total_scorms_count = int(df_institutions_selection["scorm_count"].sum())
    total_contents = total_classes_count + total_texts_count + total_scorms_count
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
        left, right = st.columns([1, 12])
        with right:
            st.metric(label=_("Created Programs"), value='{:,}'.format(total_programs_count).replace(',','.'), help=_('Total number of programs created'))
    with learning_metrics_grid[1]:
        left, right = st.columns([1, 12])
        with left:
            learning_checkboxes["Created Courses"] = st.checkbox(' ', key="Created Courses", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Courses"), value='{:,}'.format(total_courses_count).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[2]:
        left, right = st.columns([1, 12])
        with right:
            st.metric(label=_("Finished Courses"), value='{:,}'.format(total_finished_courses).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[3]:
        left, right = st.columns([1, 12])
        with right:
            st.metric(label=_("Courses Views"), value='{:,}'.format(total_courses_views_count).replace(',','.'), help=_('Total number of content items created'))
    with learning_metrics_grid[4]:
        left, right = st.columns([1, 12])
        with left:
            learning_checkboxes["Created Classes"] = st.checkbox(' ', key="Created Classes", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Classes"), value='{:,}'.format(total_classes_count).replace(',','.'), help=_('Total number of classes items created'))
    with learning_metrics_grid[5]:
        left, right = st.columns([1, 12])
        with left:
            learning_checkboxes["Created Texts"] = st.checkbox(' ', key="Created Texts", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Texts"), value='{:,}'.format(total_texts_count).replace(',','.'), help=_('Total number of texts items created'))
    with learning_metrics_grid[6]:
        left, right = st.columns([1, 12])
        with left:
            learning_checkboxes["Created Scorms"] = st.checkbox(' ', key="Created Scorms", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Scorms"), value='{:,}'.format(total_scorms_count).replace(',','.'), help=_('Total number of scorms items created'))
    with learning_metrics_grid[7]:
        left, right = st.columns([1, 12])
        with left:
            learning_checkboxes["Created Tests"] = st.checkbox(' ', key="Created Tests", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Tests"), value='{:,}'.format(total_created_tests_count).replace(',','.'), help=_('Total number of content items created'))

    for key, value in learning_checkboxes.items():
        if value == True:
            st.header(f"{key} by date")
            show_data_by_date(key, dataframes_dict[key], df_institutions_selection,language,"Data")

    
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

# Satisfaction Surveys metrics
st.header(_("Satisfaction Surveys"))
with st.expander("**"+ _("Metrics")+"**"):
    satisfaction_surveys_metrics_grid = []
    for row in range(rows):
        satisfaction_surveys_metrics_grid.extend(st.columns(cols))
    satisfaction_surveys_checkboxes = {}
    total_satisfaction_surveys_count = int(len(satisfaction_surveys_df[satisfaction_surveys_df["institution_id"] == df_institutions_selection.iloc[0]["id"]]))

    for row in range(1):
        satisfaction_surveys_metrics_grid.extend(st.columns(4))

    with satisfaction_surveys_metrics_grid[0]:
        left, right = st.columns([1, 12])
        with left:
            satisfaction_surveys_checkboxes["Created Surveys"] = st.checkbox(' ', key="Created Surveys", label_visibility="collapsed")
        with right:
            st.metric(label=_("Created Surveys"), value='{:,}'.format(total_satisfaction_surveys_count).replace(',','.'), help=_('Total number of news items created'))

    for key, value in satisfaction_surveys_checkboxes.items():
        if value == True:
            st.header(f"{key} by date")
            show_data_by_date(key, dataframes_dict[key], df_institutions_selection,language,"Data")

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

col1, col2, col3 = st.columns(3)
# Botón de descarga en formato csv
with col1:
    st.download_button(
                    label=_("Download as csv"),
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
plot2 = plotly_fig2array(fig_logged_users_by_year)

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

with col3:
    st.download_button(
                    _("Download pdf report"),
                    data=canvas.getpdfdata(),
                    file_name=f"report_{institution}.pdf",
                    mime="application/pdf",
                    )

