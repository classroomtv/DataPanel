import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
from utils.auxiliar_functions import to_excel, plotly_fig2array, get_year_range, hide_page, nav_page
########## libraries for building the pdf reports
from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from streamlit_google_oauth import logout_button

### Data loading
institutions_df = pd.read_csv("pages/Database/institutions.csv" )
users_df = pd.read_csv("pages/Database/users_by_date.csv" )
courses_info_df = pd.read_csv("pages/Database/courses_info.csv", on_bad_lines='skip')


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="General Stats", page_icon=":bar_chart:", layout="wide")

# ---- SIDEBAR ----
if "client" in st.session_state:
    hide_page('main')
    with st.sidebar:
        logout_button('Logout')
else:
    nav_page('')

name = 'bharath'
st.sidebar.title(f"Welcome {name}")

# Selecting institution
institution = st.sidebar.multiselect(
    "Select the institutions to show:",
    options=institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique(),
    default=institutions_df[institutions_df["collaborator_users"]>=3]["name"].unique(),
)


df_selection = institutions_df.query(
    "name == @institution")
df_users_selection = users_df.query(
    "Cliente == @institution")
df_course_selection = courses_info_df.query(
    "name == @institution")

# Total number of institutions
total_institutions = int(df_selection.shape[0])

year_list = get_year_range(2018)
# Users by year
users_by_year = [
    df_users_selection["Usuarios cargados 2018"].sum(),
    df_users_selection["Usuarios cargados 2019"].sum(),
    df_users_selection["Usuarios cargados 2020"].sum(),
    df_users_selection["Usuarios cargados 2021"].sum(),
    df_users_selection["Usuarios cargados 2022"].sum()]

# Logged users by year
logged_users_by_year = [
    df_users_selection["Usuarios con ingreso a plataforma 2019"].sum(),
    df_users_selection["Usuarios con ingreso a plataforma 2020"].sum(),
    df_users_selection["Usuarios con ingreso a plataforma 2021"].sum(),
    df_users_selection["Usuarios con ingreso a plataforma 2022"].sum()]

#Collaborators Users by institution
collaborators_by_institution = (
    df_selection.groupby(by=["name"]).sum()[["collaborator_users"]].sort_values(by="collaborator_users").tail(15)
)

# Admin by institution
admin_by_institution = (
    df_selection.groupby(by=["name"]).sum()[["admin_users"]].sort_values(by="admin_users").tail(15)
)

# Created courses by date
created_courses_by_date = (
    df_course_selection.groupby(by=["name"]).agg("count")[["id"]].sort_values(by="id").tail(15)
)

# Courses views by institution
courses_views_by_institution = (
    df_course_selection.groupby(by=["name"]).sum()[["view_count"]].sort_values(by="view_count").tail(15)
)


# ---- MAINPAGE ----
st.title(":bar_chart: General Institutions Stats")
st.metric(label="Total Institutions", value='{:,}'.format(total_institutions).replace(',','.'), help='Total number of institutions with at least 3 users')
st.markdown("""---""")
st.markdown("##")

### Top Metrics
# Metrics for users
st.header("Users Metrics")

total_users = int(df_users_selection["Usuarios totales"].sum()) 
total_active_users = int(df_users_selection["Usuarios activos"].sum()) 
total_collaborator_users = int(df_selection["collaborator_users"].sum()) 
total_admin_users = int(df_selection["admin_users"].sum())

# Defining the grid to display the users metrics
users_metric_grid = []
for row in range(1):
    users_metric_grid.extend(st.columns(4))

with users_metric_grid[0]:
    st.metric(label="Total Users", value='{:,}'.format(total_users).replace(',','.'), help='Total number of users')
with users_metric_grid[1]:
    st.metric(label="Active Users", value='{:,}'.format(total_active_users).replace(',','.'), help='Total number of active users')
with users_metric_grid[2]:
    st.metric(label="Collaborators Users", value='{:,}'.format(total_collaborator_users).replace(',','.'), help='Total number of collaborators')
with users_metric_grid[3]:
    st.metric(label="Admin Users", value='{:,}'.format(total_admin_users).replace(',','.'), help='Total number of admins')

