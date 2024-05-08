import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
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
    fig1.show()

st.write('# Distribuciones')

df = pd.read_csv('./data/anime_final.csv')
cont_vars = [x for x in df.columns if df[x].dtype == 'float64' or df[x].dtype == 'int64']
disc_vars = [x for x in df.columns if x not in cont_vars]
cat_vars = [x for x in disc_vars if df[x].nunique() < 20]

st.plotly_chart(hist_matrix(df, cont_vars))
