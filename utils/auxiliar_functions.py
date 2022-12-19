import pandas as pd
from io import BytesIO
from PIL import Image
import datetime

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