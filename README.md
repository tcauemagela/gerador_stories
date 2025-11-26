# 📝 Gerador de Histórias de Usuário com IA - V2

Sistema web desenvolvido com Streamlit que utiliza IA (Claude API da Anthropic) para gerar histórias de usuário técnicas no formato de tasks, com suporte a especificações de API dinâmicas baseadas em métodos HTTP REST.

## 🎯 Objetivo

Automatizar a criação de histórias de usuário técnicas bem estruturadas, economizando tempo e garantindo consistência na documentação de tarefas de desenvolvimento.

## ✨ Funcionalidades

### 🆕 NOVIDADES V2 - Especificações de API Dinâmicas
- ✅ **Seleção de Método HTTP:** GET, POST, PUT, PATCH, DELETE
- ✅ **Campos Dinâmicos por Método:**
  - **GET:** Query Params (filtros, paginação, ordenação)
  - **POST:** Body (dados para criação)
  - **PUT:** Path Param + Body completo (substituição)
  - **PATCH:** Path Param + Body parcial (atualização)
  - **DELETE:** Path Param (identificador)
- ✅ **Interpretação REST Automática:** IA valida compatibilidade entre método e campos
- ✅ **Visualização Aprimorada:** Blocos de código JSON com syntax highlighting
- ✅ **Sistema de Debug:** Stack trace completo para identificação rápida de erros

### ETAPA 1 - Criação
- ✅ Formulário intuitivo com múltiplas entradas dinâmicas
- ✅ Geração de histórias técnicas usando Claude AI
- ✅ Histórias no formato de TASK (sem persona de usuário)
- ✅ Visualização em Markdown formatado
- ✅ Exportação em múltiplos formatos (TXT, Markdown, JSON)
- ✅ Validação robusta de entradas
- ✅ Tratamento de erros completo

