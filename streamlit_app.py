import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
# import requests
from plotly.subplots import make_subplots
import pandas as pd

def make_specs( rows : int, cols : int, n : int) -> dict:
    """Makes the list of dictionaries to set the layout for the function make_subplots, especially for primes and specific grids.

    Args:
        rows (int): Number of rows for the grid
        cols (int): Number of columns for the grid
        n (int): Total number of figures

    Returns:
        dict: Grid for plotting
    """
    specs = []
    for i in range(rows):
        auxi = []
        for j in range(cols):
            if i*cols + j <= n:
                auxi.append({})
            else:
                auxi.append(None)
        specs.append(auxi)
    return specs

def hist_matrix(df : pd.DataFrame, columns : list = None, rows : int = None, cols : int = None) -> None:
    """Makes a matrix of histograms for each column of a pd.DataFrame

    Args:
        df (pd.DataFrame): Data to plot
        columns (list, optional): Columns to include in the matrix. Defaults to None.
        rows (int, optional): Number of rows for the matrix. Defaults to None.
        cols (int, optional): Number of columns for the matrix. Defaults to None.
    """
    if columns == None:
        columns = df.columns
    
    n = len(columns)

    if rows == None:
        rows = int(n**0.5)
    if cols == None:
        cols = int(n/rows + 0.99)
    
    if rows*cols < n:
        cols = int(n/rows + 0.99)

    specs = make_specs(rows, cols, n)
    fig1 = make_subplots(rows = rows, cols = cols,
                        specs= specs, subplot_titles= columns)

    for i, col in enumerate(columns):
        row = i//cols +1
        colum = i%cols + 1
        fig1.add_trace(go.Histogram(x=df[col], name=col) , row=row, col=colum)

    fig1.update_layout(title_text='Histogramas', showlegend=False)
    return fig1

def others(df1, col):
    df1 = df1.copy()

    freq = (df1[col].value_counts(True) < 0.05)
    if sum(freq)==1:
        return df1
    df1[col] = df1[col].apply(lambda x: x if not freq[x] else 'Otros')
    return df1

df = pd.read_csv('Visualización/Streamlit/Dashboard_streamlit/data/anime_final.csv')
# print(df)
cont_vars = [x for x in df.columns if (df[x].dtype == 'float64' or df[x].dtype == 'int64') and x!='anime_id']
disc_vars = [x for x in df.columns if x not in cont_vars]
cat_vars = [x for x in disc_vars if df[x].nunique() < 20]


st.write('# Distribuciones')

col1, col2 = st.columns([0.4,0.6])

with col1:
    st.write('## Discretas')
    for col in cat_vars:
        fig = px.pie(others(df, col), names=col, values='anime_id', title=col)
        fig.update_layout(width=800, height=400)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')

with col2:
    st.write('## Continuas')
    st.plotly_chart(hist_matrix(df, cont_vars), use_container_width=True, theme='streamlit')