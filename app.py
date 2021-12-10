import krakenex
from pykrakenapi import KrakenAPI
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from plotly.subplots import make_subplots
from datetime import timedelta, date
import math
import time

# Abriendo la API de Krakenex
api = krakenex.API()
k = KrakenAPI(api)

data = k.get_asset_info()

# Creando Funciones


def pairs(df, cripto_seleccionada): #Esta función devuelve los pares disponibles para la cripto seleccionada
    coin = []
    df1 = [i.split('/')[0] for i in df]
    df2 = [i.split('/')[1] for i in df]
    for i in range(len(df)):
        if df1[i] == cripto_seleccionada:
            coin.append(df2[i])
    return coin


def unix_date(fecha): #Esta función cambia el formato de la fecha que da streamlit al solicitado por la API
    unix = time.mktime(fecha.timetuple())
    return unix


def fecha_minima(intervalo_elegido): #Esta función da como resultado la fecha mínima de la cual debiesen de haber datos en la API, el problema es que hay monedas más jóvenes que los intervalos de tiempo
    c= date.today() - timedelta(days=math.ceil(int(intervalo_elegido)*720/1440))
    return c


def fun(cripto, moneda, periodo, fecha_desde= 0, vwap_calc= 5): #función que devuelve los gráficos de los pares solicitados de monedas y que utiliza cada una de las variables que solicita la API
    par_solicitado = cripto + moneda
    fecha_unix = unix_date(fecha_desde)
    df, last = k.get_ohlc_data(par_solicitado, interval=periodo, since=fecha_unix, ascending=True)
    df.head()
    pv_fun = lambda a, b, c, d, e: (a + b + c + d) * e / 4
    df["pv"] = pv_fun(df["open"], df["high"], df["low"], df["close"], df["volume"])

    df["vwap_calc"] = df.pv.rolling(window=vwap_calc, min_periods=1).sum() / df.volume.rolling(window=vwap_calc, min_periods=1).sum()

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, subplot_titles=('OHLC', 'Volume'),
                        row_width=[0.2, 0.7])
    fig.add_trace(go.Candlestick(x=df.index,
                                         open=df['open'],
                                         high=df['high'],
                                         low=df['low'],
                                         close=df['close'],
                                         name="OHLC"),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=df.index, y=df["vwap_calc"], name="VWAP", line=dict(color='purple', width=1)), row=1, col=1)

    fig.add_trace(go.Bar(x=df.index, y=df['volume'], showlegend=False), row=2, col=1)
    fig.update_xaxes(
        title_text='Date',
        rangeslider_visible=True)
    fig.update_layout(xaxis_rangeslider_visible=False,
        title={
            'text': 'Pair ' + cripto + ' ' + moneda,
            'y': 0.95,
            'x': 0.43,
            'xanchor': 'center',
            'yanchor': 'top'
        }
    )

    return df, fig


def warning(cripto, data, vwap_req, fecha_minima_requerida): #comentarios en la aplicación
    if 0 in data["volume"].to_list():
        a = st.warning(
        "In some time periods there were none transactions for the pair " + criptomoneda + monedita + ". Please select a wider interval so the Canddlesticks chart can be improved.")
        return a
    elif data.index.min() >= fecha_minima_requerida + timedelta(days=16):
        b = st.warning("Unfortunately in Kraken there are only records of transactions for the pair " + criptomoneda + monedita + " since " + str(data.index.min()) + " . Please select this or a higher initial date.")
        return b
    elif cripto[0] == "X":
        c = st.info(
            'Did you know that any asset that acts as a “supranational” currency that isn’t bound to any particular country borders begins with the letter X? Such as XAU in gold and XBT in Bitcoin markets.')
        return c
    elif len(data.volume) < vwap_req:
        d = st.warning("There are not enough canddlesticks for this time period, therefore the VWAP can't be calculated as requested. Please select a different time interval or another lenght for the VWAP.")
        return d
    else:
        d = ""
        return d


# Trabajo con Streamlit y el modelamiento de la página web
st.set_page_config(layout="wide")
st.title("Criptocurrencies from Kraken API")

# Obtengo todos los nombres de las criptos que ofrece la API para que sean seleccionados con su par respectivo y el índice propuesto para la eplicación
pairs_info = k.get_tradable_asset_pairs()
pairs_names = list(pairs_info['wsname'])

nom_cripto = np.unique([i.split('/')[0] for i in pairs_names]).tolist()
default_ix = nom_cripto.index("XBT")

# Obtengo el par disponible para la cripto seleccionada en la primera y segunda selectbox
criptomoneda = st.sidebar.selectbox(
    "Currency", nom_cripto, index=default_ix
)

lista_monedas_disponibles = pairs(pairs_names, criptomoneda)
default_ix_2 = lista_monedas_disponibles.index("USD")

monedita = st.sidebar.selectbox(
    "Desired Pair", lista_monedas_disponibles, index=default_ix_2
)

# Tercera selectbox: intervalo de tiempo entre cada Candlestick
intervalo_tiempo_sel = st.sidebar.selectbox(
    "Time Interval between each Candlestick", ["1 Minute", "5 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "4 Hours", "1 Day", "7 Days", "15 Days"]
)
diccionario = {"1": "1 Minute", "5": "5 Minutes", "15": "15 Minutes", "30": "30 Minutes", "60": "1 Hour", "240": "4 Hours", "1440": "1 Day", "10080": "7 Days", "21600": "15 Days"}
intervalo_tiempo = list(diccionario.keys())[list(diccionario.values()).index(intervalo_tiempo_sel)]

#Intervalo de tiempo para calcular el VWAP
vwap_pedido = st.sidebar.slider("Amount of Candlesticks for which the VWAP is calculated", 1, 15)

#Fecha desde la cual se quieren ver los datos
fecha_min = fecha_minima(intervalo_tiempo)
fecha_pedida = st.sidebar.date_input("Initial date", value=fecha_min, min_value=fecha_min, max_value=date.today(), key=None)

#Llamo a la función con los datos pedidos en la página web
datos, grafico = fun(criptomoneda, monedita, intervalo_tiempo, fecha_pedida, vwap_calc=vwap_pedido)

#Agrego algunos datos interesantes de los datos obtenidos
col1, col2, col3 = st.columns(3)
with col1: st.metric(label="Max price " + criptomoneda + monedita + " was sold vs its Min", value=datos.high.max(), delta=round(datos.high.max() - datos.low.min(), 3))
with col2: st.metric(label="Last " + criptomoneda + monedita + " price vs last VWAP", value=datos.close[-1], delta=round(datos.close[-1] - datos.vwap_calc[-1], 3))
with col3: warning(criptomoneda, datos, vwap_pedido, fecha_pedida)

#Grafico el OHLC, el VWAP y el Volumen
st.plotly_chart(grafico, use_container_width=True, sharing="streamlit")

#Créditos
st.markdown("By _Tomás Rodríguez Hermosilla_")
