# core_logic_single.py

from docxtpl import DocxTemplate
import os
import re
from datetime import datetime

def limpar_nome_arquivo(nome):
    """Remove caracteres inválidos para nomes de arquivo."""
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome)
    return nome_limpo.replace(' ', '_')

def gerar_e_converter_para_pdf(contexto, template_path, output_folder):
    """
    Gera um documento Word e tenta convertê-lo para PDF.
    Se a conversão falhar (comum em ambientes de hospedagem), retorna o DOCX.
    Retorna o nome do arquivo gerado.
    """
    try:
        template = DocxTemplate(template_path)
        
        # Formata a data para DD/MM/YYYY
        if 'data' in contexto and contexto['data']:
            data_obj = datetime.strptime(contexto['data'], '%Y-%m-%d')
            contexto['data'] = data_obj.strftime('%d/%m/%Y')

        template.render(contexto)

        nome_limpo = limpar_nome_arquivo(contexto.get('nome', 'sem_nome'))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        nome_base_arquivo = f"Confirmacao_{nome_limpo}_{timestamp}"
        caminho_docx = os.path.join(output_folder, f"{nome_base_arquivo}.docx")
        
        template.save(caminho_docx)

        # Tenta converter para PDF (pode falhar em ambientes de hospedagem)
        try:
            from docx2pdf import convert
            caminho_pdf = os.path.join(output_folder, f"{nome_base_arquivo}.pdf")
            convert(caminho_docx, caminho_pdf)
            os.remove(caminho_docx)  # Remove o DOCX após conversão bem-sucedida
            return f"{nome_base_arquivo}.pdf"
        except ImportError:
            print("AVISO: docx2pdf não disponível. Retornando arquivo DOCX.")
            return f"{nome_base_arquivo}.docx"
        except Exception as e:
            print(f"AVISO: Conversão para PDF falhou ({e}). Retornando arquivo DOCX.")
            return f"{nome_base_arquivo}.docx"

    except Exception as e:
        print(f"ERRO no processo de geração: {e}")
        return None
