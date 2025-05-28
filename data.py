import pandas as pd
import requests

def buscar_dados_historicos(opcoes, selecionadas):
    df_total = pd.DataFrame()
    for nome in selecionadas:
        id_crypto = opcoes[nome]
        url = f"https://api.coingecko.com/api/v3/coins/{id_crypto}/market_chart?vs_currency=usd&days=30"
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json().get("prices", [])
            if data:
                df = pd.DataFrame(data, columns=["timestamp", "price"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
                df["moeda"] = nome
                df_total = pd.concat([df_total, df], ignore_index=True)
    return df_total
