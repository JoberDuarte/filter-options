import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def excluir_csvs_anteriores(pasta_downloads):
    # Lista todos os arquivos na pasta de downloads
    for arquivo in os.listdir(pasta_downloads):
        # Verifica se o arquivo é um CSV
        if arquivo.endswith(".csv"):
            arquivo_path = os.path.join(pasta_downloads, arquivo)
            os.remove(arquivo_path)  # Exclui o arquivo CSV
            print(f"Arquivo excluído: {arquivo}")

def download_csv_b3():
    # Caminho para a pasta de downloads
    pasta_downloads = r"C:\filter-options\downloads"
    
    # Exclui os arquivos CSV antigos
    excluir_csvs_anteriores(pasta_downloads)
    
    # Configuração do navegador Edge
    options = webdriver.EdgeOptions()
    prefs = {"download.default_directory": pasta_downloads}
    options.add_experimental_option("prefs", prefs)
    
    # Caminho para o driver do Edge
    driver = webdriver.Edge(service=Service(r"c:\Users\jober\Downloads\edgedriver_win64\msedgedriver.exe"), options=options)

    try:
        # Acessar a página da B3
        driver.get("https://arquivos.b3.com.br/#")

        # Esperar até que o botão esteja presente
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="collapse"]/div/div/div[1]/div[2]/p[2]/a[1]'))
        )

        # Clique no botão de download
        download_button.click()

        # Opcional: esperar até que o arquivo seja baixado
        time.sleep(10)

        print("Download concluído!")

    except Exception as e:
        print(f"Erro: {e}")

    finally:
        driver.quit()

    # Lista os arquivos CSV na pasta de downloads
    arquivos_csv = [f for f in os.listdir(pasta_downloads) if f.endswith('.csv')]
    
    if arquivos_csv:
        # Ordena os arquivos CSV pela data de modificação (mais recente primeiro)
        arquivos_csv.sort(key=lambda x: os.path.getmtime(os.path.join(pasta_downloads, x)), reverse=True)
        
        # Caminho do arquivo mais recente
        arquivo_mais_recente = arquivos_csv[0]
        
        # Define o novo nome para o arquivo
        novo_nome_arquivo = "dados_b3_atual.csv"
        
        # Caminho completo do arquivo mais recente e o novo nome
        caminho_arquivo_original = os.path.join(pasta_downloads, arquivo_mais_recente)
        caminho_arquivo_novo = os.path.join(pasta_downloads, novo_nome_arquivo)
        
        # Renomeia o arquivo
        os.rename(caminho_arquivo_original, caminho_arquivo_novo)
        print(f"Arquivo renomeado para: {novo_nome_arquivo}")
    else:
        print("Nenhum arquivo CSV encontrado na pasta de downloads.")

# Chama a função para realizar o download
download_csv_b3()
