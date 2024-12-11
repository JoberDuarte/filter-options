#Código Jober
from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import re


#Código Adriana
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for, Response
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.secret_key = "sua_chave_secreta_segura"

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            flash("O email de usuário é obrigatório!", "danger")
            return render_template("registrar.html")
        if not request.form.get("password"):
            flash("Senha é obrigatória!", "danger")
            return render_template("registrar.html")
        if request.form.get("password") != request.form.get("confirmation"):
            flash("As senhas não coincidem!", "danger")
            return render_template("registrar.html")

        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE email = ?", (request.form.get("email"),)).fetchall()
        conn.close()
        
        if rows:
            flash("Este email já está registrado!", "danger")
            return render_template("registrar.html")

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (email, hash) VALUES (?, ?)",
            (request.form.get("email"), generate_password_hash(request.form.get("password"))),
        )
        conn.commit()
        conn.close()

        flash("Registro realizado com sucesso!", "success")
        return redirect(url_for("login"))
    
    return render_template("registrar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("E-mail e senha são obrigatórios!", "danger")
            return render_template("login.html")

        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
        conn.close()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("E-mail ou senha inválidos!", "danger")
            return render_template("login.html")

        session["user_id"] = rows[0]["id"]
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("filtros"))
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "info")
    return redirect("/")

#A partir daqui o código é do Jober

# Caminho para o arquivo CSV tratado
CSV_FILE = r"C:\filter-options\downloads\dados_filtrados.csv"

# Lista de ativos IBOVESPA
IBOVESPA_ATIVOS = [
    "ALOS3", "ALPA4", "ABEV3", "ASAI3", "AURE3", "AZUL4", "AZZA3", 
    "B3SA3", "BBSE3", "BBDC3", "BBDC4", "BRAP4", "BBAS3", "BRKM5",
    "BRAV3", "BRFS3", "BPAC11", "CXSE3", "CRFB3", "CCRO3", "CMIG4", 
    "COGN3", "CPLE6", "CSAN3", "CPFE3", "CMIN3", "CVCB3", "CYRE3", 
    "ELET3", "ELET6", "EMBR3", "ENGI11", "ENEV3", "EGIE3", "EQTL3", 
    "EZTC3", "FLRY3", "GGBR4", "GOAU4", "NTCO3", "HAPV3", "HYPE3", 
    "IGTI11", "IRBR3", "ISAE4", "ITSA4", "ITUB4", "JBSS3", "KLBN11", 
    "RENT3", "LREN3", "LWSA3", "MGLU3", "MRFG3", "BEEF3", "MRVE3", 
    "MULT3", "PCAR3", "PETR3", "PETR4", "RECV3", "PRIO3", "PETZ3", 
    "RADL3", "RAIZ4", "RDOR3", "RAIL3", "SBSP3", "SANB11", "STBP3", 
    "SMTO3", "CSNA3", "SLCE3", "SUZB3", "TAEE11", "VIVT3", "TIMS3", 
    "TOTS3", "UGPA3", "USIM5", "VALE3", "VAMO3", "VBBR3", "VIVA3", 
    "WEGE3", "YDUQ3"
]

