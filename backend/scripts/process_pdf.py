import zipfile
import os
import PyPDF2
import pandas as pd
import shutil  # Importando shutil para remover diretórios não vazios

# Caminhos de origem e destino
PASTA_ORIGEM = "../../frontend/dataset/"
ARQUIVO_ZIP = os.path.join(PASTA_ORIGEM, "anexos_compactados.zip")
ARQUIVO_SAIDA = os.path.join(PASTA_ORIGEM, "rol_procedimentos.csv")
PASTA_TEMP = os.path.join(PASTA_ORIGEM, "temp_pdfs")

# Descrições completas para substituir as abreviações
LEGENDAS = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial",
}

# Função para abrir o ZIP e extrair os PDFs
def extrair_pdfs_do_zip():
    os.makedirs(PASTA_TEMP, exist_ok=True)
    with zipfile.ZipFile(ARQUIVO_ZIP, 'r') as zip_ref:
        zip_ref.extractall(PASTA_TEMP)
    print(f"Arquivos extraídos para {PASTA_TEMP}")

# Função para extrair dados dos PDFs
def extrair_dados_pdf():
    arquivos = [f for f in os.listdir(PASTA_TEMP) if f.endswith(".pdf")]
    dados_extraidos = []

    for arquivo in arquivos:
        caminho_pdf = os.path.join(PASTA_TEMP, arquivo)
        with open(caminho_pdf, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                texto = page.extract_text()
                dados_extraidos.append(texto)

    df = pd.DataFrame({"dados": dados_extraidos})
    df.to_csv(ARQUIVO_SAIDA, index=False)
    print(f"Dados extraídos e salvos em {ARQUIVO_SAIDA}")

# Função para substituir abreviações por descrições completas
def substituir_abreviacoes():
    df = pd.read_csv(ARQUIVO_SAIDA)

    # Substituir as abreviações pelas descrições completas
    for coluna, descricao in LEGENDAS.items():
        df = df.replace({coluna: descricao})

    # Salvar o CSV modificado
    df.to_csv(ARQUIVO_SAIDA, index=False)
    print(f"Abreviações substituídas e CSV salvo em {ARQUIVO_SAIDA}")

# Função para compactar o CSV em um arquivo ZIP
def compactar_csv():
    arquivo_zip_saida = os.path.join(PASTA_ORIGEM, "rol_procedimentos_modificado.zip")
    with zipfile.ZipFile(arquivo_zip_saida, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(ARQUIVO_SAIDA, os.path.basename(ARQUIVO_SAIDA))
    print(f"CSV compactado em {arquivo_zip_saida}")

# Função para excluir a pasta temporária
def excluir_pasta_temp():
    if os.path.exists(PASTA_TEMP):
        try:
            # Remove a pasta temporária e todo o seu conteúdo
            shutil.rmtree(PASTA_TEMP)
            print(f"Pasta temporária {PASTA_TEMP} excluída.")
        except Exception as e:
            print(f"Erro ao excluir a pasta {PASTA_TEMP}: {e}")
    else:
        print(f"A pasta temporária {PASTA_TEMP} não existe.")

# Função principal
def main():
    # Extrair PDFs do arquivo ZIP
    extrair_pdfs_do_zip()

    # Extrair dados dos PDFs
    extrair_dados_pdf()

    # Substituir abreviações por descrições completas
    substituir_abreviacoes()

    # Compactar o CSV gerado
    compactar_csv()

    # Excluir a pasta temporária
    excluir_pasta_temp()

if __name__ == "__main__":
    main()
