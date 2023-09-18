import streamlit as st
from joblib import load
import pandas as pd

st.set_page_config(
    layout = 'wide',
    page_title = 'predicao-churn-novexus',
    page_icon=':chart_with_downwards_trend:'
    )

st.title('PREDIÇÃO DE CHURN - NOVEXUS')