@app.route("/filtros")
def filtros():
    if not os.path.exists(CSV_FILE):
        return "O arquivo 'dados_filtrados.csv' não foi encontrado. Certifique-se de que ele foi gerado corretamente.", 404

    # Carrega os dados para gerar as opções de filtros
    df = pd.read_csv(CSV_FILE)

    # Remove espaços extras nas colunas e converte para maiúsculas
    df['OptnTp'] = df['OptnTp'].str.strip().str.upper()
    df['OptnStyle'] = df['OptnStyle'].str.strip().str.upper()

    # Filtra valores 'NaN' das colunas e garante que os valores sejam únicos
    ativos = df['Asst'].dropna().unique().tolist()

    # Filtra apenas os ativos terminados em números
    ativos = [ativo for ativo in ativos if ativo[-1].isdigit()]

    expiracoes = df['XprtnDt'].dropna().unique().tolist()
    opcao_tipo = df['OptnTp'].dropna().unique().tolist()
    opcao_estilo = df['OptnStyle'].dropna().unique().tolist()

    # Converte a coluna de datas de expiração para datetime
    expiracoes = pd.to_datetime(expiracoes, errors='coerce')

    # Ordena as datas de expiração
    expiracoes = sorted(expiracoes)

    # Formata as datas para exibir somente a data (sem hora)
    expiracoes = [date.strftime('%Y-%m-%d') for date in expiracoes]

    # Evitar duplicatas nas listas, garantindo que cada valor seja único
    opcao_tipo = list(set(opcao_tipo))
    opcao_estilo = list(set(opcao_estilo))

    # Passa a lista de ativos IBOVESPA para o template
    return render_template('filtros.html', 
                           ativos=ativos, 
                           expiracoes=expiracoes,
                           opcao_tipo=opcao_tipo,
                           opcao_estilo=opcao_estilo,
                           ibovespa_ativos=IBOVESPA_ATIVOS)




@app.route('/download-semanais')
def download_semanal():
    if not os.path.exists(CSV_FILE):
        return "O arquivo 'dados_filtrados.csv' não foi encontrado. Certifique-se de que ele foi gerado corretamente.", 404

    # Carrega os dados do CSV
    df = pd.read_csv(CSV_FILE)

    # Filtra as opções semanais (terminadas em W1, W2, W3, W4, W5) na coluna 'TckrSymb'
    df_semanal = df[df['TckrSymb'].str.endswith(('W1', 'W2', 'W3', 'W4', 'W5'), na=False)]

    # Salva os dados filtrados em um novo arquivo
    output_file = r"C:\filter-options\downloads\dados_semanal.csv"
    df_semanal.to_csv(output_file, index=False)

    return send_file(output_file, as_attachment=True)



@app.route('/filtrar', methods=['POST'])
def filtrar():
    if not os.path.exists(CSV_FILE):
        return "O arquivo 'dados_filtrados.csv' não foi encontrado. Certifique-se de que ele foi gerado corretamente.", 404

    # Carrega os dados do CSV
    df = pd.read_csv(CSV_FILE)

    # Verifica se o DataFrame não está vazio
    if df.empty:
        return "O arquivo CSV está vazio. Certifique-se de que contém dados válidos.", 404

    # Obtém as seleções do usuário
    ativos_selecionados = request.form.getlist('ativos')
    expiracoes_selecionadas = request.form.getlist('expiracoes')
    tipos_selecionados = request.form.getlist('opcao_tipo')
    estilos_selecionados = request.form.getlist('opcao_estilo')

    # Log para depuração
    print("Ativos selecionados:", ativos_selecionados)
    print("Expirações selecionadas:", expiracoes_selecionadas)
    print("Tipos selecionados:", tipos_selecionados)
    print("Estilos selecionados:", estilos_selecionados)

    # Remove espaços extras nas colunas do DataFrame
    df['Asst'] = df['Asst'].str.strip()
    df['XprtnDt'] = df['XprtnDt'].str.strip()
    df['OptnTp'] = df['OptnTp'].str.strip().str.upper()
    df['OptnStyle'] = df['OptnStyle'].str.strip().str.upper()

    # Filtra os dados com base nas seleções do usuário
    df_filtrado = df.copy()
    if ativos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['Asst'].isin(ativos_selecionados)]
    if expiracoes_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['XprtnDt'].isin(expiracoes_selecionadas)]
    if tipos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['OptnTp'].isin(tipos_selecionados)]
    if estilos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['OptnStyle'].isin(estilos_selecionados)]

    # Verifica se o DataFrame filtrado está vazio
    if df_filtrado.empty:
        return "Nenhum dado corresponde aos filtros selecionados.", 404

    # Salva os dados filtrados em um novo arquivo
    output_file = r"C:\filter-options\downloads\dados_filtrados_usuario.csv"
    df_filtrado.to_csv(output_file, index=False)

    return send_file(output_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)





