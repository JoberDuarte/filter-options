import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Função para excluir arquivos CSV antigos na pasta de downloads
def excluir_csvs_anteriores(pasta_downloads):
    for arquivo in os.listdir(pasta_downloads):
        if arquivo.endswith(".csv"):
            arquivo_path = os.path.join(pasta_downloads, arquivo)
            os.remove(arquivo_path)  # Exclui o arquivo CSV
            print(f"Arquivo excluído: {arquivo}")

# Função para realizar o download do CSV da B3 e renomear o arquivo
def download_csv_b3():
    pasta_downloads = r"D:\Projetos_Python\downloads"
    excluir_csvs_anteriores(pasta_downloads)
    
    options = webdriver.EdgeOptions()
    prefs = {"download.default_directory": pasta_downloads}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Edge(service=Service(r"c:\Users\jober\Downloads\edgedriver_win64\msedgedriver.exe"), options=options)

    try:
        driver.get("https://arquivos.b3.com.br/#")
        wait = WebDriverWait(driver, 10)
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="collapse"]/div/div/div[1]/div[2]/p[2]/a[1]'))
        )
        download_button.click()
        time.sleep(5)
        print("Download concluído!")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

    arquivos_csv = [f for f in os.listdir(pasta_downloads) if f.endswith('.csv')]
    if arquivos_csv:
        arquivos_csv.sort(key=lambda x: os.path.getmtime(os.path.join(pasta_downloads, x)), reverse=True)
        arquivo_mais_recente = arquivos_csv[0]
        novo_nome_arquivo = "dados_b3_atual.csv"
        caminho_arquivo_original = os.path.join(pasta_downloads, arquivo_mais_recente)
        caminho_arquivo_novo = os.path.join(pasta_downloads, novo_nome_arquivo)
        os.rename(caminho_arquivo_original, caminho_arquivo_novo)
        print(f"Arquivo renomeado para: {novo_nome_arquivo}")
    else:
        print("Nenhum arquivo CSV encontrado na pasta de downloads.")
    return os.path.join(pasta_downloads, novo_nome_arquivo)

# Função para filtrar as opções no CSV e manter as colunas desejadas
def filtrar_opcoes_csv(caminho_csv, pasta_downloads):
    # Lê o CSV e especifica o delimitador como ponto e vírgula
    df = pd.read_csv(caminho_csv, encoding='ISO-8859-1', delimiter=';', header=1, on_bad_lines='skip')
    
    # Verifica e imprime os nomes das colunas
    print(f"Colunas no arquivo CSV: {df.columns.tolist()}")

    # Filtra apenas as linhas onde 'MktNm' é 'EQUITY-DERIVATE'
    df_filtrado = df[df['MktNm'] == 'EQUITY-DERIVATE']

    # Mantém as colunas desejadas, incluindo as novas colunas OptnTp e OptnStyle
    df_filtrado = df_filtrado[['TckrSymb', 'Asst', 'AsstDesc', 'XprtnDt', 'OptnTp', 'OptnStyle']]

    # Salva o CSV tratado
    novo_csv = os.path.join(pasta_downloads, 'dados_filtrados.csv')
    df_filtrado.to_csv(novo_csv, index=False)
    print(f"Novo CSV com os dados filtrados salvo em: {novo_csv}")
    return novo_csv

# Caminho para a pasta onde os CSVs são salvos
pasta_downloads = r"D:\Projetos_Python\downloads"

# 1. Realiza o download do CSV e renomeia o arquivo
caminho_csv = download_csv_b3()

# 2. Filtra as opções no CSV e salva em um novo arquivo
novo_csv_tratado = filtrar_opcoes_csv(caminho_csv, pasta_downloads)






