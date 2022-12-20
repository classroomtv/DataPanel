import pandas as pd
from io import BytesIO
from PIL import Image
import datetime
from streamlit.components.v1 import html
from streamlit.source_util import _on_pages_changed, get_pages


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

DEFAULT_PAGE = "main.py"

# Hide default page
def hide_page(name: str):
    current_pages = get_pages(DEFAULT_PAGE)

    for key, val in current_pages.items():
        if val["page_name"] == name:
            current_pages[key]["page_name"] = ''
            _on_pages_changed.send()
            break

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