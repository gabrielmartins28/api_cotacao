import requests


def consultar_moeda(moeda):
    url = f"https://economia.awesomeapi.com.br/json/last/{moeda}"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        print("Deu certo")
        print(resposta.json())
        return resposta.json()

    elif resposta.status_code == 404:
        resposta_erro = resposta.json()

        codigo = resposta_erro['code']
        mensagem = resposta_erro['message']

        print(f"Código do erro: {codigo} ")
        print(f"Motivo do erro: {mensagem}")

        return resposta.json()
    else:
        print("Erro!")

moeda_desejada = input("\nDigite a moeda que deseja consultar(ex: USD-BRL):")

dados_api = consultar_moeda(moeda_desejada)
        
if dados_api:

    
    valor = moeda_desejada["bid"]
    print("\nRequisição bem-sucedida!")

    print(f"O valor atual de {moeda_desejada} é: ")
    print(f"R$ {float(valor):.2f}")

else:
    print(f"\nErro ao consultar a moeda: {moeda_desejada}")

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

