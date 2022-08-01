#===Importing the Packges
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from finta import TA
from streamlit_option_menu import option_menu
import datetime
# import pmdarima as pm

@st.cache
def get_data(stock, date1, date2):
    data = yf.download(str(stock), start=date1, end=date2)
    return data

@st.cache
def fun_strategy1(data, ind1, ind2):
    entrada = []
    idx_ent = []
    for i, (id1, id2) in enumerate(zip(ind1, ind2)):
        if id1 > id2:
            auxiliar = pd.Series([data[i]], index=[data.index[i]])
            entrada.append(data[i])
            idx_ent.append(data.index[i])
    return idx_ent, entrada

def About(conteiner):
    with conteiner:
        st.title('App Trade Stategy')
        st.text('by Sandro Marcos de Gouveia')
        st.text('- - - - - - - - - - - - - - - - - ')
        st.text('In order to understand how these indicators works, please check the following link:\n'
                'https://www.investopedia.com/ask/answers/122414/what-are-most-common-periods-used-creating-moving-average-ma-lines.asp')

# def LoadDdata(conteiner):
#     with conteiner:
#         st.title('Load your Stock Data')
#         st.text('Define your Stock')
#
#         today = datetime.date.today()
#         tomorrow = today - datetime.timedelta(days=500)
#         start_date = st.date_input('Start date', tomorrow)
#         end_date = st.date_input('End date', today)
#
#
#         stock = st.selectbox('Select the Stock to study', ('AAPL', 'GOOG', 'AMZN', 'MSFT'))
#
#         st.title('Plot your Stock')
#         OHLC = st.selectbox('Select Open, High, Low or Close', ('Open', 'High', 'Low', 'Close'))
#         ques = st.radio("Do you table or graph?", ('Graph', 'Table'))
#
#         data = get_data(stock, start_date, end_date)
#         if ques == 'Table':
#             st.dataframe(data)
#             dados = data[OHLC]
#         else:
#             dados = data[OHLC]
#             # st.line_chart(dados)
#             fig = plt.figure(figsize=[10, 5])
#             ax = fig.add_subplot()
#             ax.grid()
#             ax.plot(dados, c='b', lw=1, label=OHLC)
#             ax.legend(loc='best')
#             ax.tick_params(axis='x', labelrotation=45)
#             fig.tight_layout()
#             st.pyplot(fig=fig)

def PlotData(conteiner, data, OHLC):
    with conteiner:
        st.title('Your Stock ')
        st.text('The historical behaviour of your stock')

        dados = data[OHLC]
        # st.line_chart(dados)
        fig = plt.figure(figsize=[10, 4])
        ax = fig.add_subplot()
        ax.grid()
        ax.plot(dados, c='b', lw=1, label=OHLC)#========================================================================
        ax.legend(loc='best')
        ax.tick_params(axis='x', labelrotation=45)
        fig.tight_layout()
        st.pyplot(fig=fig)

        st.title('EDA')
        st.text('Exploratory Data Analysis - Must be improved')

        st.text('First discrete difference')
        _o = data['Open'].diff(1)
        _h = data['High'].diff(1)
        _l = data['Low'].diff(1)
        _c = data['Close'].diff(1)

        fig = plt.figure(figsize=[10, 5])
        for ct, (i, j) in enumerate(zip(['Open', 'High', 'Low', 'Close'], [_o, _h, _l, _c])):
            ax1 = fig.add_subplot(2, 2, ct+1)
            ax1.set_title(i)
            ax1.grid()
            ax1.hist(j, 50, density=1, color='green', alpha=0.7, ec='k')
        fig.tight_layout()
        st.pyplot(fig=fig)


#===Defyning the 'conteiner' in streamlit way...
ctAbout = st.container()
ctPlot  = st.container()
ctLoadData = st.container()
ctAppStra = st.container()
ctERROR = st.container()
ctEDA = st.container()

