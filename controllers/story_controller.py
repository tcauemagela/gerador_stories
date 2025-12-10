"""
Controller responsável por orquestrar a criação de histórias.
Segue padrão MVC e Single Responsibility Principle.
"""

import re
from typing import Dict, Any, List
from models.story import Story
from models.session_storage import SessionStorage
from services.ai_service import AIService
from anthropic import APITimeoutError, APIConnectionError, RateLimitError


class StoryController:
    """
    Controller que orquestra o fluxo de criação de histórias.
    Responsável por coordenar Models, Services e Views.
    """

    def __init__(self, ai_service: AIService):
        """
        Inicializa o controller com o service de IA.

        Args:
            ai_service: Instância do AIService configurado
        """
        self.ai_service = ai_service

    def create_story(self, form_data: Dict[str, Any]) -> tuple[Story | None, str | None]:
        """
        Cria uma história a partir dos dados do formulário.

        Args:
            form_data: Dicionário com dados do formulário contendo:
                - titulo: str
                - regras_negocio: List[str]
                - apis_servicos: List[str]
                - objetivos: List[str]
                - complexidade: int
                - criterios_aceitacao: List[str]

        Returns:
            Tupla (Story, error_type) onde:
            - Story: Objeto Story se sucesso, None se erro
            - error_type: None se sucesso, string com tipo de erro se falha
                         (timeout, rate_limit, connection, api_key, generic)
        """
        try:
            # Extrair dados do formulário
            value_area = form_data.get("value_area", "Business")
            titulo = form_data.get("titulo", "")
            complexidade = form_data.get("complexidade", 5)

            # Dados específicos para Business
            regras_negocio = form_data.get("regras_negocio", [])
            apis_servicos = form_data.get("apis_servicos", [])
            objetivos = form_data.get("objetivos", {})
            criterios_aceitacao = form_data.get("criterios_aceitacao", [])
            api_specs = form_data.get("api_specs", None)

            # Chamar AI Service para gerar história (passa form_data completo)
            historia_gerada = self.ai_service.generate_story(
                titulo=titulo,
                regras_negocio=regras_negocio,
                apis_servicos=apis_servicos,
                objetivos=objetivos,
                complexidade=complexidade,
                criterios_aceitacao=criterios_aceitacao,
                api_specs=api_specs,
                form_data=form_data
            )

            # Se for Fix/Bug e tiver imagens, inserir as imagens reais na seção de evidências
            fix_images = form_data.get('fix_images', [])
            if value_area == 'Fix/Bug/Incidente' and fix_images:
                historia_gerada = self._insert_images_in_story(historia_gerada, fix_images)

            # Criar objeto Story
            story = Story(
                titulo=titulo,
                regras_negocio=regras_negocio if regras_negocio else [],
                apis_servicos=apis_servicos if apis_servicos else [],
                objetivos=objetivos if objetivos else {},
                complexidade=complexidade,
                criterios_aceitacao=criterios_aceitacao if criterios_aceitacao else [],
                historia_gerada=historia_gerada,
                value_area=value_area
            )

            # Salvar história no SessionStorage (ETAPA 3)
            SessionStorage.add_story(story.to_dict())

            return story, None

        except APITimeoutError as e:
            return None, "timeout"

        except RateLimitError as e:
            return None, "rate_limit"

        except APIConnectionError as e:
            return None, "connection"

        except Exception as e:
            # Importar traceback para debug detalhado
            import traceback

            # Verifica se é erro de API key
            error_str = str(e).lower()
            if "api key" in error_str or "authentication" in error_str or "unauthorized" in error_str:
                return None, "api_key"

            # Erro genérico - retorna detalhes completos para debug
            error_details = f"{type(e).__name__}: {str(e)}\n\nStack Trace:\n{traceback.format_exc()}"
            return None, f"generic:{error_details}"

    def validate_story_data(self, form_data: Dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Valida os dados do formulário antes de criar a história.

        Args:
            form_data: Dados do formulário

        Returns:
            Tupla (is_valid, errors) onde:
            - is_valid: True se válido, False caso contrário
            - errors: Lista de mensagens de erro
        """
        from models.validation import validate_form

        return validate_form(
            titulo=form_data.get("titulo", ""),
            regras_negocio=form_data.get("regras_negocio", []),
            apis_servicos=form_data.get("apis_servicos", []),
            objetivos=form_data.get("objetivos", {}),
            complexidade=form_data.get("complexidade", 0),
            criterios_aceitacao=form_data.get("criterios_aceitacao", [])
        )

    def _insert_images_in_story(self, historia: str, images: List[Dict[str, Any]]) -> str:
        """
        Insere as imagens reais na seção de Evidências da história.

        Args:
            historia: História gerada em Markdown
            images: Lista de imagens em formato {name, type, data}

        Returns:
            História com imagens inseridas
        """
        if not images:
            return historia

        # Criar bloco de imagens em Markdown (base64 inline)
        images_markdown = "\n\n**Imagens Anexadas:**\n\n"
        for i, img in enumerate(images):
            img_name = img.get('name', f'Evidência {i+1}')
            img_type = img.get('type', 'image/png')
            img_data = img.get('data', '')

            if img_data:
                # Sintaxe Markdown para imagem base64 inline
                images_markdown += f"**{img_name}:**\n\n"
                images_markdown += f"![{img_name}](data:{img_type};base64,{img_data})\n\n"

        # Encontrar a seção de Evidências e inserir as imagens
        # Padrão: ### Evidências seguido de conteúdo até a próxima seção ###
        evidencias_pattern = r'(### Evid[êe]ncias?\s*\n)'

        if re.search(evidencias_pattern, historia, re.IGNORECASE):
            # Inserir imagens logo após o título da seção de Evidências
            historia = re.sub(
                evidencias_pattern,
                r'\1' + images_markdown,
                historia,
                count=1,
                flags=re.IGNORECASE
            )
        else:
            # Se não encontrar seção de Evidências, adicionar antes de "Análise Técnica"
            analise_pattern = r'(### An[áa]lise T[ée]cnica)'
            if re.search(analise_pattern, historia, re.IGNORECASE):
                evidencias_section = f"\n### Evidências\n{images_markdown}\n"
                historia = re.sub(
                    analise_pattern,
                    evidencias_section + r'\1',
                    historia,
                    count=1,
                    flags=re.IGNORECASE
                )
            else:
                # Fallback: adicionar no final antes de Complexidade
                complexidade_pattern = r'(### Complexidade)'
                if re.search(complexidade_pattern, historia, re.IGNORECASE):
                    evidencias_section = f"\n### Evidências\n{images_markdown}\n"
                    historia = re.sub(
                        complexidade_pattern,
                        evidencias_section + r'\1',
                        historia,
                        count=1,
                        flags=re.IGNORECASE
                    )
                else:
                    # Último fallback: adicionar no final
                    historia += f"\n\n### Evidências\n{images_markdown}"

        return historia
