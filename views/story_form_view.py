"""
View responsável por renderizar o formulário de entrada.
Implementa campos com múltiplas entradas dinâmicas.
Segue Single Responsibility Principle.
"""

import streamlit as st
from typing import Dict, Any
from models.validation import validate_form


def initialize_session_state():
    """
    Inicializa o session_state com valores padrão.
    Deve ser chamado antes de renderizar o formulário.
    """
    # Value Area (tipo de história)
    if 'value_area' not in st.session_state:
        st.session_state.value_area = "Business"

    if 'titulo' not in st.session_state:
        st.session_state.titulo = ""

    if 'regras_negocio' not in st.session_state:
        st.session_state.regras_negocio = [""]

    if 'apis_servicos' not in st.session_state:
        st.session_state.apis_servicos = [""]

    if 'objetivos' not in st.session_state:
        st.session_state.objetivos = [""]

    if 'complexidade' not in st.session_state:
        st.session_state.complexidade = 5

    if 'criterios_aceitacao' not in st.session_state:
        st.session_state.criterios_aceitacao = [""]

    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = []

    # Campos específicos para API
    if 'is_api' not in st.session_state:
        st.session_state.is_api = False

    if 'api_metodo' not in st.session_state:
        st.session_state.api_metodo = "GET"

    if 'api_endpoint' not in st.session_state:
        st.session_state.api_endpoint = ""

    if 'api_query_params' not in st.session_state:
        st.session_state.api_query_params = ""

    if 'api_path_param' not in st.session_state:
        st.session_state.api_path_param = ""

    if 'api_body' not in st.session_state:
        st.session_state.api_body = ""

    if 'api_formato_resposta' not in st.session_state:
        st.session_state.api_formato_resposta = ""

    # Subseções de Objetivos
    if 'objetivo_como' not in st.session_state:
        st.session_state.objetivo_como = ""

    if 'objetivo_quero' not in st.session_state:
        st.session_state.objetivo_quero = ""

    if 'objetivo_para_que' not in st.session_state:
        st.session_state.objetivo_para_que = ""

    # Campo de Dependências (Business)
    if 'has_dependencies' not in st.session_state:
        st.session_state.has_dependencies = False

    if 'dependencies' not in st.session_state:
        st.session_state.dependencies = ""

    # Campos específicos para Spike
    if 'spike_pergunta' not in st.session_state:
        st.session_state.spike_pergunta = ""

    if 'spike_alternativas' not in st.session_state:
        st.session_state.spike_alternativas = [""]

    if 'spike_timebox' not in st.session_state:
        st.session_state.spike_timebox = 8

    if 'spike_output' not in st.session_state:
        st.session_state.spike_output = "Documento de decisão"

    if 'spike_criterios_sucesso' not in st.session_state:
        st.session_state.spike_criterios_sucesso = [""]

    # Campos específicos para Kaizen
    if 'kaizen_processo' not in st.session_state:
        st.session_state.kaizen_processo = ""

    if 'kaizen_situacao_atual' not in st.session_state:
        st.session_state.kaizen_situacao_atual = ""

    if 'kaizen_meta' not in st.session_state:
        st.session_state.kaizen_meta = ""

    if 'kaizen_metricas' not in st.session_state:
        st.session_state.kaizen_metricas = [""]

    if 'kaizen_impacto' not in st.session_state:
        st.session_state.kaizen_impacto = ""

    # Campos específicos para Fix/Bug/Incidente
    if 'fix_descricao' not in st.session_state:
        st.session_state.fix_descricao = ""

    if 'fix_passos_reproduzir' not in st.session_state:
        st.session_state.fix_passos_reproduzir = [""]

    if 'fix_comportamento_esperado' not in st.session_state:
        st.session_state.fix_comportamento_esperado = ""

    if 'fix_comportamento_atual' not in st.session_state:
        st.session_state.fix_comportamento_atual = ""

    if 'fix_ambiente' not in st.session_state:
        st.session_state.fix_ambiente = "Produção"

    if 'fix_severidade' not in st.session_state:
        st.session_state.fix_severidade = "Média"

    if 'fix_logs' not in st.session_state:
        st.session_state.fix_logs = ""


