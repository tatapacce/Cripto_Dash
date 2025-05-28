import time
import streamlit as st
st.set_page_config(page_title="Dashboard Criptomoedas", layout="wide")
import pandas as pd
import requests

from layout import (aplicar_estilo_personalizado, 
    configurar_interface, 
    mostrar_precos_atuais, 
    mostrar_grafico, 
    mostrar_candlestick)

@st.cache_data(ttl=300)
def obter_dados_historicos(id_crypto, dias):
    url = f"https://api.coingecko.com/api/v3/coins/{id_crypto}/market_chart?vs_currency=usd&days={dias}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json().get("prices", [])
    elif r.status_code == 429:
        raise ValueError("Limite de requisições excedido.")
    else:
        r.raise_for_status()

aplicar_estilo_personalizado()

st.title("🪙 Dashboard de Criptomoedas")
st.markdown("Compare preços, veja gráficos e acompanhe tendências das moedas digitais.")

opcoes = {"Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Cardano": "cardano",
    "Solana": "solana",
    "XRP": "ripple",
    "Dogecoin": "dogecoin",
    "Dash": "dash"}

selecionadas, periodo = configurar_interface(opcoes)

mostrar_precos_atuais(opcoes, selecionadas)

df_total = pd.DataFrame()

with st.spinner("⏳ Carregando dados históricos..."):
    for nome in selecionadas:
        id_crypto = opcoes.get(nome)
        try:
            data = obter_dados_historicos(id_crypto, periodo)
            if data:
                df = pd.DataFrame(data, columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df["moeda"] = nome
                df_total = pd.concat([df_total, df], ignore_index=True)
            else:
                st.warning(f"⚠️ Nenhum dado de preço recebido para {nome}.")
        except ValueError:
            st.warning(f"⚠️ Limite de requisições excedido para {nome}. Aguarde um pouco.")
        except Exception as e:
            st.error(f"❌ Erro ao buscar dados de {nome}: {e}")

if df_total.empty:
    st.warning("⚠️ Nenhum dado foi carregado.")
    st.stop()

mostrar_grafico(df_total)

if len(selecionadas) == 1:
    mostrar_candlestick(opcoes[selecionadas[0]], selecionadas[0], periodo)
