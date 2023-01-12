import pandas as pd
from io import BytesIO
from PIL import Image
import datetime
from streamlit.components.v1 import html
from streamlit.source_util import _on_pages_changed, get_pages
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import plotly.express as px 


DEFAULT_PAGE = "main.py"

# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            current_pages[key]["page_name"] = ''
            _on_pages_changed.send()
            break

def plot_users(user_dataframe ,title, x_label, y_label):
    users_by_year = user_dataframe.groupby(user_dataframe["create_time"].dt.year).agg({"user_id": "count"})
    users_by_year = users_by_year[users_by_year.index > 1970]

    fig_users_by_year = px.bar(
        users_by_year,
        x=users_by_year.index ,
        y=users_by_year.user_id,
        orientation="v",
        title="<b>{}</b>".format(title),
        color_discrete_sequence=["#0083B8"] * len(users_by_year),
        template="plotly_white",
        labels={"create_time": x_label, "user_id": y_label}
        )

    fig_users_by_year.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
    )
    return fig_users_by_year

def plot_top_institutions(df_selection, selected_col, title, x_label, y_label):
    group_by_institution = (
        df_selection.groupby(by=["name"]).sum()[[selected_col]].sort_values(by=selected_col).tail(15)
    )
        # Plot 5
    fig_created_courses_by_institution = px.bar(
        group_by_institution,
        x=selected_col,
        y=group_by_institution.index,
        orientation="h",
        title="<b>{}</b>".format(title),
        color_discrete_sequence=["#0083B8"] * len(group_by_institution),
        template="plotly_white",
        labels={selected_col: x_label, "name": y_label}
    )
    fig_created_courses_by_institution.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
    )
    return fig_created_courses_by_institution


def load_database(path):
    dataFrame = pd.read_csv(path, on_bad_lines="skip", index_col=0)
    for (columnName,columnDataType) in zip(dataFrame.columns,dataFrame.dtypes):
        if columnDataType == "float64":
            dataFrame[columnName] = dataFrame[columnName].astype('Int64')
        if columnName[-4:] == "time":
            dataFrame[columnName] = pd.to_datetime(dataFrame[columnName], infer_datetime_format=True)
    return dataFrame

def nav_page(page_name, timeout_secs=3):
    print(f'nav to {page_name}')
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    console.log(links[i]);
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


def set_code(code: str):
    st.experimental_set_query_params(code=code)


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, index=False, sheet_name='Sheet1') 
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def plotly_fig2array(fig):
    #convert Plotly fig to an array
    fig_bytes = fig.to_image(format="png")
    buf = BytesIO(fig_bytes)
    img = Image.open(buf)
    return img


def get_year_range(start_year, end_year=datetime.date.today().year):
    return [year for year in range(start_year, end_year+1)]

columns_for_metric = {
    "Created Courses": ["title", "create_time", "view_count", "author_id", "signed_users", "user_finished_courses", "user_failed_courses"],
    "Created Classes": ["title", "create_time", "view_count", "author_id"],
    "Created Scorms": ["title", "create_time", "view_count", "author_id"],
    "Created Tests": ["title", "create_time", "author_id"],
    "Created Texts": ["title", "create_time", "author_id"],
    "Created Surveys": ["test_title", "create_time", "view_count", "author_id", "reactive", "answer"],
    "Created Users": ["create_time", "created_users"],
    "Logged Users": ["create_time", "logged_users"],
    "Created Admin": ["create_time", "created_admins"],
    "Created Surveys": ["create_time","title", "course_title", "reactive","answer","author_id"]

}

column_names = {"en": {"title": "Title", "create_time": "Create time", "view_count": "View count", "author_id" : "Author id",
                "signed_users": "Signed users", "user_finished_courses" : "User that finished the course", "user_failed_courses":"User that failed the course",
                 "created_users": "Created users", "logged_users":"Logged users", "created_admins": "Created admins"},
                "es": {"title": "Título", "create_time": "Fecha de creación", "view_count": "Cantidad de visitas", "author_id": "Id del autor",
                "signed_users": "Usuarios inscritos", "user_finished_courses": "Usuarios que han finalizado el curso", "user_failed_courses": "Usuarios que han fallado el curso",
                "created_users": "Usuarios creados", "logged_users": "Usuarios con ingreso", "created_admins":"Administradores creados"}}

input_texts = {"date_input_text": {"en": "Select the date range to deploy the information", "es": "Seleccione un rango de fechas para mostrar la información"},
                "no_items_created": {"en": "There're no created items on this time period", "es": "No hay items creados en este período de tiempo"},
                "one_item_created": {"en": "There was one item created on", "es": "Se creó solo un item en "},
                "by_date": {"en": "by date", "es": "por fecha"} ,
                "Created Courses":{"en": "Created Courses", "es": "Cursos Creados"},
                "Created Classes":{"en": "Created Classes", "es": "Clases Creadas"},
                "Created Scorms":{"en": "Created Scorms", "es": "Scorms Creados"},
                "Created Tests":{"en": "Created Tests", "es": "Evaluaciones Creadas"},
                "Created Texts":{"en": "Created Texts", "es": "Textos Creados"},
                "Created Surveys":{"en": "Created Surveys", "es": "Encuestas Creadas"},
                "Created Users":{"en": "Created Users", "es": "Usuarios Creados"},
                "Created Admin":{"en": "Created Admin", "es": "Administradores Creados"},
                "Logged Users":{"en": "Logged Users", "es": "Usuarios con ingreso"},
                "Created Surveys":{"en": "Created Satisfaction Surveys", "es": "Encuestas de Satisfacción Creadas"}}

def show_data_by_date(title, data, df_institutions_selection,language,infoType):
    st.markdown("""---""")
    min_date = pd.to_datetime("today") - dt.timedelta(days=365)
    max_date = pd.to_datetime("today")
    columns_to_show = columns_for_metric[title]

    data_selected_institution = data[data["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    data_range_dates = st.date_input(input_texts["date_input_text"][language], (min_date, max_date), key=f'{title}_date_input')
    data_start_date = np.datetime64(data_range_dates[0])
    data_end_date = pd.to_datetime("today")
    
    if len(data_range_dates)!=1:
        data_end_date = np.datetime64(data_range_dates[1])
        
    data_date_range = (data_selected_institution["create_time"] >= data_start_date) & (data_selected_institution["create_time"] <= data_end_date)
    data_df = data_selected_institution.loc[data_date_range]
    left_column, right_column = st.columns(2)

    if infoType=="Data":
        created_elements_by_date = data_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")
    if infoType=="Users":
        created_elements_by_date = data_df.groupby(by=["create_time"]).agg("sum")["user_id"].sort_values(by="create_time")

    if len(data_df.index) == 0:
        st.markdown("##### {}".format(input_texts["no_items_created"][language]))
    if len(data_df.index) == 1:
        st.markdown("##### {} {}".format(input_texts["one_item_created"][language],data_df.iloc[0]["create_time"]))
    if len(data_df.index) > 1:
        with left_column:
            translatedNames = column_names[language]
            st.dataframe(data_df[columns_to_show].rename(columns=translatedNames).sort_values(by=translatedNames["create_time"]))
        with right_column:
            st.markdown("##### {} {}".format(input_texts[title][language],input_texts["by_date"][language]))
            st.line_chart(data=created_elements_by_date, use_container_width=True)
    return
    
    

