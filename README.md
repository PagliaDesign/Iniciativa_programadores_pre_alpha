# Sistema de Agendamentos com Geração Automática de Documentos

Este é um sistema web completo para gerenciar agendamentos e gerar automaticamente documentos de confirmação em formato Word/PDF.

## 🚀 Funcionalidades

- **Formulário Web Intuitivo**: Interface moderna para registro de agendamentos
- **Armazenamento em Excel**: Todos os dados são salvos em uma planilha Excel persistente
- **Geração Automática de Documentos**: Cria documentos de confirmação personalizados
- **Conversão para PDF**: Converte automaticamente para PDF quando possível
- **Painel de Visualização**: Visualize todos os agendamentos registrados
- **Limpeza Automática**: Remove arquivos antigos automaticamente
- **Busca em Tempo Real**: Busque agendamentos por nome no painel
- **Design Responsivo**: Funciona perfeitamente em desktop e mobile

## 📋 Pré-requisitos

### Para Execução Local
- Python 3.8 ou superior
- Microsoft Word (Windows) ou LibreOffice (macOS/Linux) para conversão PDF

### Para Hospedagem na Nuvem
- Conta no GitHub
- Conta em uma plataforma de hospedagem (Render, Heroku, Railway, etc.)

## 🛠️ Instalação Local

1. **Clone ou baixe este projeto**
2. **Navegue até a pasta do projeto**:
   ```bash
   cd agendamento_web_producao
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie o modelo Word** (se ainda não existir):
   - Crie um arquivo chamado `modelo_confirmacao.docx`
   - Adicione o texto desejado usando os campos: `{{nome}}`, `{{profissional}}`, `{{data}}`, `{{horario}}`

5. **Execute a aplicação**:
   ```bash
   python app.py
   ```

6. **Acesse no navegador**: `http://127.0.0.1:5000`

## ☁️ Deploy na Nuvem (Render)

### Passo 1: Preparar o Código
1. Crie uma conta no [GitHub](https://github.com)
2. Crie um novo repositório
3. Faça upload de todos os arquivos deste projeto para o repositório

### Passo 2: Deploy no Render
1. Crie uma conta no [Render](https://render.com)
2. Clique em "New +" → "Web Service"
3. Conecte sua conta do GitHub
4. Selecione o repositório que você criou
5. Configure:
   - **Name**: `sistema-agendamentos` (ou outro nome)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
6. Clique em "Create Web Service"

### Passo 3: Configurações Adicionais (Opcional)
- Adicione variáveis de ambiente se necessário
- Configure domínio personalizado se desejar

## 📁 Estrutura do Projeto

```
agendamento_web_producao/
├── app.py                    # Aplicação Flask principal
├── core_logic_single.py      # Lógica de geração de documentos
├── modelo_confirmacao.docx   # Modelo Word (você deve criar)
├── requirements.txt          # Dependências Python
├── Procfile                  # Instruções para deploy
├── README.md                 # Este arquivo
├── templates/                # Templates HTML
│   ├── index.html           # Página principal
│   ├── painel.html          # Painel de agendamentos
│   └── sucesso.html         # Página de sucesso
├── static/                   # Arquivos estáticos
│   └── style.css            # Estilos CSS
├── dados_agendamentos.xlsx   # Planilha (criada automaticamente)
└── output/                   # Documentos gerados (criada automaticamente)
```

## 🎯 Como Usar

### Registrar um Agendamento
1. Acesse a página principal
2. Preencha o formulário com:
   - Nome do paciente
   - Profissional responsável
   - Data do agendamento
   - Horário
3. Clique em "Registrar e Gerar Confirmação"
4. Baixe o documento gerado

### Visualizar Agendamentos
1. Clique em "Ver todos os agendamentos"
2. Use a barra de busca para encontrar agendamentos específicos
3. Visualize todos os dados em formato de tabela

## 🔧 Personalização

### Modificar o Modelo de Documento
1. Edite o arquivo `modelo_confirmacao.docx`
2. Use os campos disponíveis:
   - `{{nome}}` - Nome do paciente
   - `{{profissional}}` - Nome do profissional
   - `{{data}}` - Data formatada (DD/MM/YYYY)
   - `{{horario}}` - Horário do agendamento

### Adicionar Novos Campos
1. Modifique o formulário em `templates/index.html`
2. Atualize a lógica em `app.py` na função `registrar()`
3. Adicione os novos campos no modelo Word

### Personalizar Estilos
- Edite o arquivo `static/style.css` para modificar a aparência
- Todos os estilos estão organizados e comentados

## ⚠️ Observações Importantes

### Conversão para PDF
- A conversão para PDF funciona melhor em ambientes locais
- Em alguns serviços de hospedagem gratuitos, pode não estar disponível
- Neste caso, o sistema retorna o arquivo DOCX automaticamente

### Limpeza Automática
- Arquivos na pasta `output/` são automaticamente removidos após 7 dias
- Isso evita acúmulo de arquivos no servidor
- Configure o período em `DIAS_PARA_LIMPEZA` no `app.py`

### Segurança
- Altere a `SECRET_KEY` em produção
- Configure variáveis de ambiente para dados sensíveis
- Considere adicionar autenticação para uso em produção

## 🐛 Solução de Problemas

### Erro na Conversão PDF
```
AVISO: Conversão para PDF falhou. Retornando arquivo DOCX.
```
**Solução**: Normal em ambientes de hospedagem. O arquivo DOCX será fornecido.

### Erro ao Salvar Excel
```
Erro CRÍTICO ao salvar na planilha
```
**Solução**: Verifique permissões de escrita na pasta do projeto.

### Página não carrega
**Solução**: Verifique se todas as dependências foram instaladas corretamente.

## 📞 Suporte

Este sistema foi desenvolvido para ser robusto e fácil de usar. Em caso de dúvidas:

1. Verifique este README
2. Consulte os logs de erro no terminal
3. Verifique se todos os arquivos estão na estrutura correta

## 📄 Licença

Este projeto é de uso livre para fins educacionais e comerciais.

---

**Desenvolvido com ❤️ para automatizar seu fluxo de trabalho de agendamentos.**
