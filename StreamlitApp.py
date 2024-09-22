# streamlit run "C:\Users\Utilisateur\Desktop\_Betting2024\Codes\tennis\StreamlitApp.py"

import streamlit as st
import os
# import time
# import re
# import requests
# import lxml
# import sys
# import json
import pandas as pd
# import ast
# import datetime
# import matplotlib.pyplot as plt

#print(os.getcwd())

################### 0 - Initialization ###################
# 0 - Load files
# df = pd.read_csv(r"C:\Users\Utilisateur\Desktop\_Betting2024\Codes\tennis\Data\backtest_KNN25_250_fav0.62.csv", sep = ';')
df = pd.read_csv("./Data/backtest_KNN25_250_fav0.62.csv", sep = ';')
df['PnL'] = df['PL_favoriteBetModel']
df = df[["('Date', 'Date')", "('Other', 'tournament-name')", "('Player', 'p1')", "('Player', 'p2')","('Other', 'maxOdds_1')","('Other', 'maxOdds_2')", 'modelProba1', 'modelProba2', "('modelPred', '')", 'valueBetModel', 'PnL']]
df.columns = ["Date", "Tournament", "P1", "P2","maxOdds_1","maxOdds_2", 'modelProba1', 'modelProba2', "modelPred", 'valueBetModel', 'PnL']
df['PnL strategy'] = df['PnL'].cumsum()
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

# plt.plot(pd.to_datetime(df['Date']), df['PL_favoriteBetModel'].cumsum())
# plt.tight_layout()
# plt.show()

################### 0 - Create dashboard with Streamlit ###################
# 0 - Formatting
st.title('Quant Betting 2024')

# I - Allow for downloading full file
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")
csv = convert_df(df)
st.download_button(label = 'Download full file', data = csv)

# II - Show last 20 matches
st.subheader('Last 20 games')
st.write(df.tail(20))

# III - Show PnL since inception with a few figures
st.subheader('PnL since inception')

# Display recap stats
roi = df['PnL'].mean()
nMatches= df.shape[0]
sharpe = df['PnL'].mean() / df['PnL'].std()
hitRate = (df['PnL']>0).mean()

recap = pd.DataFrame([nMatches, roi, sharpe, hitRate], index = ["nMatches", "roi", "sharpe", "hitRate"], columns = ['Stats Strategy']).T
st.write(recap)

st.line_chart(df, y = 'PnL strategy', x_label = 'Date', y_label = 'PnL strategy', color = '#476930')
