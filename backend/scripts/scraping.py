import requests
import os
import zipfile

# URLs dos PDFs
URLs = [
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf",
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf"
]

PASTA_DESTINO = "../../frontend/dataset/"
ARQUIVO_ZIP = "../../frontend/dataset/anexos_compactados.zip"

def baixar_pdfs():
    # Cria o diretório de destino, se necessário
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    # Lista para armazenar os caminhos dos PDFs baixados
    pdf_paths = []

    for url in URLs:
        response = requests.get(url)
        if response.status_code == 200:
            nome_arquivo = os.path.join(PASTA_DESTINO, os.path.basename(url))
            with open(nome_arquivo, "wb") as f:
                f.write(response.content)
            pdf_paths.append(nome_arquivo)  # Adiciona o caminho do PDF baixado
            print(f"PDF baixado: {nome_arquivo}")
        else:
            print(f"Erro ao baixar o PDF da URL {url}. Código de status: {response.status_code}")

    # Compactar os PDFs em um arquivo ZIP
    compactar_em_zip(pdf_paths)

def compactar_em_zip(pdf_paths):
    with zipfile.ZipFile(ARQUIVO_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdf_paths:
            zipf.write(pdf, os.path.basename(pdf))  # Adiciona o PDF ao arquivo ZIP
            print(f"Adicionado ao ZIP: {pdf}")
    print(f"Todos os PDFs foram compactados em {ARQUIVO_ZIP}")

if __name__ == "__main__":
    baixar_pdfs()
