import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("Intoxicacion por sustancias psicoactivas")

df = pd.read_csv('static/datasets\intoxicacion_por_sustancias_psicoactivas.csv')

df

