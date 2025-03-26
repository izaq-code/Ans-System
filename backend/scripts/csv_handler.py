import requests
import os

# URL do arquivo CSV
URL_CSV = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

# Caminho para salvar o arquivo (pasta de destino)
PASTA_ORIGEM = "../../frontend/dataset/"
CAMINHO_ARQUIVO = os.path.join(PASTA_ORIGEM, "operadoras.csv")

# Verificando se o diretório existe, se não, cria
os.makedirs(PASTA_ORIGEM, exist_ok=True)

def baixar_csv():
    # Fazendo o pedido para o arquivo CSV
    response = requests.get(URL_CSV)

    # Verificando se o pedido foi bem-sucedido
    if response.status_code == 200:
        with open(CAMINHO_ARQUIVO, "wb") as file:
            file.write(response.content)
        print(f"Arquivo CSV baixado com sucesso e salvo como {CAMINHO_ARQUIVO}")
    else:
        print(f"Falha no download. Código de status: {response.status_code}")

if __name__ == "__main__":
    baixar_csv()
