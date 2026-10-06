"""
Front end (Streamlit) baseado no main.py de consulta de cotações.

Como rodar (no terminal, com o .venv ativo):
    pip install streamlit requests
    streamlit run front.py
"""
import requests
import streamlit as st

st.set_page_config(page_title="Cotação de moedas", page_icon="💱", layout="centered")

# Mesmas moedas e mesmo texto de menu do main.py
MOEDAS = {
    "USD-BRL": "Dólar Americano",
    "EUR-BRL": "Euro",
    "GBP-BRL": "Libra Esterlina",
    "ARS-BRL": "Peso Argentino",
    "BTC-BRL": "Bitcoin",
    "ETH-BRL": "Ethereum",
}
OUTRA = "Outra (digitar o par)"

menu_moedas = """
=== Opções de Moedas para Consulta ===

Tradicionais:

USD-BRL (Dólar Americano)
EUR-BRL (Euro)
GBP-BRL (Libra Esterlina)
ARS-BRL (Peso Argentino)

Criptomoedas:

BTC-BRL (Bitcoin)
ETH-BRL (Ethereum)

=====================================
"""


def consultar_moeda(moeda):
    """Mesma lógica do main.py, mas devolve (dados, erro) em vez de usar print."""
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    try:
        resposta = requests.get(url, timeout=10)
    except requests.exceptions.RequestException:
        return None, "Não foi possível conectar à API. Verifique sua internet."

    if resposta.status_code == 200:
        return resposta.json(), None

    elif resposta.status_code == 404:
        resposta_erro = resposta.json()
        codigo = resposta_erro.get("code", "404")
        mensagem = resposta_erro.get("message", "Moeda não encontrada")
        return None, f"Código do erro: {codigo} | Motivo do erro: {mensagem}"

    else:
        return None, f"Erro! (HTTP {resposta.status_code})"


def formatar_valor(valor):
    """Formato brasileiro. Valores abaixo de 1 (ex.: peso argentino) usam 4 casas."""
    numero = float(valor)
    casas = 4 if abs(numero) < 1 else 2
    texto = f"{numero:,.{casas}f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------- Interface
st.title("Cotação de moedas")
st.caption("Consulte o valor atual de moedas e criptomoedas.")

with st.expander("Ver opções de moedas para consulta"):
    st.code(menu_moedas, language=None)

opcoes = [f"{par} ({nome})" for par, nome in MOEDAS.items()] + [OUTRA]
escolha = st.selectbox("Moeda", opcoes)

if escolha == OUTRA:
    moeda_desejada = st.text_input("Digite a moeda que deseja consultar (ex: USD-BRL)").strip().upper()
else:
    moeda_desejada = escolha.split(" ")[0]

if st.button("Consultar cotação", type="primary", use_container_width=True):
    if not moeda_desejada:
        st.warning("Digite a moeda, por exemplo USD-BRL.")
    else:
        with st.spinner("Consultando..."):
            dados_api, erro = consultar_moeda(moeda_desejada)

        if dados_api:
            # A API devolve a chave sem hífen: "USD-BRL" vira "USDBRL"
            chave = moeda_desejada.replace("-", "")
            item = dados_api.get(chave) or next(iter(dados_api.values()))
            simbolo = "R$" if item["codein"] == "BRL" else item["codein"]
            variacao = float(item["pctChange"])

            st.success("Requisição bem-sucedida!")
            st.write(f"O valor atual de **{moeda_desejada}** é:")
            st.metric(
                label=item["name"],
                value=f"{simbolo} {formatar_valor(item['bid'])}",
                delta=f"{variacao:+.2f}%".replace(".", ","),
            )

            c1, c2, c3 = st.columns(3)
            c1.metric("Venda", f"{simbolo} {formatar_valor(item['ask'])}")
            c2.metric("Máxima do dia", f"{simbolo} {formatar_valor(item['high'])}")
            c3.metric("Mínima do dia", f"{simbolo} {formatar_valor(item['low'])}")
            st.caption(f"Atualizado em {item['create_date']}")
        else:
            st.error(f"Erro ao consultar a moeda: {moeda_desejada}")
            st.caption(erro)