import schedule
import time
from mftool import Mftool
import datetime
import pandas as pd
import os
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import requests
import json

mf = Mftool()

# Create a dictionary of all funds to track
amfi_codes = {
    'Aditya Birla Sun Life Tax Relief 96': '119544',
    'Axis Long Term Equity': '120503',
    'Axis Midcap': '120505',
    'HDFC Small Cap': '130503',
    'ICICI Prudential Equity & Debt': '120251',
    'ICICI Prudential Technology': '120594',
    'Nippon India Gold Savings': '118663',
    'Nippon India Large Cap': '118632',
    'Tata Digital India': '135800',
    'UTI Nifty': '120716'
}


# Get current year and make list of years from 2015 to current year
c_year = int(datetime.datetime.now().year)
years = range(2015, c_year + 1)

@st.cache
def refresh_data():
    '''
    Get updated data from AMFI website
    '''
    if not os.path.exists('data'):
        os.mkdir('data')

    # Loop over all funds, get their nav data and save it as csv
    for fund_name, code in amfi_codes.items():
        get_fund_data(fund_name, code)


def get_fund_data(fund_name, code):
    '''
    Get nav date for given fund for all years
    '''
    if not os.path.exists('data/' + fund_name):
        os.mkdir('data/' + fund_name)

    # Loop over all years and get their nav data
    for year in years:
        values = mf.get_scheme_historical_nav_year(code, year)['data']
        df = pd.DataFrame(values[::-1])
        save_fund_data_to_csv(fund_name, year, df)


def save_fund_data_to_csv(fund_name, year, df):
    '''
    Save dataframe to csv
    '''
    df.to_csv('data/' + fund_name + '/' +
              fund_name + '_' + str(year), index=None)


def display_6mma_12_mma_buy_sell_decision(fund_name, df_list):
    '''
    Plot moving average for 6 and 12 months
    '''
    final_df = pd.concat(df_list, axis=0, ignore_index=True)
    final_df['date'] = pd.to_datetime(final_df['date'], dayfirst=True)
    final_df = final_df.resample('M', on='date').mean()
    final_df['SMA_6'] = final_df.iloc[:, 0].rolling(window=6).mean()
    final_df['SMA_12'] = final_df.iloc[:, 0].rolling(window=12).mean()
    max_nav = max(final_df.iloc[:, 0])
    final_df['buy_sell_signal'] = (final_df['SMA_6'] > final_df['SMA_12']).map({True: max_nav, False: 0})
    fig = px.line(final_df, x=final_df.index, y=['nav', 'SMA_6', 'SMA_12', 'buy_sell_signal'], color_discrete_map = {'buy_sell_signal': 'black'})
    fig.update_layout(
        title={
            'text': fund_name,
            'y':0.92,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Year",
        yaxis_title="Value",
        height=700,
        legend=dict(
            x=0.5,
            y=-0.35,
            bordercolor="Black",
            borderwidth=1
        ),
        margin=dict(
            l=0,
            r=0,
            t=70,
            b=0,
            pad=0
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write('When black line is highest, the signal is BUY. When the black line is 0, the signal is SELL.')
    
    st.header('Current Status:')
    st.subheader('NAV:' + str(round(final_df.loc[final_df.index[-1], 'nav'], 4)))
    st.subheader('SMA 6 Months:' + str(round(final_df.loc[final_df.index[-1], 'SMA_6'], 4)))
    st.subheader('SMA 12 Months:' + str(round(final_df.loc[final_df.index[-1], 'SMA_12'], 4)))
    st.subheader('Signal: ' +("BUY :arrow_up:" if final_df.loc[final_df.index[-1], 'SMA_6'] > final_df.loc[final_df.index[-1], 'SMA_12'] else "SELL :arrow_down:"))
    st.text('Last updated: ' + str(final_df.index[-1].strftime("%d/%m/%Y")))

def read_fund_data(fund_name):
    '''
    Read csv file and show graph as well as buy-sell decisions
    '''
    df_list = []
    # Loop over all years
    for year in years:
        df = pd.read_csv('data/' + fund_name + '/' + fund_name + '_' + str(year), index_col=None)
        df_list.append(df)
    display_6mma_12_mma_buy_sell_decision(fund_name, df_list)

def checkValidAmfiCode(amfi_code_input):
    '''
    If AMFI code is valid, download nav data for provided it and show graph and buy-sell decision
    '''
    response_text = requests.get('https://raw.githubusercontent.com/NayakwadiS/mftool/master/Scheme_codes.txt').text
    all_amfi_codes_dict = eval(response_text)
    if(amfi_code_input in all_amfi_codes_dict.keys()):
        st.write('Loading data. Please wait...')
        get_fund_data(all_amfi_codes_dict[amfi_code_input], amfi_code_input)
        st.write('Data refresh complete!!!')
        st.write('INFO: Delete AMFI code to populate data from the Mutual Fund dropdown.')
        read_fund_data(all_amfi_codes_dict[amfi_code_input])
    else:
        st.write('Invalid AMFI code. Please enter a valid AMFI code from the link below.')
        st.write('Delete AMFI code to populate data from the Mutual Fund dropdown.')


# Run refresh everyday at 9.30am
schedule.every().day.at("09:30").do(refresh_data)
# while True:
#     schedule.run_pending()

def main():
    # Steamlit Config
    if st.checkbox('Dark Mode'):
        st.markdown('''<style>
            body, .stCheckbox, .Widget > label >div, label {
                color: #fff !important;
                background-color: #000 !important;
            }
            </style>''', unsafe_allow_html=True)

    st.title("Mutual Funds Moving Average Webapp")
    st.subheader('View 6 Month and 12 Month Simple Moving Average for Mutual Funds')
    st.write('Disclaimer: This webapp is made for knowledge purposes only and should not be considered as investment advice. Please perform your own research before making any decisions.')
    option = st.selectbox('Select Mutual Fund', list(amfi_codes.keys()))
    st.write('OR')
    amfi_code_input = st.text_input(label='Enter AMFI code')
    st.markdown('[View list of AMFI codes](https://raw.githubusercontent.com/NayakwadiS/mftool/master/Scheme_codes.txt)')
    if(amfi_code_input):
        checkValidAmfiCode(amfi_code_input)
    else:
        read_fund_data(option)

if __name__=='__main__':
    main()