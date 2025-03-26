import mysql.connector
import pandas as pd

# Configuração de conexão com o banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "ans_db"
}

# Função para conectar ao banco de dados
def conectar_db():
    return mysql.connector.connect(**db_config)

# Função para importar dados do CSV para o MySQL
def importar_csv_para_db():
    # Caminho do arquivo CSV
    arquivo_csv = "../../frontend/dataset/operadoras.csv"
    
    # Lê o CSV com pandas
    df = pd.read_csv(arquivo_csv, sep=";", encoding="utf-8")
    
    # Conectar ao banco de dados
    conexao = conectar_db()
    cursor = conexao.cursor()
    
    # Inserir os dados no banco de dados
    for index, row in df.iterrows():
        cursor.execute("""
        INSERT INTO operadoras (nome, cnpj, registro_ans) 
        VALUES (%s, %s, %s)
    """, (row['Razao_Social'], row['CNPJ'], row['Registro_ANS']))

    # Commit para salvar as alterações no banco
    conexao.commit()
    
    cursor.close()
    conexao.close()
    print(f"Dados importados com sucesso do arquivo {arquivo_csv}.")

if __name__ == "__main__":
    importar_csv_para_db()
