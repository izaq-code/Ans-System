import os
import requests
import zipfile
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import mysql.connector

# URLs para os diretórios 2023 e 2024
URL_2023 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/"
URL_2024 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/"

# Pasta destino onde os arquivos serão salvos
PASTA_DESTINO_2023 = "../../frontend/dataset/demonstracoes_contabeis/2023/"
PASTA_DESTINO_2024 = "../../frontend/dataset/demonstracoes_contabeis/2024/"

# Função para criar diretórios, caso não existam
def criar_pasta(destino):
    os.makedirs(destino, exist_ok=True)

# Função para baixar arquivos de um diretório
def baixar_arquivos_do_diretorio(url, pasta_destino):
    criar_pasta(pasta_destino)
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        
        for link in links:
            arquivo_url = urljoin(url, link['href'])
            
            # Filtra para garantir que os arquivos CSV e ZIP sejam baixados
            if arquivo_url.endswith(".zip"):
                nome_arquivo = os.path.join(pasta_destino, link['href'])
                
                # Baixa o arquivo ZIP e salva no diretório
                with open(nome_arquivo, "wb") as f:
                    f.write(requests.get(arquivo_url).content)
                print(f"Baixado: {nome_arquivo}")
                
                # Descompacta o arquivo ZIP
                descompactar_zip(nome_arquivo, pasta_destino)
            else:
                print(f"Arquivo ignorado (não ZIP): {link['href']}")
    else:
        print(f"Erro ao acessar o diretório {url}. Código de status: {response.status_code}")

# Função para descompactar arquivos ZIP
def descompactar_zip(arquivo_zip, pasta_destino):
    try:
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)
            print(f"Arquivo {arquivo_zip} descompactado com sucesso!")
    except zipfile.BadZipFile:
        print(f"Erro ao descompactar o arquivo {arquivo_zip}. Não é um arquivo ZIP válido.")

# Função para inserir os dados no banco de dados
def inserir_dados_no_banco(ano, df):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ans_db"
        )
        
        cursor = conn.cursor()
        
        for index, row in df.iterrows():
            data = row['DATA']
            reg_ans = row['REG_ANS']
            cd_conta_contabil = row['CD_CONTA_CONTABIL']
            descricao = row['DESCRICAO']
            vl_saldo_inicial = row['VL_SALDO_INICIAL']
            vl_saldo_final = row['VL_SALDO_FINAL']
            
            # Exibe os dados que serão inseridos
            
            cursor.execute(""" 
                INSERT INTO demonstracoes_contabeis (ano, data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (ano, data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Dados inseridos com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao inserir dados no banco: {err}")

# Função para processar os arquivos CSV
def processar_arquivos_csv():
    for ano in [2023, 2024]:
        pasta_destino = PASTA_DESTINO_2023 if ano == 2023 else PASTA_DESTINO_2024
        arquivos = [f for f in os.listdir(pasta_destino) if f.endswith('.csv')]
        
        if not arquivos:
            print(f"Não há arquivos CSV em {pasta_destino}.")
            continue
        
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta_destino, arquivo)
            print(f"Lendo arquivo: {caminho_arquivo}")
            
            # Verifica se o arquivo existe antes de tentar abrir
            if os.path.exists(caminho_arquivo):
                try:
                    # Lê o arquivo CSV com pandas
                    df = pd.read_csv(caminho_arquivo, delimiter=";")  # Ajuste o delimitador conforme o formato do seu CSV
                    print(f"Dados lidos do CSV: {df.head()}")  # Exibe as primeiras linhas para verificar os dados

                    # Verifica se o CSV contém dados
                    if df.empty:
                        print(f"O arquivo {arquivo} está vazio.")
                        continue
                    
               

                    # Inserir os dados no banco
                    inserir_dados_no_banco(ano, df)
                    print(f"Dados do ano {ano} inseridos no banco.")
                except Exception as e:
                    print(f"Erro ao ler o arquivo {arquivo}: {e}")
            else:
                print(f"Arquivo não encontrado: {caminho_arquivo}")

# Função principal para baixar arquivos e processar os dados
def baixar_arquivos_e_processar():
    print("Iniciando o download dos arquivos de 2023...")
    baixar_arquivos_do_diretorio(URL_2023, PASTA_DESTINO_2023)
    
    print("Iniciando o download dos arquivos de 2024...")
    baixar_arquivos_do_diretorio(URL_2024, PASTA_DESTINO_2024)
    
    print("Processando arquivos CSV e inserindo dados no banco...")
    processar_arquivos_csv()

if __name__ == "__main__":
    baixar_arquivos_e_processar()