# Plot 1: Amount of users by year
fig_users_by_year = px.bar(
    users_by_year,
    x=year_list ,
    y=users_by_year,
    orientation="v",
    title="<b>Total users by year</b>",
    color_discrete_sequence=["#0083B8"] * len(users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_users_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

# Plot 2: Amount of logged users by year
fig_logs_by_year = px.bar(
    logged_users_by_year,
    x=year_list[1:] ,
    y=logged_users_by_year,
    orientation="v",
    title="<b>Logged users by year</b>",
    color_discrete_sequence=["#0083B8"] * len(logged_users_by_year),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_logs_by_year.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_users_by_year, use_container_width=True)
right_column.plotly_chart(fig_logs_by_year, use_container_width=True)

# Plot 3: Amount of users by institutions
fig_users_by_institution = px.bar(
    collaborators_by_institution,
    x="collaborator_users",
    y=collaborators_by_institution.index,
    orientation="h",
    title="<b>Collaborators users by institution</b>",
    color_discrete_sequence=["#0083B8"] * len(collaborators_by_institution),
    template="plotly_white",
    labels={'x': 'Collaborator users', 'y':'Institution'}
)
fig_users_by_institution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

# Plot 4: Amount of admins by institutions
fig_admin_by_institution = px.bar(
    admin_by_institution,
    x="admin_users",
    y=admin_by_institution.index,
    orientation="h",
    title="<b>Admin users by institution</b>",
    color_discrete_sequence=["#0083B8"] * len(admin_by_institution),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_admin_by_institution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_users_by_institution, use_container_width=True)
right_column.plotly_chart(fig_admin_by_institution, use_container_width=True)


#Courses information
st.markdown("""---""")
st.header("Courses metrics")

total_contents = int(df_selection["classes_count"].sum()) + int(df_selection["text_count"].sum()) + int(df_selection["scorm_count"].sum())
total_programs_count = int(df_selection["programs_count"].sum())
total_created_tests_count = int(df_selection["created_tests_count"].sum())
total_created_questions = int(df_selection["created_questions"].sum())
total_courses_count = int(df_selection["courses_count"].sum())
total_finished_courses = int(df_selection["finished_courses"].sum())
total_answered_questions_count = int(df_selection["answered_questions_count"].sum())
total_correct_answers_count = int(df_selection["correct_answers_count"].sum())
total_incorrect_answers_count = int(df_selection["incorrect_answers_count"].sum())
total_attempts_count = int(df_selection["attempts_count"].sum())
total_courses_views_count = int(df_course_selection["view_count"].sum())


# Defining the grid to display the courses metrics

courses_metric_grid = []
for row in range(3):
    courses_metric_grid.extend(st.columns(5))

# Adding the courses' metrics to the grid
with courses_metric_grid[0]:
    st.metric(label="Created Programs", value='{:,}'.format(total_programs_count).replace(',','.'), help='Total number of programs created')
with courses_metric_grid[1]:
    st.metric(label="Created Contents", value='{:,}'.format(total_contents).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[2]:
    st.metric(label="Created Courses", value='{:,}'.format(total_courses_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[3]:
    st.metric(label="Finished Courses", value='{:,}'.format(total_finished_courses).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[4]:
    st.metric(label="Courses Views", value='{:,}'.format(total_courses_views_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[5]:
    st.metric(label="Created Tests", value='{:,}'.format(total_created_tests_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[6]:
    st.metric(label="Created Questions", value='{:,}'.format(total_created_questions).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[7]:
    st.metric(label="Answered Questions", value='{:,}'.format(total_answered_questions_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[8]:
    st.metric(label="Correct Answers", value='{:,}'.format(total_correct_answers_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[9]:
    st.metric(label="Incorrect Answers", value='{:,}'.format(total_incorrect_answers_count).replace(',','.'), help='Total number of content items created')
with courses_metric_grid[10]:
    st.metric(label="Attempts Count", value='{:,}'.format(total_attempts_count).replace(',','.'), help='Total number of content items created')

# Plot 5
fig_created_courses_by_institution = px.bar(
    created_courses_by_date,
    x="id",
    y=created_courses_by_date.index,
    orientation="h",
    title="<b>Created courses by Institution</b>",
    color_discrete_sequence=["#0083B8"] * len(created_courses_by_date),
    template="plotly_white",
)
fig_created_courses_by_institution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)


# Plot 6
fig_courses_view_by_institution = px.bar(
    courses_views_by_institution,
    x="view_count",
    y=courses_views_by_institution.index,
    orientation="h",
    title="<b>Courses views count by Institution</b>",
    color_discrete_sequence=["#0083B8"] * len(courses_views_by_institution),
    template="plotly_white",
    labels={'x': 'Year', 'y':'Users'}
)
fig_courses_view_by_institution.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_created_courses_by_institution, use_container_width=True)
right_column.plotly_chart(fig_courses_view_by_institution, use_container_width=True)


# News stats
st.markdown("""---""")
st.header("News general stats")

total_created_news_count = int(df_selection["created_news_count"].sum())
total_news_likes_count = int(df_selection["likes_count"].sum())
total_news_views_count = int(df_selection["new_views_count"].sum())
total_news_comments_count = int(df_selection["comments_count"].sum())

news_metrics_grid = []
for row in range(1):
    news_metrics_grid.extend(st.columns(4))

with news_metrics_grid[0]:
    st.metric(label="Created News", value='{:,}'.format(total_created_news_count).replace(',','.'), help='Total number of news items created')
with news_metrics_grid[1]:
    st.metric(label="News Views", value='{:,}'.format(total_news_views_count).replace(',','.'), help='Total number of views')
with news_metrics_grid[2]:
    st.metric(label="News Likes Count", value='{:,}'.format(total_news_likes_count).replace(',','.'), help='Total number of likes')
with news_metrics_grid[3]:
    st.metric(label="Comments Count", value='{:,}'.format(total_news_comments_count).replace(',','.'), help='Total number of comments')


metrics_keys = [
    "Total Institutions",
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
    total_institutions,
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
    total_attempts_count,
    total_news_likes_count,
    total_news_views_count,
    total_news_comments_count,
]

# Dataframe with all metrics to be downloaded
metrics_data = []
for index_metric in range(len(metrics_keys)):
    metrics_data.append([metrics_keys[index_metric], metrics_values[index_metric]])

metrics_df = pd.DataFrame(metrics_data, columns=["Metric", "Value"], index=None)

col1, col2 = st.columns(2)

# Download button for csv file
with col1:
    st.download_button(
                    "Download .csv",
                    data=metrics_df.to_csv(index=False),
                    file_name=f"metrics.csv",
                    mime="text/csv",
                    key='download-csv'
                    )

# Download button for excel file
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

### PDF report generation
template = PdfReader("assets/template_report.pdf", decompress=False).pages[0]
template_obj = pagexobj(template)

canvas = Canvas('report')

xobj_name = makerl(canvas, template_obj)
canvas.doForm(xobj_name)

#canvas.setFont('psfontname', size, leading = None)


ystart = 0

# Title and institution count
canvas.drawCentredString(297, 773, "All Institutions")
canvas.drawCentredString(297, 676, "Number of Institutions")
canvas.drawCentredString(297, 652, '{:,}'.format(total_institutions).replace(',','.'))

# Users stats
canvas.drawString(45, 565, '{:,}'.format(total_users).replace(',','.'))
canvas.drawString(170, 567, '{:,}'.format(total_active_users).replace(',','.'))
canvas.drawString(335, 565, '{:,}'.format(total_collaborator_users).replace(',','.'))
canvas.drawString(490, 567, '{:,}'.format(total_admin_users).replace(',','.'))

# Plots
plot1 = plotly_fig2array(fig_users_by_year)
plot2 = plotly_fig2array(fig_logs_by_year)
plot3 = plotly_fig2array(fig_users_by_institution)
plot4 = plotly_fig2array(fig_admin_by_institution)

plot_w = 120
plot_h = 120
canvas.drawInlineImage(plot1, 45, 400, width=plot_w, height=plot_h)
canvas.drawInlineImage(plot2, 45 + plot_w + 10, 400, width=plot_w, height=plot_h)
canvas.drawInlineImage(plot3, 45 + 2*plot_w + 20, 400, width=plot_w, height=plot_h)
canvas.drawInlineImage(plot4, 45 + 3*plot_w + 30, 400, width=plot_w, height=plot_h)

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
                file_name=f"report.pdf",
                mime="application/pdf",
                )
