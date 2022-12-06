import pandas as pd
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output)
    df.to_excel(writer, index=False, sheet_name='Sheet1') 
    writer.save()
    processed_data = output.getvalue()
    return processed_data