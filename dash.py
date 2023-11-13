import requests
import pandas as pd
import streamlit as st
import datetime 
import plotly.express as px
import numpy as np

data_hora_atual = datetime.datetime.now()
mes_atual = data_hora_atual.month

st.set_page_config(
    page_title="Estação Meteorológica",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded",
)

def get_data_from_thingspeak(channel_id, read_key):
    endpoint = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
    params = {
        "api_key": read_key,
        "start": '2023-'+str(mes_atual)+'-01T00:00:00Z' 
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

data = get_data_from_thingspeak('2302302', 'A5W7L8EBQ74NJ3YH')

df = pd.DataFrame(data['feeds'])

last_entry = df["created_at"].iloc[-1]
last_temperatura = df["field1"].iloc[-1]
last_umidade = df["field2"].iloc[-1]
last_pressao = df["field3"].iloc[-1]

divisao0 = df["created_at"].str.split("T")

data = divisao0.str.get(0)
df["Data"] = data
df["Data"] = pd.to_datetime(df["Data"])

horario_utc = divisao0.str.get(1)
df["Horario UTC"] = horario_utc
divisao1 = df["Horario UTC"].str.split(":")
hora = divisao1.str.get(0)
minuto = divisao1.str.get(1)

horario = hora+":"+minuto

df["Horario"] = horario

df["Temperatura"] = df["field1"]
df["Umidade"] = df["field2"]
df["Pressao Atmosferica"] = df["field3"]

df = df.drop("entry_id", axis=1)

df["Day"] = df["Data"].apply(lambda x: str(x.year)+"/"+str(x.month)+"/"+str(x.day))
day = st.sidebar.selectbox("Selecione o dia", df["Day"].unique())

df_filtered = df[df["Day"] == day]

st.title("Última Leitura")
st.write(last_entry )

st.write("Temperatura: ", last_temperatura, "ºC")
st.write("Umidade: ", last_umidade, "%")
st.write("Pressão Atmosférica: ", last_pressao, "hPa")

st.title("Mês Atual")
st.write(df_filtered)

col1, = st.columns(1)
col2, = st.columns(1) 
col3, = st.columns(1)


fig_temperatura_dia = px.line(df_filtered, x="Horario", y="Temperatura", title="Gráfico de Temperatura por Dia")
col1.plotly_chart(fig_temperatura_dia, use_container_width=True)

fig_umidade_dia = px.line(df_filtered, x="Horario", y="Umidade", title="Gráfico de Umidade do Ar por Dia")
col2.plotly_chart(fig_umidade_dia, use_container_width=True)

fig_pressao_dia = px.line(df_filtered, x="Horario", y="Pressao Atmosferica", title="Gráfico de Pressão Atmosférioca por Dia")
col3.plotly_chart(fig_pressao_dia, use_container_width=True)

