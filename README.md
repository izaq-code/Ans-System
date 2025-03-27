# Documentação do Projeto: Ans System

Este projeto é composto por um **backend** utilizando **Flask** em Python e um **frontend** desenvolvido com **Vue.js**. Ele é destinado ao processamento de dados relacionados a operadoras, extração de PDFs, conversão de dados para CSV, e importação para um banco de dados MySQL.

## Estrutura do Projeto

A estrutura do projeto é a seguinte:

```
ans_system/
├── backend/
│   ├── app.py                  # Servidor Flask
│   ├── database.sql            # Script SQL para MySQL
│   ├── requirements.txt        # Dependências do Python
│   ├── scripts/                
│   │   ├── scraping.py         # Web scraping e download de PDFs
│   │   ├── process_pdf.py      # Extração e conversão dos dados do PDF para CSV
│   │   ├── db_import.py        # Importação do CSV para o MySQL
│
├── frontend/
│   ├── src/
│   │   ├── App.vue                  # Componente principal do Vue
│   │   ├── main.js                       # Arquivo principal do Vue.js
│   |
│   ├── dataset/
│   │   ├── operadoras.csv           # Dados baixados das operadoras
│   │   ├── anexos.zip               # PDFs baixados e compactados
│   │
│   ├── public/
│   │   ├── index.html                # Página inicial
│   │   ├── style.css                 # Estilos globais
│   ├── package.json                  # Dependências do Vue.js
│
├── .gitignore                       
├── README.md                        # Documentação do projeto
```

## Iniciando o Banco de Dados

Antes de iniciar o backend e o frontend, certifique-se de que o banco de dados MySQL esteja rodando.

1. Inicie o MySQL e crie o banco de dados, se ainda não existir:
   ```sql
         CREATE DATABASE ans_db;
         USE ans_db;

         CREATE TABLE operadoras (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cnpj VARCHAR(20) NOT NULL,
            registro_ans VARCHAR(20) NOT NULL
         );

         CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ano INT NOT NULL,
            trimestre INT NOT NULL,
            data DATE,
            reg_ans VARCHAR(20),
            cd_conta_contabil VARCHAR(50),
            descricao VARCHAR(255),
            vl_saldo_inicial DECIMAL(15,2),
            vl_saldo_final DECIMAL(15,2)
         );
   ```
2. Confirme que o banco de dados está funcionando corretamente antes de prosseguir para os próximos passos.

### Backend

O backend é responsável pela execução de scripts que processam e importam dados para um banco de dados MySQL.

#### Passos para iniciar o backend

1. Navegue até a pasta `backend`:
   ```bash
   cd backend
   ```

2. Instale as dependências do Python:
   ```bash
   pip install -r requirements.txt
   ```

3. Navegue até a pasta `backend/scripts`:
   ```bash
   cd scripts
   ```

4. Execute os seguintes scripts em ordem para processar e importar os dados:
   ```bash
   python scraping.py       # Web scraping e download de PDFs
   python process_pdf.py    # Extração e conversão dos dados do PDF para CSV
   python pastas.py         # Organiza arquivos em pastas
   python csv_handler.py    # Processamento do CSV
   python db_import.py      # Importação do CSV para o MySQL
   ```
   
5. Volte até a pasta `backend`:
  ```bash
   cd ..  
 ```
6. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

### Frontend

O frontend é uma aplicação Vue.js que serve como interface de usuário.

#### Passos para iniciar o frontend

1. Navegue até a pasta `frontend`:
   ```bash
   cd frontend
   ```

2. Instale as dependências do projeto:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run serve
   ```

### Dataset

Os dados que são baixados das operadoras são armazenados na pasta `dataset`:

- `operadoras.csv` – Arquivo CSV com os dados processados das operadoras.
- `anexos.zip` – Arquivo compactado contendo os PDFs baixados.

### Como Usar

1. **Inicie o banco de dados** antes de qualquer outro passo.
2. **Inicie o backend** primeiro para garantir que a API esteja rodando.
3. **Inicie o frontend** para acessar a interface de usuário.
4. O sistema irá processar os PDFs, extrair os dados e importá-los para o banco de dados MySQL.
5. A interface do Vue.js permite buscar e exibir dados das operadoras processadas.

### Conclusão

Este projeto combina o poder do Python com Flask e o Vue.js para criar um sistema robusto para o processamento e exibição de dados. Certifique-se de seguir as instruções de instalação corretamente para garantir que tudo funcione como esperado.

