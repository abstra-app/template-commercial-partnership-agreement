import pandas as pd
from abstra import *
import json
from datetime import datetime
import plotly.express as px
import numpy as np
import plotly.graph_objs as go
import os
from abstra.tables import Tables
from abstra.dashes import get_user

# Authenticate abstra team members
user = get_user()
if not user.email.endswith('@abstra.app'):
  exit()

tables_key =os.getenv("TABLES_API_TOKEN")
query_id = os.getenv("GET_SUBMISSIONS_QUERY_ID")

# Get submissions from Tables
tables = Tables(api_key=tables_key)
statement = tables.statement(id=query_id)
result = statement.run()

# Transform into dataframe
df = pd.DataFrame(result)

# Convert 'created_at' and 'updated_at' columns to datetime objects
df['created_at'] = pd.to_datetime(df['created_at'])
df['updated_at'] = pd.to_datetime(df['updated_at'])
 

# Replace the missing 'created_at' values with the corresponding 'updated_at' values
df['created_at'].fillna(df['updated_at'], inplace=True)

# Strip time from datetime
df['created_at'] = df['created_at'].dt.date

# Initialize variables to filter dataframe
selected_start_date = datetime.strptime("2023-06-01", "%Y-%m-%d").date()
ascending = False

print (df['created_at'])

# Create dynamic dataframe
def get_df():
    # First, filter the DataFrame by the date
    filtered_df = df[df['created_at'] >= selected_start_date]

    # Then, select the desired columns
    filtered_df = filtered_df[
        [
            'created_at',
            'nome',
            'email',
            'telefone',
            'empresa',
            'industria',
            'site',
            'ideia',
            'budget'
        ]
    ]

    # Rename columns
    filtered_df.rename(columns={"created_at": "Date",
                                 "nome": "Nome",
                                 "email": "Email",
                                 "telefone":"telefone",
                                 "empresa":"Emporesa",
                                 "industria":"Indústria",
                                 "site":"Site",
                                 "ideia":"Ideia",
                                 "budget":"Budget"},
                                 inplace=True)
    
    # Sort filtered_df by 'Date' in correct order
    filtered_df = filtered_df.sort_values(by='Date', ascending=ascending)

    return filtered_df

# Initialize variable
submissions = len(df.index)

# Create plotly bar chart
def get_chart():
    chart_data = get_df()

    # Group submissions by day
    chart_data = chart_data.groupby('Date').size().reset_index(name='submissions')

    # Define x and y axes, draw chart
    trace1 = go.Bar(
        x=chart_data['Date'],
        y=chart_data['submissions']
    )
    data = [trace1]

    # Plot figure
    fig = go.Figure(data=data)

    return fig