#====Begin....
with st.sidebar:
    About(ctAbout)
    st.title('Stock')
    stock = st.selectbox('Stock:', ('AAPL', 'GOOG', 'AMZN', 'MSFT', 'TSLA', 'NVDA', 'JPM', 'USER*'))
    if stock == 'USER*':
        stock = st.text_input('Define a stock', 'AAPL')

    today = datetime.date.today()
    tomorrow = today - datetime.timedelta(days=1000)

    start_date = st.date_input('Start date', tomorrow)
    end_date = st.date_input('End date', today)

    st.title('Plot your Stock')
    OHLC = st.selectbox('Select Open, High, Low or Close', ('Open', 'High', 'Low', 'Close'))
    data = get_data(stock, start_date, end_date)


    st.title('Define your Indicator')
    indicador1 = st.selectbox('Select the Indicator #1', ('SMA', 'EMA', 'DEMA'))
    per1 = st.slider("Please enter ind#1 periods", 2, 150, 1)
    indicador2 = st.selectbox('Select the Indicator #2', ('SMA', 'EMA', 'DEMA'))
    per2 = st.slider("Please enter ind#2 periods", 2, 150, 1)

    # st.title('Forecast')
    # n_ahead = st.slider("Please, select the days ahead", 2, 500, 1)
    # ahead = today + datetime.timedelta(days=n_ahead-1)
    # data_afrente = pd.date_range(today, ahead, freq='d')

with ctAppStra:
    PlotData(ctPlot, data, OHLC)
    st.title('Test your Strategy')
    st.text('The strategy: When the indicator#1 is above the indicator#2,\nit is an entry sign represented by the green triangule(^)')
    data = data

    if indicador1 == 'SMA':
        data_ind1 = TA.SMA(data, per1)
    elif indicador1 == 'EMA':
        data_ind1 = TA.EMA(data, per1)
    else:
        data_ind1 = TA.DEMA(data, per1)

    if indicador1 == 'SMA':
        data_ind2 = TA.SMA(data, per2)
    elif indicador2 == 'EMA':
        data_ind2 = TA.EMA(data, per2)
    else:
        data_ind2 = TA.DEMA(data, per2)

    idx_ent, entrada = fun_strategy1(data[OHLC], data_ind1, data_ind2)

    fig = plt.figure(figsize=[10, 5])
    ax = fig.add_subplot()
    ax.grid()
    ax.plot(data[OHLC], c='b', lw=1, label='data')#===================================================================
    ax.scatter(idx_ent, entrada, marker='^', c='g', label='entry', s=25)
    ax.plot(data_ind1, ls='-', c='r', lw=0.75, label='Ind#1')#========================================================
    ax.plot(data_ind2, ls='-', c='g', lw=0.75, label='Ind#2')#========================================================
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend(loc='best')
    fig.tight_layout()
    st.pyplot(fig=fig)


#     # st.title('Time-Series Forecast')
#     # st.text('Forecast your stock using ARIMA approach - Must be improved')
#     # treino = data[OHLC]
#     # modl = pm.auto_arima(treino, start_p=1, start_q=1, start_P=1, start_Q=1,
#     #                      max_p=5, max_q=10, max_P=10, max_Q=10, seasonal=True,
#     #                      stepwise=True, suppress_warnings=True, D=20, max_D=20,
#     #                      error_action='ignore')
#     #
#     # preds, conf_int = modl.predict(n_periods=n_ahead, return_conf_int=True)
#     #
#     # fig = plt.figure(figsize=[8, 2])
#     # ax = fig.add_subplot()
#     # ax.grid()
#     # ax.plot(treino, alpha=0.75, c='b', label='Real')
#     # ax.plot(data_afrente, preds, alpha=0.75, c='r', label='Predict')
#     # plt.fill_between(data_afrente, conf_int[:, 0], conf_int[:, 1], alpha=0.1, color='b')
#     # ax.legend(loc='best')
#     # fig.tight_layout()
#     # st.pyplot(fig=fig)






