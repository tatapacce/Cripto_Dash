import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

def aplicar_estilo_personalizado():
    st.session_state["plotly_tema"] = "plotly_white"
    st.markdown("""<style>
        body { background-color: #f0f2f6; color: #000000;}
        .stApp {background: linear-gradient(to bottom, #8224e3, #e242e5, #f0f2f6);
            background-attachment: fixed;}
        h1, h2, h3, h4 {color: #003366;}
        .stMultiSelect, .stMetric 
                {background-color: #1f4c2f;
            border-radius: 12px;
            padding: 10px;
            border-color: #FFFFFF;}
        .stMetricValue {
            font-weight: bold;}
        </style>""", unsafe_allow_html=True)

def configurar_interface(opcoes):
    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("⚙️ Configurações")
        selecionadas = st.multiselect(
            "Escolha as criptomoedas:",
            options=list(opcoes.keys()),
            default=["Bitcoin"])
        if not selecionadas:
            st.warning("Selecione pelo menos uma criptomoeda.")
            st.stop()

        periodo = st.selectbox("Período para histórico (dias):", [7, 14, 30, 90, 180, 365], index=2)

    with col2:
        st.subheader("📊 Comparativo de Preços")

    st.markdown("---")
    return selecionadas, periodo

def mostrar_precos_atuais(opcoes, selecionadas):
    st.markdown("### 💰 Preços Atuais")
    colunas = st.columns(len(selecionadas))

    for i, nome in enumerate(selecionadas):
        id_crypto = opcoes[nome]
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={id_crypto}&vs_currencies=usd&include_24hr_change=true"

        tentativas = 3
        while tentativas > 0:
            r = requests.get(url)
            if r.status_code == 200:
                dados = r.json()[id_crypto]
                preco = dados["usd"]
                variacao = dados.get("usd_24h_change", 0)
                colunas[i].metric(label=nome,
                    value=f"${preco:,.2f}",
                    delta=f"{variacao:.2f}%" if variacao else None)
                break
            elif r.status_code == 429:
                time.sleep(2) 
                tentativas -= 5
            else:
                colunas[i].error("Erro ao buscar preço.")
                break
        else:
            colunas[i].error("Limite de requisições excedido. Tente mais tarde.")

def mostrar_grafico(df_total):
    st.markdown("### 📈 Histórico de Preços")
    fig = px.line(df_total, x="timestamp", y="price", color="moeda",
                  title="Variação de Preço por Criptomoeda")
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Preço (USD)",
        template=st.session_state["plotly_tema"])
    st.plotly_chart(fig, use_container_width=True)

def mostrar_candlestick(id_crypto, nome, periodo):
    st.markdown(f"### 🕯️ Candlestick: {nome}")
    url = f"https://api.coingecko.com/api/v3/coins/{id_crypto}/ohlc?vs_currency=usd&days={periodo}"
    r = requests.get(url)
    if r.status_code == 200 and r.json():
        data = pd.DataFrame(r.json(), columns=["timestamp", "open", "high", "low", "close"])
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")

        fig = go.Figure(data=[go.Candlestick(
            x=data["timestamp"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            increasing_line_color='lime', 
            decreasing_line_color='red')])
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Preço (USD)",
            template=st.session_state["plotly_tema"])
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Dados de Candlestick indisponíveis para esse período.")
