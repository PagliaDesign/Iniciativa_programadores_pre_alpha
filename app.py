# app.py

from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import pandas as pd
import os
import time
from datetime import datetime

# Importa a lógica de geração e conversão
from core_logic_single import gerar_e_converter_para_pdf 

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'mude_esta_chave_secreta_depois')

# --- Configurações ---
ARQUIVO_EXCEL = 'dados_agendamentos.xlsx'
MODELO_WORD = 'modelo_confirmacao.docx'
PASTA_SAIDA = 'output'
DIAS_PARA_LIMPEZA = 7 # Arquivos na pasta 'output' mais antigos que isso serão apagados

# Garante que a pasta de saída exista
if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

# --- Lógica de Limpeza Automática ---
def limpar_arquivos_antigos():
    """Apaga arquivos na pasta de saída mais antigos que DIAS_PARA_LIMPEZA."""
    try:
        arquivos_apagados = 0
        agora = time.time()
        
        for filename in os.listdir(PASTA_SAIDA):
            caminho_arquivo = os.path.join(PASTA_SAIDA, filename)
            if os.path.isfile(caminho_arquivo):
                if os.stat(caminho_arquivo).st_mtime < agora - (DIAS_PARA_LIMPEZA * 86400):
                    os.remove(caminho_arquivo)
                    arquivos_apagados += 1
        
        if arquivos_apagados > 0:
            print(f"LIMPEZA: {arquivos_apagados} arquivo(s) antigo(s) foram removidos da pasta '{PASTA_SAIDA}'.")
    except Exception as e:
        print(f"AVISO: Não foi possível executar a limpeza de arquivos. Erro: {e}")

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário."""
    limpar_arquivos_antigos()
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    """Recebe os dados, salva no Excel e gera o documento PDF."""
    novo_agendamento = {
        'nome': request.form['nome'],
        'profissional': request.form['profissional'],
        'data': request.form['data'],
        'horario': request.form['horario'],
    }

    try:
        df_existente = pd.read_excel(ARQUIVO_EXCEL) if os.path.exists(ARQUIVO_EXCEL) else pd.DataFrame()
        novo_df = pd.DataFrame([novo_agendamento])
        df_final = pd.concat([df_existente, novo_df], ignore_index=True)
        df_final.to_excel(ARQUIVO_EXCEL, index=False)
    except Exception as e:
        flash(f"Erro CRÍTICO ao salvar na planilha: {e}", 'error')
        return redirect(url_for('index'))

    nome_arquivo_pdf = gerar_e_converter_para_pdf(
        contexto=novo_agendamento.copy(),
        template_path=MODELO_WORD,
        output_folder=PASTA_SAIDA
    )

    if nome_arquivo_pdf:
        flash(f"Agendamento para '{novo_agendamento['nome']}' registrado!", 'success')
        return redirect(url_for('sucesso', filename=nome_arquivo_pdf))
    else:
        flash("Agendamento salvo no Excel, mas houve um erro ao gerar o PDF. Verifique se o LibreOffice está disponível no servidor.", 'error')
        return redirect(url_for('index'))

@app.route('/painel')
def painel():
    """Exibe todos os agendamentos registrados em uma tabela."""
    agendamentos = []
    if os.path.exists(ARQUIVO_EXCEL):
        try:
            df = pd.read_excel(ARQUIVO_EXCEL)
            if 'data' in df.columns:
                df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            agendamentos = df.to_dict('records')
        except Exception as e:
            flash(f"Erro ao ler o arquivo de agendamentos: {e}", "error")
    
    return render_template('painel.html', agendamentos=agendamentos)

@app.route('/sucesso/<filename>')
def sucesso(filename):
    """Página de sucesso com link para download do PDF."""
    return render_template('sucesso.html', filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    """Serve o arquivo PDF para download."""
    return send_from_directory(PASTA_SAIDA, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Servidor iniciado! Acesse em http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port)