### ETAPA 2 - Edição e Refinamento
- ✅ Editor visual com preview em tempo real
- ✅ Edição seção por seção com live preview
- ✅ Regeneração seletiva de seções específicas com IA
- ✅ Validação INVEST (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- ✅ Validação local (rápida) e validação profunda com IA
- ✅ Análise e sugestões de melhoria com IA
- ✅ Sistema de versionamento (até 10 versões)
- ✅ Timeline de versões com timestamps e notas
- ✅ Comparação visual (diff) entre versões
- ✅ Restauração de versões anteriores
- ✅ Exportação de relatórios INVEST (JSON/TXT)
- ✅ Arquitetura SOLID/MVC expandida

## 🏗️ Arquitetura

O projeto segue rigorosamente os princípios SOLID e o padrão MVC:

```
gerador_historia/
├── app.py                          # Entry point (routing com tabs)
├── config.py                       # Configurações centralizadas
├── controllers/                    # Controllers (MVC)
│   ├── story_controller.py         # ETAPA 1: Criação
│   └── editor_controller.py        # ETAPA 2: Edição/Refinamento
├── models/                         # Models (MVC)
│   ├── story.py                    # Modelo de história
│   ├── validation.py               # Validações
│   ├── version.py                  # Versionamento
│   └── invest_validator.py         # Validação INVEST
├── views/                          # Views (MVC)
│   ├── story_form_view.py          # ETAPA 1: Formulário
│   ├── story_display_view.py       # ETAPA 1: Exibição
│   ├── editor_view.py              # ETAPA 2: Editor
│   ├── validation_view.py          # ETAPA 2: INVEST
│   ├── suggestions_view.py         # ETAPA 2: Sugestões
│   └── version_view.py             # ETAPA 2: Versões
├── services/                       # Services (lógica de negócio)
│   ├── ai_service.py               # Integração Claude API
│   ├── editor_service.py           # Edição e parsing
│   ├── version_service.py          # Controle de versões
│   └── invest_service.py           # Validação INVEST
└── utils/                          # Utilitários
    ├── constants.py
    ├── helpers.py
    └── formatters.py
```

## 📋 Pré-requisitos

- Python 3.9 ou superior
- Conta na Anthropic com API key
- Pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd gerador_historia
```

### 2. Crie um ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key

**Opção A - Desenvolvimento Local (arquivo .env):**

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

2. Edite o arquivo `.env` e adicione sua API key:
   ```
   ANTHROPIC_API_KEY=sua-chave-api-aqui
   ```

3. Obtenha sua API key em: https://console.anthropic.com/

**Opção B - Streamlit Cloud (Secrets):**

1. Faça deploy no Streamlit Cloud
2. Vá em Settings > Secrets
3. Adicione:
   ```toml
   ANTHROPIC_API_KEY = "sua-chave-api-aqui"
   ```

## ▶️ Como Executar

```bash
streamlit run app.py
```

O aplicativo abrirá automaticamente no seu navegador em `http://localhost:8501`

## 📖 Como Usar

O sistema possui 4 abas principais:

### Tab 1: 📝 Criar História (ETAPA 1)

**1. Preencha o Formulário:**
- **Título**: Nome técnico da tarefa (ex: "Implementar autenticação OAuth")
- **Regras de Negócio**: Use os botões ➕/➖ para adicionar/remover regras
- **APIs/Serviços**: Liste as APIs e serviços necessários
- **Objetivos**: Defina objetivos claros e mensuráveis
- **Complexidade**: Escolha pontos (escala Fibonacci: 1, 2, 3, 5, 8, 13, 21)
- **Critérios de Aceitação**: Liste todos os critérios de aceitação

**2. Gere a História:**
- Clique em "Gerar História"
- Aguarde até 30 segundos para a IA processar
- A história será exibida formatada em Markdown

**3. Exporte:**
- **TXT**: Texto simples
- **Markdown**: Formatação completa
- **JSON**: Dados estruturados
- **Copiar**: Para clipboard

### Tab 2: ✏️ Editar (ETAPA 2)

**Editor Visual com Preview:**
- Edite título e seções individualmente
- Visualize mudanças em tempo real no painel de preview
- Salve alterações (cria nova versão automaticamente)
- Adicione notas às suas edições

**Regeneração Seletiva:**
- Regenere apenas seções específicas (Critérios, Testes, Arquitetura, Benefícios)
- Compare versão antiga vs nova
- Aceite ou rejeite mudanças

**Sugestões de Melhoria:**
- Analise história com IA
- Receba sugestões categorizadas por tipo e severidade
- Filtre sugestões por criticidade

### Tab 3: ✅ Validar INVEST (ETAPA 2)

**Validação Rápida (Local):**
- Validação instantânea baseada em regras
- Sem custo de API

**Validação Profunda (IA):**
- Análise completa com Claude AI
- Justificativas detalhadas para cada critério
- Scores de 0-100 para cada aspecto INVEST

**Critérios Avaliados:**
- **I**ndependent: História pode ser desenvolvida independentemente
- **N**egotiable: Flexibilidade de implementação
- **V**aluable: Entrega valor claro
- **E**stimable: Pode ser estimada com precisão
- **S**mall: Tamanho adequado para sprint
- **T**estable: Possui critérios testáveis

**Relatórios:**
- Exportação em JSON ou TXT
- Pontos fortes e fracos
- Sugestões acionáveis

### Tab 4: 📚 Versões (ETAPA 2)

**Timeline de Versões:**
- Visualize histórico completo (até 10 versões)
- Timestamps e notas de cada versão
- Preview do conteúdo

**Comparação:**
- Compare duas versões lado a lado
- Diff visual (highlighting de diferenças)
- Análise de mudanças

**Restauração:**
- Restaure qualquer versão anterior
- Cria nova versão automaticamente
- Adicione notas de restauração

## 🎨 Formato da História Gerada

As histórias seguem este formato técnico:

```markdown
## 📋 [Título da Tarefa Técnica]

### 🎯 Descrição
[Descrição detalhada da tarefa técnica]

### 📐 Regras de Negócio
[Lista de regras]

### 🔌 APIs/Serviços Necessários
[Lista de APIs com descrição de uso]

### 🎯 Objetivos
[Objetivos claros e mensuráveis]

### ✅ Critérios de Aceitação
[Critérios formatados]

### 🧪 Cenários de Teste Sugeridos
1. Cenário de sucesso (happy path)
2. Cenário de erro/exceção
3. Cenário de edge case

### 📊 Complexidade
Pontos: X
Justificativa: [explicação]
```

## 🔧 Configurações Avançadas

### Modificar Modelo Claude

Edite o arquivo `config.py`:

```python
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 4000
CLAUDE_TIMEOUT = 30
```

### Personalizar Validações

Edite o arquivo `models/validation.py` para ajustar regras de validação.

## 🐛 Troubleshooting

### Erro: "API Key não encontrada"

- Verifique se o arquivo `.env` existe e contém a chave
- Certifique-se de que a chave está no formato: `ANTHROPIC_API_KEY=sk-...`
- No Streamlit Cloud, verifique se adicionou o secret corretamente

### Erro: "Tempo esgotado"

- A IA pode demorar até 30 segundos
- Tente reduzir a quantidade de informações
- Verifique sua conexão com a internet

### Erro: "Limite de requisições atingido"

- Aguarde 1-2 minutos antes de tentar novamente
- Verifique seu plano na Anthropic (limites de rate)

### Formulário não carrega ou campos desaparecem

- Limpe o cache do Streamlit: `streamlit cache clear`
- Reinicie a aplicação

## 📦 Dependências

```
streamlit>=1.28.0      # Framework web
anthropic>=0.7.0       # Cliente API Claude
python-dotenv>=1.0.0   # Gerenciamento de .env
pydantic>=2.0.0        # Validação de dados
```

## 🏛️ Princípios SOLID Aplicados

- **S**ingle Responsibility: Cada módulo tem uma única responsabilidade
- **O**pen/Closed: Aberto para extensão, fechado para modificação
- **L**iskov Substitution: Subtipos substituíveis
- **I**nterface Segregation: Interfaces específicas
- **D**ependency Inversion: Dependências de abstrações

## 🎓 Estrutura de Código

### Models
Contêm a estrutura de dados e regras de validação.

### Views
Renderizam a interface do usuário (formulários e exibições).

### Controllers
Orquestram o fluxo entre Models, Views e Services.

### Services
Implementam lógica de negócio e integrações externas (API).

### Utils
Funções auxiliares e utilitárias reutilizáveis.

## 📝 Próximas Etapas (Roadmap)

- [x] **ETAPA 1**: Criação básica de histórias com IA ✅
- [x] **ETAPA 2**: Edição, validação INVEST e versionamento ✅
- [ ] **ETAPA 3**: Templates personalizáveis e bibliotecas de histórias
- [ ] **ETAPA 4**: Exportação avançada (PDF, DOCX, Jira, Azure DevOps)
- [ ] **ETAPA 5**: Colaboração em equipe e comentários
- [ ] **ETAPA 6**: Dashboard e analytics de histórias

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os princípios SOLID e mantenha a arquitetura MVC.

## 📄 Licença

Este projeto é de código aberto para fins educacionais.

## 📧 Suporte

Para dúvidas ou problemas:
1. Verifique a seção Troubleshooting
2. Revise a documentação da Anthropic: https://docs.anthropic.com/
3. Abra uma issue no repositório do projeto

---

**Desenvolvido com ❤️ usando Streamlit e Claude AI**