def render_multiple_text_areas(
    label: str,
    key_prefix: str,
    state_key: str,
    placeholder: str = ""
):
    """
    Renderiza múltiplas text_areas com botões de adicionar/remover.

    Args:
        label: Label do campo
        key_prefix: Prefixo para keys únicas
        state_key: Chave no session_state
        placeholder: Texto placeholder
    """
    # Label com caixa de destaque
    st.markdown(f"""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">{label}</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)

    items = st.session_state[state_key]

    for i, item in enumerate(items):
        col1, col2 = st.columns([6, 1])

        with col1:
            new_value = st.text_area(
                f"{label} {i + 1}",
                value=item,
                key=f"{key_prefix}_{i}",
                placeholder=placeholder,
                label_visibility="collapsed",
                height=100
            )
            st.session_state[state_key][i] = new_value

        with col2:
            # Botão remover (só aparece se houver mais de 1 item)
            if len(items) > 1:
                if st.button("➖", key=f"remove_{key_prefix}_{i}", help="Remover"):
                    st.session_state[state_key].pop(i)
                    st.rerun()

    # Botão adicionar
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        if st.button(f"➕ Adicionar {label}", key=f"add_{key_prefix}"):
            st.session_state[state_key].append("")
            st.rerun()

    st.markdown("---")


def render_form() -> Dict[str, Any]:
    """
    Renderiza o formulário completo de entrada.

    Returns:
        Dict com os dados do formulário ou None se não submetido
    """
    initialize_session_state()

    # Título principal com destaque (sem emoji)
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        ">
            <h2 style="color: white; margin: 0; font-weight: 700;">Criar Nova História</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Seletor de Categoria da História
    st.markdown("""
        <div style="
            background-color: rgba(236, 72, 153, 0.1);
            border-left: 4px solid #EC4899;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Categoria da Historia</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)

    value_area_options = {
        "Business": "Funcional - Entrega de valor ao usuário",
        "Spike": "Exploratória - Investigação/pesquisa técnica",
        "Kaizen": "Melhoria Contínua - Otimização de processos",
        "Fix/Bug/Incidente": "Corretiva - Correção de bugs e incidentes"
    }

    st.session_state.value_area = st.selectbox(
        "Value Area",
        options=list(value_area_options.keys()),
        format_func=lambda x: f"{x} - {value_area_options[x]}",
        index=list(value_area_options.keys()).index(st.session_state.value_area),
        label_visibility="collapsed",
        key="value_area_select"
    )
    st.markdown("---")

    # Renderizar campos baseados no Value Area selecionado
    if st.session_state.value_area == "Business":
        return _render_business_form()
    elif st.session_state.value_area == "Spike":
        return _render_spike_form()
    elif st.session_state.value_area == "Kaizen":
        return _render_kaizen_form()
    elif st.session_state.value_area == "Fix/Bug/Incidente":
        return _render_fix_form()

    return None


def _render_business_form() -> Dict[str, Any]:
    """Renderiza formulário para histórias Business (funcionais)."""

    # Campo 1: Título (único, sem múltiplas entradas)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Título da Tarefa</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.titulo = st.text_input(
        "Título",
        value=st.session_state.titulo,
        max_chars=100,
        placeholder="Ex: DU Benefícios - Desenvolver API Districts/Bairros",
        help="Título técnico da tarefa (máx. 100 caracteres, sem caracteres especiais !@#$%^&*())",
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Campo 2: Regras de Negócio (múltiplas entradas)
    render_multiple_text_areas(
        label="Regras de Negócio",
        key_prefix="regra",
        state_key="regras_negocio",
        placeholder="Descreva uma regra de negócio..."
    )

    # Campo 3: APIs/Serviços (múltiplas entradas)
    render_multiple_text_areas(
        label="APIs/Serviços Necessários",
        key_prefix="api",
        state_key="apis_servicos",
        placeholder="Ex: API do Google OAuth 2.0, Firebase Authentication..."
    )

    # Campo 4: Subseções de objetivos (direto, sem header principal)

    # Subseção: Como
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Como:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_como = st.text_area(
        "Como",
        value=st.session_state.objetivo_como,
        placeholder="Descreva o contexto ou papel do usuário...",
        label_visibility="collapsed",
        height=80,
        key="obj_como"
    )

    # Subseção: Quero
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Quero:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_quero = st.text_area(
        "Quero",
        value=st.session_state.objetivo_quero,
        placeholder="Descreva o que o usuário deseja fazer...",
        label_visibility="collapsed",
        height=80,
        key="obj_quero"
    )

    # Subseção: Para que
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Para que:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_para_que = st.text_area(
        "Para que",
        value=st.session_state.objetivo_para_que,
        placeholder="Descreva o benefício ou objetivo final...",
        label_visibility="collapsed",
        height=80,
        key="obj_para_que"
    )
    st.markdown("---")

    # Campo 5: Complexidade (único)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Complexidade Estimada (pontos)</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.complexidade = st.number_input(
        "Complexidade",
        min_value=1,
        max_value=21,
        value=st.session_state.complexidade,
        step=1,
        help="Defina a complexidade da tarefa (1 a 21 pontos)",
        label_visibility="collapsed"
    )
    st.caption("Defina a complexidade da tarefa (1 a 21 pontos)")
    st.markdown("---")

    # Campo 6: Critérios de Aceitação (múltiplas entradas)
    render_multiple_text_areas(
        label="Critérios de Aceitação",
        key_prefix="criterio",
        state_key="criterios_aceitacao",
        placeholder="Descreva um critério de aceitação..."
    )

    # Pergunta sobre API (dentro dos critérios de aceitação)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Esta tarefa envolve desenvolvimento de API?</strong>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.is_api = st.checkbox(
        "Sim, esta tarefa envolve desenvolvimento de API",
        value=st.session_state.is_api,
        key="is_api_checkbox"
    )

    # Se for API, mostrar campos específicos
    if st.session_state.is_api:
        st.markdown("<br>", unsafe_allow_html=True)

        # Seleção de Método HTTP
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Método HTTP</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.api_metodo = st.selectbox(
            "Método",
            options=["GET", "POST", "PUT", "PATCH", "DELETE"],
            index=["GET", "POST", "PUT", "PATCH", "DELETE"].index(st.session_state.api_metodo),
            label_visibility="collapsed",
            key="api_metodo_select"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Endpoint da API (sempre mostra)
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Endpoint da API</strong>
            </div>
        """, unsafe_allow_html=True)

        # Placeholder dinâmico baseado no método
        endpoint_placeholders = {
            "GET": "Ex: /api/v1/usuarios",
            "POST": "Ex: /api/v1/usuarios",
            "PUT": "Ex: /api/v1/usuarios/{id}",
            "PATCH": "Ex: /api/v1/usuarios/{id}",
            "DELETE": "Ex: /api/v1/usuarios/{id}"
        }

        st.session_state.api_endpoint = st.text_input(
            "Endpoint",
            value=st.session_state.api_endpoint,
            placeholder=endpoint_placeholders.get(st.session_state.api_metodo, "Ex: /api/v1/recurso"),
            label_visibility="collapsed",
            key="api_endpoint_input"
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # Campos dinâmicos baseados no método HTTP
        metodo = st.session_state.api_metodo

        # GET: Parâmetros de Consulta (Query Params)
        if metodo == "GET":
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Parâmetros de Consulta (Query Params)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Filtros, paginação e ordenação passados na URL")
            st.session_state.api_query_params = st.text_area(
                "Query Params",
                value=st.session_state.api_query_params,
                placeholder="Ex: status=ativo&limit=10&page=1",
                label_visibility="collapsed",
                height=100,
                key="api_query_params_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        # POST: Corpo da Requisição (Body)
        elif metodo == "POST":
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Corpo da Requisição (Body)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Objeto JSON com os dados que serão enviados para criação")
            st.session_state.api_body = st.text_area(
                "Body",
                value=st.session_state.api_body,
                placeholder='Ex: {\n  "nome": "João",\n  "email": "joao@email.com"\n}',
                label_visibility="collapsed",
                height=120,
                key="api_body_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        # PUT: Parâmetro de Rota + Corpo da Requisição
        elif metodo == "PUT":
            # Parâmetro de Rota
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Parâmetro de Rota (Path Param)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Identificador do recurso a ser substituído")
            st.session_state.api_path_param = st.text_input(
                "Path Param",
                value=st.session_state.api_path_param,
                placeholder="Ex: id (UUID ou número)",
                label_visibility="collapsed",
                key="api_path_param_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

            # Corpo da Requisição
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Corpo da Requisição (Body)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Objeto JSON completo que substituirá o recurso existente")
            st.session_state.api_body = st.text_area(
                "Body",
                value=st.session_state.api_body,
                placeholder='Ex: {\n  "nome": "João Silva",\n  "email": "joao@email.com",\n  "status": "ativo"\n}',
                label_visibility="collapsed",
                height=120,
                key="api_body_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        # PATCH: Parâmetro de Rota + Corpo da Requisição (parcial)
        elif metodo == "PATCH":
            # Parâmetro de Rota
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Parâmetro de Rota (Path Param)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Identificador do recurso a ser alterado")
            st.session_state.api_path_param = st.text_input(
                "Path Param",
                value=st.session_state.api_path_param,
                placeholder="Ex: id (UUID ou número)",
                label_visibility="collapsed",
                key="api_path_param_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

            # Corpo da Requisição
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Corpo da Requisição (Body)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Objeto JSON contendo apenas os campos que serão modificados")
            st.session_state.api_body = st.text_area(
                "Body",
                value=st.session_state.api_body,
                placeholder='Ex: {\n  "status": "inativo"\n}',
                label_visibility="collapsed",
                height=100,
                key="api_body_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        # DELETE: Parâmetro de Rota
        elif metodo == "DELETE":
            st.markdown("""
                <div style="
                    background-color: rgba(139, 92, 246, 0.08);
                    border-left: 3px solid #8B5CF6;
                    padding: 0.5rem 0.75rem;
                    border-radius: 6px;
                    margin-bottom: 0.5rem;
                ">
                    <strong style="color: #E0E0E0; font-size: 0.95rem;">Parâmetro de Rota (Path Param)</strong>
                </div>
            """, unsafe_allow_html=True)
            st.caption("Identificador do recurso a ser excluído")
            st.session_state.api_path_param = st.text_input(
                "Path Param",
                value=st.session_state.api_path_param,
                placeholder="Ex: id (UUID ou número)",
                label_visibility="collapsed",
                key="api_path_param_input"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        # Formato da Resposta (sempre mostra)
        st.markdown("""
            <div style="
                background-color: rgba(139, 92, 246, 0.08);
                border-left: 3px solid #8B5CF6;
                padding: 0.5rem 0.75rem;
                border-radius: 6px;
                margin-bottom: 0.5rem;
            ">
                <strong style="color: #E0E0E0; font-size: 0.95rem;">Formato da Resposta</strong>
            </div>
        """, unsafe_allow_html=True)
        st.caption("A resposta da API deve ser retornada no formato JSON, contendo:")
        st.session_state.api_formato_resposta = st.text_area(
            "Formato Resposta",
            value=st.session_state.api_formato_resposta,
            placeholder='Ex: {\n  "sucesso": true,\n  "mensagem": "Operação realizada com sucesso"\n}',
            label_visibility="collapsed",
            height=120,
            key="api_formato_input"
        )

    st.markdown("---")

    # Campo de Dependências
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Possui dependências de outras equipes/sistemas?</strong>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.has_dependencies = st.checkbox(
        "Sim, possui dependências",
        value=st.session_state.has_dependencies,
        key="has_dependencies_checkbox"
    )

    if st.session_state.has_dependencies:
        st.session_state.dependencies = st.text_area(
            "Dependências",
            value=st.session_state.dependencies,
            placeholder="Descreva as dependências (ex: API do time de Pagamentos, Aprovação do time de Segurança, Deploy do serviço X...)",
            label_visibility="collapsed",
            height=100,
            key="dependencies_input"
        )

    st.markdown("---")

    # Exibir erros de validação (se houver)
    if st.session_state.validation_errors:
        st.error("**Erros de validação:**")
        for error in st.session_state.validation_errors:
            st.markdown(f"- {error}")
        st.markdown("---")

    # Botão de submissão
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_button = st.button(
            "Gerar Historia",
            type="primary",
            use_container_width=True
        )

    # Processar submissão
    if submit_button:
        # Validar formulário
        is_valid, errors = validate_form(
            titulo=st.session_state.titulo,
            regras_negocio=st.session_state.regras_negocio,
            apis_servicos=st.session_state.apis_servicos,
            objetivos=st.session_state.objetivos,
            complexidade=st.session_state.complexidade,
            criterios_aceitacao=st.session_state.criterios_aceitacao
        )

        if not is_valid:
            st.session_state.validation_errors = errors
            st.rerun()
        else:
            st.session_state.validation_errors = []

            # Retornar dados limpos
            objetivos_dict = {
                "como": st.session_state.objetivo_como.strip(),
                "quero": st.session_state.objetivo_quero.strip(),
                "para_que": st.session_state.objetivo_para_que.strip()
            }

            form_data = {
                "value_area": st.session_state.value_area,
                "titulo": st.session_state.titulo.strip(),
                "regras_negocio": [r.strip() for r in st.session_state.regras_negocio if r.strip()],
                "apis_servicos": [a.strip() for a in st.session_state.apis_servicos if a.strip()],
                "objetivos": objetivos_dict,
                "complexidade": st.session_state.complexidade,
                "criterios_aceitacao": [c.strip() for c in st.session_state.criterios_aceitacao if c.strip()],
                "is_api": st.session_state.is_api,
                "has_dependencies": st.session_state.has_dependencies,
                "dependencies": st.session_state.dependencies.strip() if st.session_state.has_dependencies else ""
            }

            # Adicionar dados da API se aplicável
            if st.session_state.is_api:
                api_specs = {
                    "metodo": st.session_state.api_metodo,
                    "endpoint": st.session_state.api_endpoint.strip(),
                    "formato_resposta": st.session_state.api_formato_resposta.strip()
                }

                # Adicionar campos específicos baseados no método HTTP
                metodo = st.session_state.api_metodo

                if metodo == "GET":
                    api_specs["query_params"] = st.session_state.api_query_params.strip()
                elif metodo == "POST":
                    api_specs["body"] = st.session_state.api_body.strip()
                elif metodo in ["PUT", "PATCH"]:
                    api_specs["path_param"] = st.session_state.api_path_param.strip()
                    api_specs["body"] = st.session_state.api_body.strip()
                elif metodo == "DELETE":
                    api_specs["path_param"] = st.session_state.api_path_param.strip()

                form_data["api_specs"] = api_specs

            return form_data

    return None


def reset_form():
    """
    Reseta o formulário para os valores iniciais.
    Útil após gerar uma história com sucesso.
    """
    st.session_state.value_area = "Business"
    st.session_state.titulo = ""
    st.session_state.regras_negocio = [""]
    st.session_state.apis_servicos = [""]
    st.session_state.complexidade = 5
    st.session_state.criterios_aceitacao = [""]
    st.session_state.validation_errors = []

    # Resetar campos de Objetivos
    st.session_state.objetivo_como = ""
    st.session_state.objetivo_quero = ""
    st.session_state.objetivo_para_que = ""

    # Resetar campos da API
    st.session_state.is_api = False
    st.session_state.api_metodo = "GET"
    st.session_state.api_endpoint = ""
    st.session_state.api_query_params = ""
    st.session_state.api_path_param = ""
    st.session_state.api_body = ""
    st.session_state.api_formato_resposta = ""

    # Resetar dependências
    st.session_state.has_dependencies = False
    st.session_state.dependencies = ""

    # Resetar campos Spike
    st.session_state.spike_pergunta = ""
    st.session_state.spike_alternativas = [""]
    st.session_state.spike_timebox = 8
    st.session_state.spike_output = "Documento de decisão"
    st.session_state.spike_criterios_sucesso = [""]

    # Resetar campos Kaizen
    st.session_state.kaizen_processo = ""
    st.session_state.kaizen_situacao_atual = ""
    st.session_state.kaizen_meta = ""
    st.session_state.kaizen_metricas = [""]
    st.session_state.kaizen_impacto = ""

    # Resetar campos Fix
    st.session_state.fix_descricao = ""
    st.session_state.fix_passos_reproduzir = [""]
    st.session_state.fix_comportamento_esperado = ""
    st.session_state.fix_comportamento_atual = ""
    st.session_state.fix_ambiente = "Produção"
    st.session_state.fix_severidade = "Média"
    st.session_state.fix_logs = ""


def _render_spike_form() -> Dict[str, Any]:
    """Renderiza formulário para histórias Spike (exploratórias)."""

    # Título
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Título da Investigação</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.titulo = st.text_input(
        "Título",
        value=st.session_state.titulo,
        max_chars=100,
        placeholder="Ex: Spike - Avaliar viabilidade de migração para GraphQL",
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Campos de Objetivos (Como/Quero/Para que)
    st.markdown("""
        <div style="
            background-color: rgba(236, 72, 153, 0.1);
            border-left: 4px solid #EC4899;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Objetivos (Como/Quero/Para que)</strong>
        </div>
    """, unsafe_allow_html=True)

    # Subseção: Como
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Como:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_como = st.text_area(
        "Como",
        value=st.session_state.objetivo_como,
        placeholder="Ex: Como arquiteto de software...",
        label_visibility="collapsed",
        height=60,
        key="spike_obj_como"
    )

    # Subseção: Quero
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Quero:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_quero = st.text_area(
        "Quero",
        value=st.session_state.objetivo_quero,
        placeholder="Ex: Quero investigar a viabilidade de migração para GraphQL...",
        label_visibility="collapsed",
        height=60,
        key="spike_obj_quero"
    )

    # Subseção: Para que
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Para que:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_para_que = st.text_area(
        "Para que",
        value=st.session_state.objetivo_para_que,
        placeholder="Ex: Para que possamos tomar uma decisão informada sobre a arquitetura...",
        label_visibility="collapsed",
        height=60,
        key="spike_obj_para_que"
    )
    st.markdown("---")

    # Pergunta/Hipótese a validar
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Pergunta/Hipótese a Validar</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.spike_pergunta = st.text_area(
        "Pergunta",
        value=st.session_state.spike_pergunta,
        placeholder="Ex: É viável migrar nossa API REST para GraphQL sem impactar os clientes existentes?",
        label_visibility="collapsed",
        height=100
    )
    st.markdown("---")

    # Alternativas a investigar
    render_multiple_text_areas(
        label="Alternativas/Tecnologias a Investigar",
        key_prefix="spike_alt",
        state_key="spike_alternativas",
        placeholder="Ex: Apollo Server, Hasura, AWS AppSync..."
    )


    # Output esperado
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Output Esperado</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.spike_output = st.selectbox(
        "Output",
        options=["Documento de decisão", "POC funcional", "Relatório técnico", "Apresentação para o time", "Outro"],
        index=["Documento de decisão", "POC funcional", "Relatório técnico", "Apresentação para o time", "Outro"].index(st.session_state.spike_output),
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Critérios de sucesso
    render_multiple_text_areas(
        label="Critérios de Sucesso da Investigação",
        key_prefix="spike_crit",
        state_key="spike_criterios_sucesso",
        placeholder="Ex: Identificar se a solução atende aos requisitos de performance..."
    )

    # Botão de submissão
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_button = st.button(
            "Gerar Historia Spike",
            type="primary",
            use_container_width=True
        )

    if submit_button:
        if not st.session_state.titulo.strip():
            st.error("Título é obrigatório")
            return None
        if not st.session_state.spike_pergunta.strip():
            st.error("Pergunta/Hipótese é obrigatória")
            return None

        objetivos_dict = {
            "como": st.session_state.objetivo_como.strip(),
            "quero": st.session_state.objetivo_quero.strip(),
            "para_que": st.session_state.objetivo_para_que.strip()
        }

        form_data = {
            "value_area": "Spike",
            "titulo": st.session_state.titulo.strip(),
            "objetivos": objetivos_dict,
            "spike_pergunta": st.session_state.spike_pergunta.strip(),
            "spike_alternativas": [a.strip() for a in st.session_state.spike_alternativas if a.strip()],
            "spike_output": st.session_state.spike_output,
            "spike_criterios_sucesso": [c.strip() for c in st.session_state.spike_criterios_sucesso if c.strip()]
        }
        return form_data

    return None


def _render_kaizen_form() -> Dict[str, Any]:
    """Renderiza formulário para histórias Kaizen (melhoria contínua)."""

    # Título
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Título da Melhoria</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.titulo = st.text_input(
        "Título",
        value=st.session_state.titulo,
        max_chars=100,
        placeholder="Ex: Kaizen - Reduzir tempo de deploy em 50%",
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Campos de Objetivos (Como/Quero/Para que)
    st.markdown("""
        <div style="
            background-color: rgba(236, 72, 153, 0.1);
            border-left: 4px solid #EC4899;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Objetivos (Como/Quero/Para que)</strong>
        </div>
    """, unsafe_allow_html=True)

    # Subseção: Como
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Como:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_como = st.text_area(
        "Como",
        value=st.session_state.objetivo_como,
        placeholder="Ex: Como time de desenvolvimento...",
        label_visibility="collapsed",
        height=60,
        key="kaizen_obj_como"
    )

    # Subseção: Quero
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Quero:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_quero = st.text_area(
        "Quero",
        value=st.session_state.objetivo_quero,
        placeholder="Ex: Quero reduzir o tempo de deploy em 50%...",
        label_visibility="collapsed",
        height=60,
        key="kaizen_obj_quero"
    )

    # Subseção: Para que
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Para que:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_para_que = st.text_area(
        "Para que",
        value=st.session_state.objetivo_para_que,
        placeholder="Ex: Para que possamos entregar mais valor com menos tempo de espera...",
        label_visibility="collapsed",
        height=60,
        key="kaizen_obj_para_que"
    )
    st.markdown("---")

    # Processo/Área a melhorar
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Processo/Área a Melhorar</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.kaizen_processo = st.text_area(
        "Processo",
        value=st.session_state.kaizen_processo,
        placeholder="Ex: Pipeline de CI/CD, processo de code review, fluxo de testes...",
        label_visibility="collapsed",
        height=80
    )
    st.markdown("---")

    # Situação atual (baseline)
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Situação Atual (Baseline)</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.kaizen_situacao_atual = st.text_area(
        "Situação Atual",
        value=st.session_state.kaizen_situacao_atual,
        placeholder="Ex: Deploy atual leva em média 45 minutos, com falhas em 20% das vezes...",
        label_visibility="collapsed",
        height=100
    )
    st.markdown("---")

    # Meta desejada
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Meta Desejada</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.kaizen_meta = st.text_area(
        "Meta",
        value=st.session_state.kaizen_meta,
        placeholder="Ex: Reduzir tempo de deploy para 20 minutos com taxa de falha < 5%...",
        label_visibility="collapsed",
        height=80
    )
    st.markdown("---")

    # Métricas de sucesso
    render_multiple_text_areas(
        label="Métricas de Sucesso",
        key_prefix="kaizen_met",
        state_key="kaizen_metricas",
        placeholder="Ex: Tempo médio de deploy, taxa de falha, satisfação do time..."
    )

    # Impacto esperado
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Impacto Esperado no Time/Processo</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.kaizen_impacto = st.text_area(
        "Impacto",
        value=st.session_state.kaizen_impacto,
        placeholder="Ex: Mais tempo para desenvolvimento, menos retrabalho, maior confiança no processo...",
        label_visibility="collapsed",
        height=80
    )
    st.markdown("---")

    # Complexidade
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Complexidade Estimada (pontos)</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.complexidade = st.number_input(
        "Complexidade",
        min_value=1,
        max_value=21,
        value=st.session_state.complexidade,
        step=1,
        label_visibility="collapsed",
        key="kaizen_complexidade"
    )
    st.markdown("---")

    # Botão de submissão
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_button = st.button(
            "Gerar Historia Kaizen",
            type="primary",
            use_container_width=True
        )

    if submit_button:
        if not st.session_state.titulo.strip():
            st.error("Título é obrigatório")
            return None
        if not st.session_state.kaizen_processo.strip():
            st.error("Processo/Área é obrigatório")
            return None

        objetivos_dict = {
            "como": st.session_state.objetivo_como.strip(),
            "quero": st.session_state.objetivo_quero.strip(),
            "para_que": st.session_state.objetivo_para_que.strip()
        }

        form_data = {
            "value_area": "Kaizen",
            "titulo": st.session_state.titulo.strip(),
            "objetivos": objetivos_dict,
            "kaizen_processo": st.session_state.kaizen_processo.strip(),
            "kaizen_situacao_atual": st.session_state.kaizen_situacao_atual.strip(),
            "kaizen_meta": st.session_state.kaizen_meta.strip(),
            "kaizen_metricas": [m.strip() for m in st.session_state.kaizen_metricas if m.strip()],
            "kaizen_impacto": st.session_state.kaizen_impacto.strip(),
            "complexidade": st.session_state.complexidade
        }
        return form_data

    return None


def _render_fix_form() -> Dict[str, Any]:
    """Renderiza formulário para histórias Fix/Bug/Incidente."""

    # Título
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Título do Bug/Incidente</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.titulo = st.text_input(
        "Título",
        value=st.session_state.titulo,
        max_chars=100,
        placeholder="Ex: Fix - Erro 500 ao processar pagamentos com cartão internacional",
        label_visibility="collapsed"
    )
    st.markdown("---")

    # Campos de Objetivos (Como/Quero/Para que)
    st.markdown("""
        <div style="
            background-color: rgba(236, 72, 153, 0.1);
            border-left: 4px solid #EC4899;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Objetivos (Como/Quero/Para que)</strong>
        </div>
    """, unsafe_allow_html=True)

    # Subseção: Como
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Como:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_como = st.text_area(
        "Como",
        value=st.session_state.objetivo_como,
        placeholder="Ex: Como usuário do sistema...",
        label_visibility="collapsed",
        height=60,
        key="fix_obj_como"
    )

    # Subseção: Quero
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Quero:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_quero = st.text_area(
        "Quero",
        value=st.session_state.objetivo_quero,
        placeholder="Ex: Quero que o bug seja corrigido...",
        label_visibility="collapsed",
        height=60,
        key="fix_obj_quero"
    )

    # Subseção: Para que
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Para que:</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.objetivo_para_que = st.text_area(
        "Para que",
        value=st.session_state.objetivo_para_que,
        placeholder="Ex: Para que eu possa realizar pagamentos sem erros...",
        label_visibility="collapsed",
        height=60,
        key="fix_obj_para_que"
    )
    st.markdown("---")

    # Descrição do bug
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Descrição do Bug/Erro</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.fix_descricao = st.text_area(
        "Descrição",
        value=st.session_state.fix_descricao,
        placeholder="Descreva o bug/erro de forma clara e objetiva...",
        label_visibility="collapsed",
        height=100
    )
    st.markdown("---")

    # Passos para reproduzir
    render_multiple_text_areas(
        label="Passos para Reproduzir",
        key_prefix="fix_passos",
        state_key="fix_passos_reproduzir",
        placeholder="Ex: 1. Acessar tela de pagamento, 2. Selecionar cartão internacional..."
    )

    # Comportamento esperado
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Comportamento Esperado</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.fix_comportamento_esperado = st.text_area(
        "Esperado",
        value=st.session_state.fix_comportamento_esperado,
        placeholder="Ex: O pagamento deveria ser processado com sucesso e exibir confirmação...",
        label_visibility="collapsed",
        height=80
    )
    st.markdown("---")

    # Comportamento atual
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Comportamento Atual (O que está acontecendo)</strong>
            <span style="color: #EC4899; margin-left: 0.25rem;">*</span>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.fix_comportamento_atual = st.text_area(
        "Atual",
        value=st.session_state.fix_comportamento_atual,
        placeholder="Ex: Retorna erro 500 Internal Server Error e o pagamento não é processado...",
        label_visibility="collapsed",
        height=80
    )
    st.markdown("---")

    # Ambiente e Severidade em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="
                background-color: rgba(99, 102, 241, 0.1);
                border-left: 4px solid #6366F1;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                margin-bottom: 0.75rem;
            ">
                <strong style="color: #FFFFFF; font-size: 1.05rem;">Ambiente Afetado</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.fix_ambiente = st.selectbox(
            "Ambiente",
            options=["Produção", "Homologação", "Desenvolvimento", "Todos"],
            index=["Produção", "Homologação", "Desenvolvimento", "Todos"].index(st.session_state.fix_ambiente),
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("""
            <div style="
                background-color: rgba(99, 102, 241, 0.1);
                border-left: 4px solid #6366F1;
                padding: 0.75rem 1rem;
                border-radius: 8px;
                margin-bottom: 0.75rem;
            ">
                <strong style="color: #FFFFFF; font-size: 1.05rem;">Severidade</strong>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.fix_severidade = st.selectbox(
            "Severidade",
            options=["Crítica", "Alta", "Média", "Baixa"],
            index=["Crítica", "Alta", "Média", "Baixa"].index(st.session_state.fix_severidade),
            label_visibility="collapsed"
        )

    st.markdown("---")

    # Logs/Screenshots
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Logs/Evidências (opcional)</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.fix_logs = st.text_area(
        "Logs",
        value=st.session_state.fix_logs,
        placeholder="Cole aqui logs de erro, stack traces ou descreva evidências...",
        label_visibility="collapsed",
        height=120
    )

    # Upload de imagens/prints
    st.markdown("""
        <div style="
            background-color: rgba(139, 92, 246, 0.08);
            border-left: 3px solid #8B5CF6;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            margin: 0.75rem 0;
        ">
            <strong style="color: #E0E0E0; font-size: 0.95rem;">Prints/Imagens (opcional)</strong>
        </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Envie prints ou imagens do erro",
        type=["png", "jpg", "jpeg", "gif", "webp"],
        accept_multiple_files=True,
        key="fix_images_uploader",
        label_visibility="collapsed"
    )

    # Mostrar preview das imagens enviadas
    if uploaded_files:
        st.caption(f"{len(uploaded_files)} imagem(ns) anexada(s)")
        cols = st.columns(min(len(uploaded_files), 3))
        for i, file in enumerate(uploaded_files):
            with cols[i % 3]:
                st.image(file, caption=file.name, use_container_width=True)

    # Armazenar referência dos arquivos no session_state
    if 'fix_images' not in st.session_state:
        st.session_state.fix_images = []
    st.session_state.fix_images = uploaded_files if uploaded_files else []

    st.markdown("---")

    # Complexidade
    st.markdown("""
        <div style="
            background-color: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        ">
            <strong style="color: #FFFFFF; font-size: 1.05rem;">Complexidade Estimada (pontos)</strong>
        </div>
    """, unsafe_allow_html=True)
    st.session_state.complexidade = st.number_input(
        "Complexidade",
        min_value=1,
        max_value=21,
        value=st.session_state.complexidade,
        step=1,
        label_visibility="collapsed",
        key="fix_complexidade"
    )
    st.markdown("---")

    # Botão de submissão
    col1, col2, col3 = st.columns([2, 2, 2])
    with col2:
        submit_button = st.button(
            "Gerar Historia Fix",
            type="primary",
            use_container_width=True
        )

    if submit_button:
        if not st.session_state.titulo.strip():
            st.error("Título é obrigatório")
            return None
        if not st.session_state.fix_descricao.strip():
            st.error("Descrição do bug é obrigatória")
            return None

        # Processar imagens para envio (converter para base64)
        fix_images_data = []
        if st.session_state.fix_images:
            import base64
            for img_file in st.session_state.fix_images:
                try:
                    # Ler bytes da imagem
                    img_bytes = img_file.getvalue()
                    # Converter para base64
                    img_base64 = base64.standard_b64encode(img_bytes).decode("utf-8")
                    # Determinar media type
                    file_type = img_file.type if img_file.type else "image/png"
                    fix_images_data.append({
                        "name": img_file.name,
                        "type": file_type,
                        "data": img_base64
                    })
                except Exception as e:
                    st.warning(f"Erro ao processar imagem {img_file.name}: {str(e)}")

        objetivos_dict = {
            "como": st.session_state.objetivo_como.strip(),
            "quero": st.session_state.objetivo_quero.strip(),
            "para_que": st.session_state.objetivo_para_que.strip()
        }

        form_data = {
            "value_area": "Fix/Bug/Incidente",
            "titulo": st.session_state.titulo.strip(),
            "objetivos": objetivos_dict,
            "fix_descricao": st.session_state.fix_descricao.strip(),
            "fix_passos_reproduzir": [p.strip() for p in st.session_state.fix_passos_reproduzir if p.strip()],
            "fix_comportamento_esperado": st.session_state.fix_comportamento_esperado.strip(),
            "fix_comportamento_atual": st.session_state.fix_comportamento_atual.strip(),
            "fix_ambiente": st.session_state.fix_ambiente,
            "fix_severidade": st.session_state.fix_severidade,
            "fix_logs": st.session_state.fix_logs.strip(),
            "fix_images": fix_images_data,
            "complexidade": st.session_state.complexidade
        }
        return form_data

    return None
