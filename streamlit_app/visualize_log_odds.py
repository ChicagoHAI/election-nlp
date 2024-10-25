import streamlit as st
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px

@st.cache_data
def load_data():
    log_odds_dir = '../results/log_odds/platforms/ngram_2/stopwords_english'
    df = pd.read_csv(os.path.join(log_odds_dir,'democrat_2024_republican_2024.csv'))
    return df

def df_filter(df,corpus1_name,corpus2_name):
    sel_slider = st.slider(f"{corpus1_name} Word Count Range",max_value=df['count 1'].max())
    df = df[df['count 1'] >= sel_slider]
    sel_slider = st.slider(f"{corpus2_name} Minimum Word Count",max_value=df['count 2'].max())
    df = df[df['count 2'] >= sel_slider]
    df['abs_log_odds'] = df['log_odds'].abs()
    sel_slider = st.slider("Log-Odds Range (Magnitude)",
                           value=(0.0, df['abs_log_odds'].max()))
    df = df[df['abs_log_odds'].between(*sel_slider, inclusive='both')]
    return df

    


st.title('Log-Odds Analysis of 2024 Party Platforms')

df = load_data()
df['total_count'] = df['count 1'] + df['count 2']
# rename count columns based on the value of "corpus 1" and "corpus 2"
df = df_filter(df,"Democratic Party 2024","Republican Party 2024")


# Create a scatterplot with interactive tooltips
fig = px.scatter(df, x='total_count', y='log_odds', #text='term', 
                color='log_odds', width=800, height=800,
                color_continuous_scale=px.colors.diverging.RdYlBu,
                opacity=1, color_continuous_midpoint=0,range_color=[-4,4],
                hover_name='term', log_x=True, log_y=False,
                hover_data={'log_odds': ':.2f',
                            'total_count': False,
                            'term': False,
                            }
                )
fig.update_traces(marker=dict(size=10))  # Set all points to size 10

fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
    ),
)

st.plotly_chart(fig)