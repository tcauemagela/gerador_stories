"""
Entry point da aplicação Streamlit.
Responsável por inicialização, configuração e routing principal.
Integra ETAPA 1 (Criação) + ETAPA 2 (Edição/Refinamento).
"""

import streamlit as st
import config
from services.ai_service import AIService
from controllers.story_controller import StoryController
from controllers.editor_controller import EditorController
from views import story_form_view, story_display_view
from views import editor_view, suggestions_view, version_view
from views import story_list_view, export_view
from utils.formatters import format_error_message
from models.story import Story
from services.invest_service import InvestService


def initialize_app():
    """
    Inicializa configurações da aplicação Streamlit.
    """
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.APP_LAYOUT,
        initial_sidebar_state="collapsed"
    )

    # Adicionar Font Awesome para ícones modernos
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    """, unsafe_allow_html=True)

    # CSS customizado com paleta de cores moderna
    st.markdown("""
        <style>
        /* Dark Mode Global */
        .stApp {
            background-color: #0E1117;
        }

        /* Cores principais */
        :root {
            --primary-color: #6366F1;
            --secondary-color: #8B5CF6;
            --accent-color: #EC4899;
            --bg-dark: #1A1D29;
            --bg-card: #242837;
            --text-primary: #FFFFFF;
            --text-secondary: #B4B4B4;
        }

        /* Animações */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideIn {
            from { transform: translateX(-30px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        /* Header principal */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
            animation: fadeIn 0.8s ease-out;
        }

        .main-header h1 {
            color: white;
            font-size: 2.8rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }

        .main-header p {
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.1rem;
            margin-top: 0.5rem;
        }

        /* Cards de métricas */
        .metric-card {
            background: var(--bg-card);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            border-left: 5px solid var(--primary-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideIn 0.6s ease-out;
        }

        .metric-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 40px rgba(99, 102, 241, 0.3);
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            background-color: var(--bg-card);
            padding: 1rem;
            border-radius: 16px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .stTabs [data-baseweb="tab"] {
            height: 55px;
            background-color: var(--bg-dark);
            border-radius: 12px;
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 1rem;
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #2A2D3A;
            transform: translateY(-2px);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
            width: 100%;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.5);
        }

        .stDownloadButton > button {
            background: linear-gradient(135deg, #242837 0%, #1A1D29 100%);
            color: #FFFFFF;
            border: 2px solid rgba(99, 102, 241, 0.4);
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
            width: 100%;
        }

        .stDownloadButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
            border-color: rgba(99, 102, 241, 0.6);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1A1D29 0%, #242837 100%);
        }

        /* Content containers */
        .content-card {
            background: var(--bg-card);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            margin: 1rem 0;
        }

        /* Override Streamlit defaults - Cores específicas */
        /* Labels e títulos em branco */
        .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
            color: #FFFFFF !important;
            font-weight: 500;
        }

        /* Conteúdo de markdown da história - BRANCO */
        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: #FFFFFF !important;
        }

        /* Cabeçalhos do markdown em branco */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #FFFFFF !important;
        }

        /* Blocos de código inline */
        .stMarkdown code {
            color: #10B981 !important;  /* Verde claro */
            background-color: #1E293B !important;  /* Fundo escuro */
            padding: 2px 6px;
            border-radius: 4px;
        }

        /* Blocos de código pre-formatado (como JSON) */
        .stMarkdown pre {
            background-color: #1E293B !important;  /* Fundo escuro */
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 1rem;
        }

        .stMarkdown pre code {
            color: #10B981 !important;  /* Verde claro para código */
            background-color: transparent !important;
        }

        /* Selectbox dropdown text */
        .stSelectbox div[data-baseweb="select"] > div {
            color: #FFFFFF !important;
        }

        /* Placeholder text */
        ::placeholder {
            color: #B0B0B0 !important;
        }

        /* Caption text - verde claro para visibilidade */
        .stCaptionContainer, [data-testid="stCaptionContainer"],
        .st-emotion-cache-1n76uvr, .st-emotion-cache-1y4p8pa,
        [class*="caption"] {
            color: #A0D9B4 !important;
        }

        /* Força caption (small) do streamlit */
        small {
            color: #A0D9B4 !important;
        }

        /* Text inputs */
        .stTextInput > div > div > input {
            background-color: var(--bg-dark);
            color: #FFFFFF !important;
            border-radius: 8px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: border-color 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border: 1px solid rgba(16, 185, 129, 0.6);
            outline: none;
        }

        .stTextInput > div > div > input:not(:placeholder-shown) {
            border: 1px solid rgba(16, 185, 129, 0.5);
        }

        /* Text areas */
        .stTextArea > div > div > textarea {
            background-color: var(--bg-dark);
            color: #FFFFFF !important;
            border-radius: 8px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: border-color 0.3s ease;
        }

        .stTextArea > div > div > textarea:focus {
            border: 1px solid rgba(16, 185, 129, 0.6);
            outline: none;
        }

        .stTextArea > div > div > textarea:not(:placeholder-shown) {
            border: 1px solid rgba(16, 185, 129, 0.5);
        }

        /* Selectbox */
        .stSelectbox > div > div {
            background-color: var(--bg-dark);
            color: #FFFFFF !important;
            border-radius: 8px;
        }

        /* Number input */
        .stNumberInput > div > div > input {
            background-color: var(--bg-dark);
            color: #FFFFFF !important;
            border-radius: 8px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            transition: border-color 0.3s ease;
        }

        .stNumberInput > div > div > input:focus {
            border: 1px solid rgba(16, 185, 129, 0.6);
            outline: none;
        }

        /* Info boxes text - verde claro para visibilidade */
        .stAlert p, .stInfo p, .stWarning p {
            color: #FFFFFF !important;
        }

        /* Expander */
        .streamlit-expanderHeader {
            background-color: var(--bg-card);
            color: var(--text-primary);
            border-radius: 12px;
        }

        /* Section headers */
        h1, h2, h3, h4 {
            color: var(--text-primary) !important;
        }

        /* Info/Warning/Success boxes */
        .stAlert {
            border-radius: 12px;
        }

        /* Texto geral em containers - verde claro para boa visibilidade */
        [data-testid="stVerticalBlock"] > div > div > p,
        [data-testid="stVerticalBlock"] > div > div > span {
            color: #A7F3D0 !important;
        }

        /* Checkboxes e outros componentes interativos */
        .stCheckbox label {
            color: #D1FAE5 !important;
        }

        /* Success/Info/Warning messages */
        .stSuccess, .stInfo, .stWarning {
            color: #FFFFFF !important;
        }

        /* Texto dentro de colunas */
        [data-testid="column"] p, [data-testid="column"] span {
            color: #A7F3D0 !important;
        }
        </style>
        """, unsafe_allow_html=True)


def initialize_services():
    """
    Inicializa services necessários (AI Service, Controllers).
    Usa cache para evitar reinicialização desnecessária.

    Returns:
        Tupla (AIService, StoryController, EditorController)
    """
    # Obter API key
    api_key = config.get_api_key()

    # Criar AI Service
    ai_service = AIService(api_key=api_key)

    # Criar Controllers
    story_controller = StoryController(ai_service=ai_service)
    editor_controller = EditorController(ai_service=ai_service)

    return ai_service, story_controller, editor_controller


def main():
    """
    Função principal da aplicação.
    Implementa navegação por tabs integrando ETAPA 1 e ETAPA 2.
    """
    # Inicializar app
    initialize_app()

    # Título principal com gradiente e autor
    st.markdown(f"""
        <div class="main-header">
            <h1>{config.APP_TITLE}</h1>
            <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.9;">
                <i class="fas fa-code" style="margin-right: 8px;"></i>Desenvolvido por {config.APP_AUTHOR}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Banner de aviso sobre persistência de dados (ETAPA 3)
    st.markdown("""
        <div style="
            background-color: rgba(255, 193, 7, 0.1);
            border-left: 4px solid #FFC107;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <p style="margin: 0; color: #FFC107;">
                <i class="fas fa-exclamation-triangle" style="margin-right: 8px;"></i>
                <strong>Aviso:</strong> Suas histórias são armazenadas apenas na sessão atual do navegador.
                Ao fechar o navegador ou recarregar a página, todos os dados serão perdidos.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Inicializar services
    try:
        ai_service, story_controller, editor_controller = initialize_services()
    except Exception as e:
        st.error(f"Erro ao inicializar aplicação: {str(e)}")
        st.stop()

    # Gerenciar estado da aplicação
    if 'current_story' not in st.session_state:
        st.session_state.current_story = None

    # Sistema de navegação por tabs (ETAPA 3: 5 tabs)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Criar Historia",
        "✏️ Editar",
        "📋 Versoes",
        "📚 Minhas Historias",
        "💾 Exportar"
    ])

    # TAB 1: Criar História (ETAPA 1)
    with tab1:
        _render_create_story_tab(story_controller, editor_controller)

    # TAB 2: Editar (ETAPA 2)
    with tab2:
        _render_edit_tab(editor_controller)

    # TAB 3: Versões (ETAPA 2)
    with tab3:
        _render_versions_tab(editor_controller)

    # TAB 4: Minhas Histórias (ETAPA 3)
    with tab4:
        story_list_view.render_story_list()

    # TAB 5: Exportar (ETAPA 3)
    with tab5:
        export_view.render_export_options()


def _render_create_story_tab(story_controller: StoryController, editor_controller: EditorController):
    """
    Renderiza tab de criação de história (ETAPA 1).

    Args:
        story_controller: Controller de histórias
        editor_controller: Controller de edição
    """
    if st.session_state.current_story is None:
        # Mostrar formulário
        st.info("Preencha o formulario abaixo para gerar uma nova historia")

        form_data = story_form_view.render_form()

        # Se formulário foi submetido
        if form_data is not None:
            # Salvar form_data para regeneração posterior
            st.session_state.form_data = form_data

            # Exibir loading
            with st.spinner("Gerando historia..."):
                st.info("Isso pode levar ate 30 segundos...")

                # Criar história via controller
                story, error_type = story_controller.create_story(form_data)

                if story is not None:
                    # Sucesso - converter Story para dict e armazenar
                    story_dict = story.to_dict()
                    st.session_state.current_story = story_dict

                    # IMPORTANTE: Inicializar primeira versão (ETAPA 2)
                    editor_controller.initialize_first_version(story_dict)

                    # Marcar que história foi gerada com sucesso
                    st.session_state.story_generated_success = True

                    st.rerun()
                else:
                    # Erro - exibir mensagem apropriada
                    error_info = format_error_message(error_type)
                    story_display_view.show_error(
                        error_message=error_info["message"],
                        error_type=error_type
                    )
    else:
        # Verificar se história foi gerada com sucesso (mostrar mensagem)
        if st.session_state.get('story_generated_success', False):
            st.balloons()
            st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #10B981 0%, #059669 100%);
                    padding: 1.5rem;
                    border-radius: 12px;
                    margin-bottom: 1.5rem;
                    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                    text-align: center;
                ">
                    <h3 style="color: white; margin: 0; font-weight: 700;">
                        Historia gerada com sucesso!
                    </h3>
                    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;">
                        Confira o resultado abaixo
                    </p>
                </div>
            """, unsafe_allow_html=True)
            # Limpar flag para não mostrar novamente
            st.session_state.story_generated_success = False

        # Mostrar história gerada + botões de ação
        # Converter dict para Story object para compatibilidade com story_display_view
        from datetime import datetime
        story_dict = st.session_state.current_story

        # Converter created_at de string ISO para datetime se necessário
        created_at = story_dict.get('created_at')
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        story = Story(
            id=story_dict.get('id'),
            titulo=story_dict.get('titulo'),
            regras_negocio=story_dict.get('regras_negocio'),
            apis_servicos=story_dict.get('apis_servicos'),
            objetivos=story_dict.get('objetivos'),
            complexidade=story_dict.get('complexidade'),
            criterios_aceitacao=story_dict.get('criterios_aceitacao'),
            historia_gerada=story_dict.get('historia_gerada', ''),
            created_at=created_at
        )

        story_display_view.render_story(story)

        st.markdown("---")

        # Seção de possíveis melhorias (personalizada)
        with st.expander("💡 Possiveis Criterios de Melhoria", expanded=False):
            # Gerar sugestões personalizadas usando InvestService
            invest_service = InvestService()
            invest_score = invest_service.validate_invest_local(story_dict)

            st.markdown("**Sugestões personalizadas para sua história:**")

            # Mostrar pontos fracos identificados
            if invest_score.weaknesses:
                st.markdown("**Pontos que precisam de atenção:**")
                for weakness in invest_score.weaknesses:
                    st.markdown(f"- ⚠️ {weakness}")
                st.markdown("")

            # Mostrar sugestões específicas
            if invest_score.suggestions:
                st.markdown("**Sugestões de melhoria:**")
                for i, suggestion in enumerate(invest_score.suggestions, 1):
                    st.markdown(f"{i}. {suggestion}")
            else:
                st.success("Sua história está bem estruturada! Nenhuma sugestão crítica identificada.")

            # Mostrar pontos fortes
            if invest_score.strengths:
                st.markdown("")
                st.markdown("**Pontos fortes:**")
                for strength in invest_score.strengths:
                    st.markdown(f"- ✅ {strength}")

            st.markdown("---")
            st.markdown("**Fazer alterações:**")
            st.info("Use a aba 'Editar' para modificar seções específicas ou regenerar partes da história")

        st.markdown("---")

        # Botão Nova História
        if st.button("🔄 Nova Historia", type="secondary", use_container_width=True):
            # Limpar estado
            st.session_state.current_story = None
            if 'form_data' in st.session_state:
                del st.session_state.form_data
            st.rerun()


def _render_edit_tab(editor_controller: EditorController):
    """
    Renderiza tab de edição (ETAPA 2).

    Args:
        editor_controller: Controller de edição
    """
    # Interface principal de edição
    editor_view.render_editor(editor_controller)

    st.markdown("---")

    # Painel de regeneração de seções
    with st.expander("Regenerar Secoes Especificas", expanded=False):
        editor_view.render_regeneration_panel(editor_controller)

    # Painel de sugestões
    st.markdown("---")
    with st.expander("Ver Sugestoes de Melhoria", expanded=False):
        suggestions_view.render_suggestions(editor_controller)


def _render_versions_tab(editor_controller: EditorController):
    """
    Renderiza tab de versões (ETAPA 2).

    Args:
        editor_controller: Controller de edição
    """
    version_view.render_version_history(editor_controller)


if __name__ == "__main__":
    main()
