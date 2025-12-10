"""
Modelo de dados para histórias de usuário.
Utiliza Pydantic para validação e serialização.
Segue Single Responsibility Principle.
"""

from datetime import datetime
from typing import List, Dict, Any
from uuid import uuid4
from pydantic import BaseModel, Field, field_validator


class Story(BaseModel):
    """
    Modelo de dados que representa uma história de usuário técnica.

    Attributes:
        id: Identificador único da história
        titulo: Título da tarefa técnica
        regras_negocio: Lista de regras de negócio
        apis_servicos: Lista de APIs/serviços necessários
        objetivos: Dicionário de objetivos da tarefa com subseções
        complexidade: Pontos de complexidade (escala Fibonacci)
        criterios_aceitacao: Lista de critérios de aceitação
        historia_gerada: História completa gerada pela IA em Markdown
        created_at: Data/hora de criação
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    titulo: str = Field(..., min_length=1, max_length=100)
    regras_negocio: List[str] = Field(default_factory=list)
    apis_servicos: List[str] = Field(default_factory=list)
    objetivos: Dict[str, Any] = Field(default_factory=dict)
    complexidade: int = Field(default=5, ge=1, le=21)
    criterios_aceitacao: List[str] = Field(default_factory=list)
    historia_gerada: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.now)
    value_area: str = Field(default="Business")

    @field_validator("regras_negocio", "apis_servicos", "criterios_aceitacao")
    @classmethod
    def remove_empty_strings(cls, v: List[str]) -> List[str]:
        """Remove strings vazias ou apenas com espaços das listas."""
        return [item.strip() for item in v if item and item.strip()]

    @field_validator("titulo")
    @classmethod
    def validate_titulo(cls, v: str) -> str:
        """Valida e limpa o título."""
        if not v or not v.strip():
            raise ValueError("Título não pode estar vazio")
        return v.strip()

    def to_dict(self) -> Dict:
        """
        Converte o modelo para dicionário.

        Returns:
            Dict com todos os dados da história
        """
        return {
            "id": self.id,
            "titulo": self.titulo,
            "regras_negocio": self.regras_negocio,
            "apis_servicos": self.apis_servicos,
            "objetivos": self.objetivos,
            "complexidade": self.complexidade,
            "criterios_aceitacao": self.criterios_aceitacao,
            "historia_gerada": self.historia_gerada,
            "created_at": self.created_at.isoformat(),
            "value_area": self.value_area
        }

    def to_json_export(self) -> Dict:
        """
        Converte para formato de exportação JSON.

        Returns:
            Dict formatado para exportação
        """
        return self.to_dict()

    def to_markdown_export(self) -> str:
        """
        Retorna a história gerada em formato Markdown.

        Returns:
            String com o Markdown completo
        """
        return self.historia_gerada

    def to_text_export(self) -> str:
        """
        Converte a história para formato texto simples.
        Remove emojis e formata de maneira básica.

        Returns:
            String com texto simples
        """
        # Remove emojis comuns e formatação Markdown
        import re
        texto = self.historia_gerada

        # Remove emojis
        emoji_pattern = re.compile(
            "["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
            u"\U0001F680-\U0001F6FF"  # transporte & mapas
            u"\U0001F1E0-\U0001F1FF"  # bandeiras
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        texto = emoji_pattern.sub('', texto)

        # Remove formatação Markdown básica
        texto = re.sub(r'#{1,6}\s', '', texto)  # Remove headers
        texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)  # Remove bold
        texto = re.sub(r'\*(.+?)\*', r'\1', texto)  # Remove italic

        return texto.strip()

    class Config:
        """Configuração do modelo Pydantic."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
