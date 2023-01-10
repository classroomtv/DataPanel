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


DEFAULT_PAGE = "main.py"

# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            current_pages[key]["page_name"] = ''
            _on_pages_changed.send()
            break

def load_database(path):
    dataFrame = pd.read_csv(path, on_bad_lines="skip")
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
    "Created Surveys": ["title", "create_time", "view_count", "author_id"]
}

def show_data_by_date(title, data, df_institutions_selection):
    st.markdown("""---""")
    min_date = pd.to_datetime("today") - dt.timedelta(days=365)
    max_date = pd.to_datetime("today")
    columns_to_show = columns_for_metric[title]

    data_selected_institution = data[data["institution_id"] == df_institutions_selection.iloc[0]["id"]]
    data_range_dates = st.date_input("Select the date range to deploy the information", (min_date, max_date), key=f'{title}_date_input')
    data_start_date = np.datetime64(data_range_dates[0])
    data_end_date = pd.to_datetime("today")
    
    if len(data_range_dates)!=1:
        data_end_date = np.datetime64(data_range_dates[1])
        
    data_date_range = (data_selected_institution["create_time"] >= data_start_date) & (data_selected_institution["create_time"] <= data_end_date)
    data_df = data_selected_institution.loc[data_date_range]
    left_column, right_column = st.columns(2)
    created_elements_by_date = data_df.groupby(by=["create_time"]).agg("count")[["title"]].sort_values(by="create_time")

    if len(data_df.index) == 0:
        st.markdown("##### There're no created items on this time period")
    if len(data_df.index) == 1:
        st.markdown("##### There was one item created on {}".format(data_df.iloc[0]["create_time"]))
    if len(data_df.index) > 1:
        with left_column:
            st.dataframe(data_df[columns_to_show].sort_values(by="create_time"))
        with right_column:
            st.markdown(f"##### {title} by date")
            st.line_chart(data=created_elements_by_date, use_container_width=True)
    return
