"""
Service de integração com Claude API (Anthropic).
Responsável por comunicação com IA e geração de histórias.
Segue Single Responsibility Principle e Dependency Inversion Principle.
"""

from typing import List, Dict, Any
from anthropic import Anthropic, APITimeoutError, APIConnectionError, RateLimitError
import config


class AIService:
    """
    Service responsável pela comunicação com Claude API.
    Gera histórias de usuário técnicas usando IA.
    """

    def __init__(self, api_key: str):
        """
        Inicializa o service com configurações da API.

        Args:
            api_key: Chave de API da Anthropic
        """
        self.client = Anthropic(api_key=api_key)
        self.model = config.CLAUDE_MODEL
        self.max_tokens = config.CLAUDE_MAX_TOKENS
        self.timeout = config.CLAUDE_TIMEOUT

    def generate_story(
        self,
        titulo: str,
        regras_negocio: List[str] = None,
        apis_servicos: List[str] = None,
        objetivos: Dict[str, Any] = None,
        complexidade: int = 5,
        criterios_aceitacao: List[str] = None,
        api_specs: Dict[str, str] = None,
        form_data: Dict[str, Any] = None
    ) -> str:
        """
        Gera história técnica usando Claude API.

        Args:
            titulo: Título da história
            regras_negocio: Lista de regras de negócio
            apis_servicos: Lista de APIs/serviços necessários
            objetivos: Dicionário de objetivos com subseções
            complexidade: Pontos de complexidade (1-21)
            criterios_aceitacao: Lista de critérios de aceitação
            api_specs: Especificações da API (endpoint, parâmetros, etc.)
            form_data: Dados completos do formulário (para novos tipos de história)

        Returns:
            História gerada em formato Markdown

        Raises:
            APITimeoutError: Se a API demorar mais que o timeout
            RateLimitError: Se atingir limite de requisições
            APIConnectionError: Se houver erro de conexão
            Exception: Para outros erros da API
        """
        # Verificar se é um novo tipo de história (Spike, Kaizen, Fix)
        value_area = form_data.get('value_area', 'Business') if form_data else 'Business'

        if value_area == 'Spike':
            prompt = self._build_spike_prompt(form_data)
        elif value_area == 'Kaizen':
            prompt = self._build_kaizen_prompt(form_data)
        elif value_area == 'Fix/Bug/Incidente':
            prompt = self._build_fix_prompt(form_data)
        else:
            prompt = self._build_prompt(
                titulo=titulo,
                regras_negocio=regras_negocio or [],
                apis_servicos=apis_servicos or [],
                objetivos=objetivos or {},
                complexidade=complexidade,
                criterios_aceitacao=criterios_aceitacao or [],
                api_specs=api_specs,
                form_data=form_data
            )

        try:
            # Verificar se há imagens para enviar (Fix/Bug/Incidente)
            fix_images = form_data.get('fix_images', []) if form_data else []

            if fix_images and value_area == 'Fix/Bug/Incidente':
                # Usar API multimodal com imagens
                content = []

                # Adicionar cada imagem como content block
                for img in fix_images:
                    content.append({
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": img.get("type", "image/png"),
                            "data": img.get("data", "")
                        }
                    })

                # Adicionar o prompt de texto
                content.append({
                    "type": "text",
                    "text": prompt
                })

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                    messages=[
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                )
            else:
                # Requisição normal sem imagens
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    timeout=self.timeout,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            # Extrai texto da resposta
            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError(
                "Tempo esgotado ao aguardar resposta da IA. Tente novamente."
            )
        except RateLimitError:
            raise RateLimitError(
                "Limite de requisições atingido. Aguarde alguns minutos."
            )
        except APIConnectionError:
            raise APIConnectionError(
                "Erro de conexão com a API. Verifique sua internet."
            )
        except Exception as e:
            raise Exception(f"Erro ao gerar história: {str(e)}")

    def _build_prompt(
        self,
        titulo: str,
        regras_negocio: List[str],
        apis_servicos: List[str],
        objetivos: Dict[str, Any],
        complexidade: int,
        criterios_aceitacao: List[str],
        api_specs: Dict[str, str] = None,
        form_data: Dict[str, Any] = None
    ) -> str:
        """
        Constrói prompt estruturado profissional para Claude API.
        Baseado em padrões de Product Owner sênior.

        Args:
            titulo: Título da história
            regras_negocio: Lista de regras
            apis_servicos: Lista de APIs
            objetivos: Dicionário de objetivos com subseções
            complexidade: Pontos de complexidade
            criterios_aceitacao: Lista de critérios
            api_specs: Especificações da API
            form_data: Dados completos do formulário

        Returns:
            Prompt formatado em XML
        """
        # Extrair dependências se existirem
        has_dependencies = form_data.get('has_dependencies', False) if form_data else False
        dependencies = form_data.get('dependencies', '') if form_data else ''
        # Formata listas em items
        regras_formatadas = "\n".join(f"- {regra}" for regra in regras_negocio)
        apis_formatadas = "\n".join(f"- {api}" for api in apis_servicos)

        # Converte dicionário de objetivos em lista formatada
        objetivos_lista = []

        # Garantir que objetivos seja um dicionário
        if not isinstance(objetivos, dict):
            objetivos = {}

        labels = {
            "como": "Como",
            "quero": "Quero",
            "para_que": "Para que"
        }

        for key, value in objetivos.items():
            if value and isinstance(value, str) and value.strip():
                label = labels.get(key, key.replace("_", " ").title())
                objetivos_lista.append(f"{label}: {value.strip()}")

        objetivos_formatados = "\n".join(f"- {obj}" for obj in objetivos_lista) if objetivos_lista else "- Não especificado"
        criterios_formatados = "\n".join(f"- {crit}" for crit in criterios_aceitacao)

        # Formatar especificações da API se fornecidas
        api_specs_formatado = ""
        if api_specs and isinstance(api_specs, dict):
            specs_parts = []

            # Método HTTP (sempre presente)
            if api_specs.get('metodo'):
                specs_parts.append(f"Método HTTP: {api_specs['metodo']}")

            # Endpoint (sempre presente)
            if api_specs.get('endpoint'):
                specs_parts.append(f"Endpoint: {api_specs['endpoint']}")

            # Campos específicos baseados no método
            metodo = api_specs.get('metodo', '')

            if metodo == 'GET' and api_specs.get('query_params'):
                specs_parts.append(f"Parâmetros de Consulta (Query Params): {api_specs['query_params']}")
            elif metodo == 'POST' and api_specs.get('body'):
                specs_parts.append(f"Corpo da Requisição (Body): {api_specs['body']}")
            elif metodo in ['PUT', 'PATCH']:
                if api_specs.get('path_param'):
                    specs_parts.append(f"Parâmetro de Rota (Path Param): {api_specs['path_param']}")
                if api_specs.get('body'):
                    specs_parts.append(f"Corpo da Requisição (Body): {api_specs['body']}")
            elif metodo == 'DELETE' and api_specs.get('path_param'):
                specs_parts.append(f"Parâmetro de Rota (Path Param): {api_specs['path_param']}")

            # Formato de resposta (sempre presente)
            if api_specs.get('formato_resposta'):
                specs_parts.append(f"Formato de Resposta: {api_specs['formato_resposta']}")

            if specs_parts:
                api_specs_formatado = "\n".join(f"- {spec}" for spec in specs_parts)

        prompt = f"""
<task>
Você é um Product Owner sênior especializado em metodologias ágeis e documentação técnica de alta qualidade.
Sua missão é gerar uma história de usuário COMPLETA, TÉCNICA e PROFISSIONAL seguindo rigorosamente
os padrões estabelecidos.
</task>

<critical_rules>
REGRAS ABSOLUTAS (NUNCA VIOLAR):

1. NUNCA ADICIONAR EMOJIS NO CONTEÚDO DA HISTÓRIA
   - Títulos e seções devem ser puramente textuais
   - Sem emojis decorativos em nenhuma parte
   - Formato corporativo/técnico profissional

2. NUNCA INVENTAR INFORMAÇÕES
   - Use APENAS dados fornecidos pelo usuário
   - Não criar APIs, endpoints ou tecnologias não mencionadas
   - Não adicionar regras de negócio não fornecidas
   - Se algo não foi informado, não especular
   - Mantenha-se fiel aos inputs fornecidos
   - SEMPRE incluir especificações de API quando fornecidas (endpoint, parâmetros, formato, erros, documentação)

3. SER OBJETIVA E DIRETA
   - Evitar floreios ou descrições elaboradas
   - Foco em clareza e precisão técnica
   - Tom profissional e direto ao ponto
   - Sem criatividade excessiva

4. FORMATO TÉCNICO
   - Esta é uma especificação para desenvolvedores
   - Linguagem técnica precisa
   - Sem formato "Como usuário, eu quero..."
   - Formato direto: "Implementar X", "Integrar Y"
</critical_rules>

<input_data>
<titulo>{titulo}</titulo>

<regras_negocio>
{regras_formatadas}
</regras_negocio>

<apis_servicos>
{apis_formatadas}
</apis_servicos>

<objetivos>
{objetivos_formatados}
</objetivos>

<complexidade>{complexidade}</complexidade>

<criterios_aceitacao>
{criterios_formatados}
</criterios_aceitacao>
{f'''
<especificacoes_api>
{api_specs_formatado}
</especificacoes_api>''' if api_specs_formatado else ''}
{f'''
<dependencias>
{dependencies}
</dependencias>''' if has_dependencies and dependencies else ''}
</input_data>

<mandatory_structure>
SUA HISTÓRIA DEVE CONTER EXATAMENTE ESTAS SEÇÕES (SEM EMOJIS):

1. TÍTULO (nível ##)
   Formato: ## [Título da Tarefa]

2. CONTEXTO/PROBLEMA (nível ###)
   Formato: ### Contexto
   Conteúdo: Situação atual baseada APENAS nos dados fornecidos

3. OBJETIVO (nível ###)
   Formato: ### Objetivo
   Conteúdo: O que se pretende alcançar (baseado nos objetivos fornecidos)

4. REGRAS DE NEGÓCIO (nível ###)
   Formato: ### Regras de Negocio
   Conteúdo: TODAS as regras fornecidas (bullet points)
   IMPORTANTE: Incluir TODAS sem omitir nenhuma

5. APIS/SERVIÇOS (nível ###)
   Formato: ### APIs e Servicos Necessarios
   Conteúdo: Listar TODAS as APIs fornecidas
   Descrição: Uso técnico baseado no contexto

5.1. ESPECIFICAÇÕES DE API (nível #### - SUBSEÇÃO OBRIGATÓRIA SE especificacoes_api FORNECIDAS)
   Formato: #### Especificacoes da API
   CRÍTICO: Se a tag <especificacoes_api> estiver presente nos dados de entrada, VOCÊ DEVE:
   - Criar esta subseção dentro de "APIs e Servicos Necessarios"
   - Incluir TODOS os detalhes fornecidos em especificacoes_api:
     * Endpoint (se fornecido)
     * Parâmetros (se fornecido)
     * Formato de Resposta (se fornecido) - usar bloco de código markdown para JSON
     * Tratamento de Erros (se fornecido)
     * Documentação (se fornecido)
   - NÃO omitir nenhum detalhe fornecido
   - Usar formatação markdown apropriada (código em blocos ```)

6. OBJETIVOS TÉCNICOS (nível ###)
   Formato: ### Objetivos Tecnicos
   Conteúdo: TODOS os objetivos fornecidos (bullet points)

7. CRITÉRIOS DE ACEITAÇÃO (nível ###)
   Formato: ### Criterios de Aceitacao
   Conteúdo: Mínimo 3 critérios

   Use formato Gherkin quando apropriado:
   ```
   CA1 - [Nome do critério]
   Dado que [condição]
   Quando [ação]
   Então [resultado esperado]
   ```

   OU bullet points técnicos:
   ```
   - Sistema deve validar X
   - Formato de saída deve ser Y
   - Performance deve ser < Z
   ```

   SEMPRE incluir:
   - Caso de sucesso
   - Caso de erro
   - Validação técnica

8. CENÁRIOS DE TESTE (nível ###)
   Formato: ### Cenarios de Teste Sugeridos
   Conteúdo: OBRIGATÓRIO mínimo 3 cenários

   1. Cenario de sucesso: [descrição objetiva]
   2. Cenario de erro/excecao: [descrição objetiva]
   3. Cenario edge case: [descrição objetiva]

9. DEPENDÊNCIAS (nível ### - APENAS SE <dependencias> FORNECIDAS)
   Formato: ### Dependencias
   Conteúdo: Se a tag <dependencias> estiver presente nos dados de entrada:
   - Listar todas as dependências de outras equipes/sistemas
   - Indicar impacto no cronograma se aplicável
   - Sugerir pontos de comunicação necessários

10. COMPLEXIDADE (nível ###)
   Formato: ### Complexidade
   Conteúdo:
   Pontos: {complexidade}
</mandatory_structure>

<formatting_rules>
FORMATAÇÃO:

1. Use Markdown estruturado
   - ## para título principal
   - ### para seções
   - Listas com - ou números
   - Blocos de código com ```

2. NUNCA use emojis em:
   - Títulos (## ou ###)
   - Conteúdo das seções
   - Listas
   - Critérios
   - Nenhuma parte da história

3. Linguagem:
   - Técnica e profissional
   - Objetiva e direta
   - Sem adjetivos desnecessários
   - Foco em precisão

4. Estrutura:
   - Linha em branco entre seções
   - Bullet points alinhados
   - Numeração sequencial para cenários
</formatting_rules>

<quality_checklist>
ANTES DE ENTREGAR, VERIFICAR:

[ ] Nenhum emoji presente na história
[ ] Todas as 9 seções obrigatórias presentes
[ ] TODAS as regras de negócio incluídas
[ ] TODAS as APIs mencionadas detalhadas
[ ] SE <especificacoes_api> presente: subseção "Especificacoes da API" incluída com TODOS os detalhes
[ ] TODOS os objetivos incluídos
[ ] TODOS os critérios fornecidos incluídos
[ ] Mínimo 3 cenários de teste
[ ] Nenhuma informação inventada
[ ] Linguagem objetiva e técnica
[ ] Formato Markdown correto
[ ] Blocos de código JSON formatados com ```json
</quality_checklist>

<generation_instructions>
INSTRUÇÕES DE GERAÇÃO:

1. ANÁLISE:
   - Leia TODOS os inputs fornecidos
   - Identifique o tipo de implementação
   - Compreenda o CONTEXTO DE NEGÓCIO por trás da tarefa

2. CONTEXTO (ENRIQUECER COM ANÁLISE):
   - Descreva a situação atual de forma CONTEXTUALIZADA
   - Explique POR QUE essa funcionalidade é necessária
   - Conecte com o valor de negócio que será entregue
   - Mantenha-se fiel aos dados mas ELABORE o contexto de forma profissional
   - EXEMPLO: Se o input é "API de bairros", contextualize: "O sistema atual não possui capacidade de consulta geográfica granular, limitando a personalização de ofertas por região..."

3. DESCRIÇÃO (PROFISSIONAL E ELABORADA):
   - Use linguagem técnica profissional
   - EXPANDA os pontos fornecidos com detalhamento técnico relevante
   - Não adicione tecnologias não mencionadas, mas DETALHE as mencionadas
   - Para cada regra de negócio, explique seu impacto técnico
   - Para cada API, descreva sua integração e uso no fluxo

4. CRITÉRIOS DE ACEITAÇÃO (COMPLETOS E TESTÁVEIS):
   - TRANSFORME critérios simples em critérios GHERKIN completos
   - Adicione cenários de ERRO e EDGE CASES baseados nas regras
   - Cada critério deve ser VERIFICÁVEL e MENSURÁVEL
   - Inclua validações de dados, performance esperada, e tratamento de exceções

5. ESPECIFICAÇÕES DE API (SE FORNECIDAS):
   - Verifique se há tag <especificacoes_api> nos inputs
   - Se presente, OBRIGATORIAMENTE criar subseção "#### Especificacoes da API"
   - Incluir TODOS os campos fornecidos
   - Usar blocos de código ```json para JSONs
   - Detalhar códigos de erro HTTP esperados (400, 401, 404, 500)

6. CENÁRIOS DE TESTE (ABRANGENTES):
   - Crie cenários que REALMENTE testem a funcionalidade
   - Inclua dados de exemplo quando relevante
   - Cubra fluxos principais, alternativos e de exceção
   - Não omitir nenhum detalhe

3.2. INTERPRETAÇÃO DE MÉTODOS HTTP:
   Ao gerar especificações de API, você DEVE interpretar os campos de acordo com o método HTTP:

   **GET (Consulta de dados)**
   - Endpoint: Rota da API
   - Parâmetros de Consulta (Query Params): Filtros, paginação e ordenação passados na URL
   - Exemplo: GET /api/v1/usuarios?status=ativo&limit=10&page=1
   - NÃO possui corpo de requisição

   **POST (Criação de recurso)**
   - Endpoint: Rota da API
   - Corpo da Requisição (Body): Objeto JSON com os dados que serão enviados para criação
   - Exemplo: POST /api/v1/usuarios com body {{"nome": "João", "email": "joao@email.com"}}
   - NÃO utiliza parâmetros de consulta para envio de dados

   **PUT (Substituição completa de recurso)**
   - Endpoint: Rota da API contendo o identificador do recurso
   - Parâmetro de Rota (Path Param): Identificador do recurso a ser substituído
   - Corpo da Requisição (Body): Objeto JSON completo que substituirá o recurso existente
   - Exemplo: PUT /api/v1/usuarios/123 com body contendo todos os campos do recurso

   **PATCH (Alteração parcial de recurso)**
   - Endpoint: Rota da API contendo o identificador do recurso
   - Parâmetro de Rota (Path Param): Identificador do recurso a ser alterado
   - Corpo da Requisição (Body): Objeto JSON contendo apenas os campos que serão modificados
   - Exemplo: PATCH /api/v1/usuarios/123 com body {{"status": "inativo"}}

   **DELETE (Exclusão de recurso)**
   - Endpoint: Rota da API contendo o identificador do recurso
   - Parâmetro de Rota (Path Param): Identificador do recurso a ser excluído
   - Exemplo: DELETE /api/v1/usuarios/123
   - NÃO possui corpo de requisição

   IMPORTANTE: Se o usuário fornecer informações incompatíveis (ex: body em requisição GET),
   ignore ou adapte conforme o padrão REST apropriado para o método.

4. CRITÉRIOS:
   - Derive dos critérios fornecidos
   - Adicione casos de erro/sucesso relacionados
   - Mantenha testável e verificável

5. FORMATAÇÃO:
   - Aplique Markdown estruturado
   - SEM emojis em nenhuma parte
   - Seções claramente separadas

6. VALIDAÇÃO FINAL:
   - Execute checklist de qualidade
   - Confirme ausência de emojis
   - Verifique que nada foi inventado
</generation_instructions>

<output_example>
EXEMPLO DE FORMATO ESPERADO (SEM EMOJIS):

## Implementar autenticacao OAuth com Google

### Contexto

Atualmente o sistema utiliza autenticacao basica com usuario e senha.
Necessidade de adicionar opcao de login social conforme especificado.

### Objetivo

Implementar fluxo de autenticacao OAuth 2.0 utilizando Google Identity Platform.

### Regras de Negocio

- Usuario deve poder iniciar login com botao dedicado
- Sistema deve redirecionar para tela de consentimento do Google
- Email do Google deve ser usado como identificador unico
- Sessao deve expirar apos periodo definido

### APIs e Servicos Necessarios

- Google OAuth 2.0 API: Autenticacao e autorizacao de usuarios
- Google Identity Platform: Gerenciamento de identidades

#### Especificacoes da API

**Método HTTP:** POST

**Endpoint:** `/api/v1/auth/google`

**Corpo da Requisição (Body):**
```json
{{
  "redirect_uri": "https://app.example.com/callback",
  "state": "random_csrf_token"
}}
```

**Formato de Resposta:**
```json
{{
  "success": true,
  "token": "jwt_token_aqui",
  "user": {{
    "id": "123",
    "email": "user@example.com"
  }}
}}
```

### Objetivos Tecnicos

- Permitir autenticacao via conta Google
- Reduzir tempo de cadastro
- Melhorar experiencia do usuario

### Criterios de Aceitacao

CA1 - Iniciar fluxo OAuth
Dado que usuario acessa tela de login
Quando clica em botao de login com Google
Então deve ser redirecionado para tela de consentimento

CA2 - Processar autorizacao
Dado que usuario autoriza acesso
Quando Google redireciona de volta
Então sistema deve processar tokens
E criar ou atualizar cadastro do usuario

CA3 - Tratar erro
Dado que usuario nega permissao
Quando retorna para aplicacao
Então sistema deve exibir mensagem de erro apropriada

### Cenarios de Teste Sugeridos

1. Cenario de sucesso: Usuario completa fluxo OAuth e e autenticado com sucesso
2. Cenario de erro: Usuario nega permissao e recebe mensagem apropriada
3. Cenario edge case: Token expira durante sessao e sistema renova automaticamente

### Complexidade

Pontos: 5
</output_example>

<final_reminder>
CRÍTICO - LEMBRE-SE:

1. SEM EMOJIS EM NENHUMA PARTE DA HISTÓRIA
2. USAR APENAS INFORMAÇÕES FORNECIDAS
3. NÃO INVENTAR NADA
4. SER OBJETIVA E DIRETA
5. INCLUIR TODAS AS SEÇÕES OBRIGATÓRIAS
6. INCLUIR TODAS AS REGRAS/APIs/OBJETIVOS/CRITÉRIOS FORNECIDOS
7. **ESPECIFICAÇÕES DE API**: Se a tag <especificacoes_api> estiver presente, OBRIGATORIAMENTE incluir subseção "#### Especificacoes da API" com TODOS os detalhes fornecidos (endpoint, parâmetros, formato de resposta em ```json, tratamento de erros, documentação)

Retorne APENAS o Markdown da história, sem texto adicional antes ou depois.
</final_reminder>
"""

        return prompt.strip()

    # ============================================================
    # NOVOS MÉTODOS DA ETAPA 2
    # ============================================================

    def regenerate_section(
        self,
        section_name: str,
        original_story: Dict,
        form_data: Dict
    ) -> str:
        """
        Regenera apenas uma seção específica da história.
        ETAPA 2: Permite regeneração parcial mantendo contexto.

        Args:
            section_name: Nome da seção ("criterios", "testes", "arquitetura", "beneficios")
            original_story: História completa original
            form_data: Dados do formulário original

        Returns:
            Seção regenerada em Markdown

        Raises:
            Exception: Em caso de erro na API
        """
        prompt = self._build_regeneration_prompt(section_name, original_story, form_data)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao regenerar seção. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao regenerar seção: {str(e)}")

    def _build_regeneration_prompt(
        self,
        section_name: str,
        original_story: Dict,
        form_data: Dict
    ) -> str:
        """
        Constrói prompt para regeneração parcial.

        Args:
            section_name: Seção a regenerar
            original_story: História original
            form_data: Dados do formulário

        Returns:
            Prompt formatado
        """
        historia_completa = original_story.get('historia_gerada', '')

        section_mapping = {
            'criterios': 'Criterios de Aceitacao',
            'testes': 'Cenarios de Teste Sugeridos',
            'arquitetura': 'Estrutura Tecnica/Arquitetura',
            'beneficios': 'Beneficios'
        }

        section_label = section_mapping.get(section_name, section_name)

        prompt = f"""
<task>
Regenere APENAS a seção "{section_label}" desta história.
Mantenha todo o contexto e informações da história original.
</task>

<critical_rules>
1. NUNCA ADICIONAR EMOJIS
2. USAR APENAS INFORMAÇÕES FORNECIDAS
3. SER OBJETIVA E DIRETA
4. NÃO INVENTAR NADA
</critical_rules>

<original_story>
{historia_completa}
</original_story>

<form_data>
Título: {form_data.get('titulo', '')}
Regras de Negócio:
{chr(10).join(f"- {r}" for r in form_data.get('regras_negocio', []))}

APIs/Serviços:
{chr(10).join(f"- {a}" for a in form_data.get('apis_servicos', []))}

Objetivos:
{chr(10).join(f"- {o}" for o in form_data.get('objetivos', []))}

Complexidade: {form_data.get('complexidade', 5)}

Critérios de Aceitação:
{chr(10).join(f"- {c}" for c in form_data.get('criterios_aceitacao', []))}
</form_data>

<section_to_regenerate>
{section_label}
</section_to_regenerate>

<instructions>
1. Analise o contexto da história completa
2. Regenere APENAS a seção "{section_label}"
3. Mantenha consistência com o resto da história
4. Use mesmo nível de detalhe técnico
5. Retorne APENAS a seção em Markdown, começando com ### {section_label}
</instructions>

<output_format>
### {section_label}

[Conteúdo regenerado da seção...]
</output_format>

Retorne APENAS a seção solicitada em Markdown, sem texto adicional.
"""

        return prompt.strip()

    def validate_invest_with_ai(self, story: Dict) -> str:
        """
        Valida história com IA segundo critérios INVEST.
        ETAPA 2: Análise profunda de qualidade da história.

        Args:
            story: História completa

        Returns:
            Resposta JSON da IA com scores e justificativas

        Raises:
            Exception: Em caso de erro na API
        """
        from services.invest_service import InvestService

        invest_service = InvestService()
        prompt = invest_service.prepare_for_ai_validation(story)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao validar. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao validar história: {str(e)}")

    def analyze_and_suggest(self, story: Dict) -> str:
        """
        Analisa história e sugere melhorias.
        ETAPA 2: Identifica problemas e propõe soluções.

        Args:
            story: História completa

        Returns:
            Resposta JSON da IA com sugestões

        Raises:
            Exception: Em caso de erro na API
        """
        prompt = self._build_suggestion_prompt(story)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                timeout=self.timeout,
                messages=[{"role": "user", "content": prompt}]
            )

            if response.content and len(response.content) > 0:
                return response.content[0].text

            raise Exception("Resposta vazia da API")

        except APITimeoutError:
            raise APITimeoutError("Tempo esgotado ao analisar. Tente novamente.")
        except RateLimitError:
            raise RateLimitError("Limite de requisições atingido. Aguarde alguns minutos.")
        except APIConnectionError:
            raise APIConnectionError("Erro de conexão com a API. Verifique sua internet.")
        except Exception as e:
            raise Exception(f"Erro ao analisar história: {str(e)}")

    def _build_suggestion_prompt(self, story: Dict) -> str:
        """
        Constrói prompt para análise e sugestões.

        Args:
            story: História completa

        Returns:
            Prompt formatado
        """
        historia_texto = story.get('historia_gerada', '')

        prompt = f"""
<task>
Analise esta história técnica e sugira melhorias específicas.
Seja OBJETIVO e PRÁTICO nas sugestões.
NÃO INVENTE - use apenas o que está na história.
</task>

<story>
{historia_texto}
</story>

<analysis_points>
Analise os seguintes aspectos:

1. AMBIGUIDADES:
   - Termos vagos ou imprecisos
   - Falta de especificidade técnica
   - Requisitos não claros

2. TAMANHO:
   - História muito grande (complexidade > 13)?
   - Pode ser quebrada em partes menores?
   - Sugestões de divisão lógica

3. CRITÉRIOS FALTANTES:
   - Cenários não cobertos
   - Casos de erro não tratados
   - Validações ausentes

4. CLAREZA:
   - Seções que precisam mais detalhes
   - Falta de exemplos concretos
   - Informações técnicas incompletas
</analysis_points>

<output_format>
Retorne APENAS JSON array neste formato:
[
  {{
    "type": "ambiguidade|tamanho|criterio|clareza",
    "severity": "baixa|media|alta",
    "problem": "descrição específica do problema encontrado",
    "suggestion": "sugestão específica e acionável de melhoria",
    "applicable": true|false
  }}
]
</output_format>

<important>
- Seja específico: "A seção X está vaga" não "História pode melhorar"
- Sugestões acionáveis: "Adicione critério para caso Y" não "Melhore critérios"
- Use dados da história, não invente
- Máximo 5 sugestões mais importantes
- Retorne APENAS o JSON, sem texto antes ou depois
</important>
"""

        return prompt.strip()

    def _build_spike_prompt(self, form_data: Dict[str, Any]) -> str:
        """
        Constrói prompt para histórias do tipo Spike (exploratórias).

        Args:
            form_data: Dados do formulário Spike

        Returns:
            Prompt formatado
        """
        titulo = form_data.get('titulo', '')
        pergunta = form_data.get('spike_pergunta', '')
        alternativas = form_data.get('spike_alternativas', [])
        timebox = form_data.get('spike_timebox', 8)
        output = form_data.get('spike_output', '')
        criterios_sucesso = form_data.get('spike_criterios_sucesso', [])

        alternativas_formatadas = "\n".join(f"- {alt}" for alt in alternativas if alt)
        criterios_formatados = "\n".join(f"- {crit}" for crit in criterios_sucesso if crit)

        prompt = f"""
<task>
Você é um Product Owner sênior especializado em metodologias ágeis.
Gere uma história de usuário do tipo SPIKE (exploratória/investigação) completa e profissional.
</task>

<critical_rules>
1. NUNCA ADICIONAR EMOJIS
2. SER OBJETIVO E TÉCNICO
3. FOCAR NA INVESTIGAÇÃO, NÃO NA IMPLEMENTAÇÃO
4. DEFINIR CLARAMENTE O QUE SERÁ ENTREGUE AO FINAL
</critical_rules>

<input_data>
<titulo>{titulo}</titulo>
<pergunta_hipotese>{pergunta}</pergunta_hipotese>
<alternativas_investigar>
{alternativas_formatadas}
</alternativas_investigar>
<timebox_horas>{timebox}</timebox_horas>
<output_esperado>{output}</output_esperado>
<criterios_sucesso>
{criterios_formatados}
</criterios_sucesso>
</input_data>

<mandatory_structure>
## [Título]

### Contexto
Descreva o cenário que motivou esta investigação. Por que precisamos investigar isso?
Qual incerteza técnica ou de negócio estamos tentando resolver?

### Pergunta/Hipótese
Formule claramente a pergunta principal que esta spike deve responder.
Se aplicável, liste hipóteses secundárias a serem validadas.

### Escopo da Investigação
Liste especificamente o que SERÁ e o que NÃO SERÁ investigado.
Defina limites claros para manter o foco.

### Alternativas a Avaliar
Para cada alternativa fornecida, descreva:
- O que é a tecnologia/abordagem
- Prós esperados
- Contras potenciais
- Critérios de avaliação

### Timebox
Tempo máximo: {timebox} horas
- Defina checkpoints intermediários
- Estabeleça momento de decisão go/no-go

### Entregáveis
Output esperado: {output}
Liste especificamente o que será produzido:
- Documentação
- POC (se aplicável)
- Recomendação final

### Critérios de Sucesso
Defina quando a spike será considerada bem-sucedida.
Liste critérios mensuráveis e verificáveis.

### Próximos Passos Potenciais
Descreva os possíveis caminhos após a conclusão:
- Se a hipótese for validada
- Se a hipótese for invalidada
- Se precisar de mais investigação
</mandatory_structure>

Retorne APENAS o Markdown da história, sem texto adicional.
"""
        return prompt.strip()

    def _build_kaizen_prompt(self, form_data: Dict[str, Any]) -> str:
        """
        Constrói prompt para histórias do tipo Kaizen (melhoria contínua).

        Args:
            form_data: Dados do formulário Kaizen

        Returns:
            Prompt formatado
        """
        titulo = form_data.get('titulo', '')
        processo = form_data.get('kaizen_processo', '')
        situacao_atual = form_data.get('kaizen_situacao_atual', '')
        meta = form_data.get('kaizen_meta', '')
        metricas = form_data.get('kaizen_metricas', [])
        impacto = form_data.get('kaizen_impacto', '')
        complexidade = form_data.get('complexidade', 5)

        metricas_formatadas = "\n".join(f"- {m}" for m in metricas if m)

        prompt = f"""
<task>
Você é um Product Owner sênior especializado em metodologias ágeis e melhoria contínua.
Gere uma história de usuário do tipo KAIZEN (melhoria contínua) completa e profissional.
</task>

<critical_rules>
1. NUNCA ADICIONAR EMOJIS
2. FOCAR EM MÉTRICAS E RESULTADOS MENSURÁVEIS
3. COMPARAR ESTADO ATUAL vs ESTADO DESEJADO
4. SER ESPECÍFICO SOBRE O IMPACTO ESPERADO
</critical_rules>

<input_data>
<titulo>{titulo}</titulo>
<processo_area>{processo}</processo_area>
<situacao_atual>{situacao_atual}</situacao_atual>
<meta_desejada>{meta}</meta_desejada>
<metricas_sucesso>
{metricas_formatadas}
</metricas_sucesso>
<impacto_esperado>{impacto}</impacto_esperado>
<complexidade>{complexidade}</complexidade>
</input_data>

<mandatory_structure>
## [Título]

### Contexto
Descreva o processo/área atual e por que precisa ser melhorado.
Conecte com o impacto no time e na entrega de valor.

### Situação Atual (Baseline)
Detalhe o estado atual com dados concretos:
- Métricas atuais (tempo, taxa de erro, etc.)
- Problemas identificados
- Impacto negativo no time/processo

### Meta Desejada
Descreva claramente o estado futuro esperado:
- Métricas alvo
- Melhorias específicas
- Benefícios esperados

### Plano de Melhoria
Liste as ações necessárias para atingir a meta:
1. Ação 1 - Descrição e impacto esperado
2. Ação 2 - Descrição e impacto esperado
(baseado no processo descrito)

### Métricas de Sucesso
Defina como medir o sucesso da melhoria:
- Métrica principal
- Métricas secundárias
- Frequência de medição

### Impacto Esperado
Descreva o impacto positivo após a implementação:
- No time
- No processo
- Na entrega de valor

### Critérios de Aceitação
CA1 - [Critério mensurável]
Dado que [situação atual]
Quando [melhoria implementada]
Então [resultado esperado com métrica]

### Riscos e Mitigações
Liste possíveis riscos na implementação e como mitigá-los.

### Complexidade
Pontos: {complexidade}
</mandatory_structure>

Retorne APENAS o Markdown da história, sem texto adicional.
"""
        return prompt.strip()

    def _build_fix_prompt(self, form_data: Dict[str, Any]) -> str:
        """
        Constrói prompt para histórias do tipo Fix/Bug/Incidente.

        Args:
            form_data: Dados do formulário Fix

        Returns:
            Prompt formatado
        """
        titulo = form_data.get('titulo', '')
        descricao = form_data.get('fix_descricao', '')
        passos = form_data.get('fix_passos_reproduzir', [])
        esperado = form_data.get('fix_comportamento_esperado', '')
        atual = form_data.get('fix_comportamento_atual', '')
        ambiente = form_data.get('fix_ambiente', '')
        severidade = form_data.get('fix_severidade', '')
        logs = form_data.get('fix_logs', '')
        complexidade = form_data.get('complexidade', 5)
        fix_images = form_data.get('fix_images', [])

        passos_formatados = "\n".join(f"{i+1}. {p}" for i, p in enumerate(passos) if p)

        # Texto sobre imagens anexadas
        imagens_info = ""
        if fix_images:
            nomes_imagens = [img.get('name', 'imagem') for img in fix_images]
            imagens_info = f"""
<imagens_anexadas>
Foram anexadas {len(fix_images)} imagem(ns) como evidência do bug:
{chr(10).join(f"- {nome}" for nome in nomes_imagens)}

IMPORTANTE: As imagens serão inseridas automaticamente na história depois.
NÃO descreva o conteúdo das imagens na seção de Evidências.
Apenas mencione que há evidências visuais anexadas e foque nos logs/erros textuais se houver.
</imagens_anexadas>
"""

        prompt = f"""
<task>
Você é um Product Owner sênior especializado em metodologias ágeis.
Gere uma história de usuário do tipo FIX/BUG/INCIDENTE completa e profissional.
</task>

<critical_rules>
1. NUNCA ADICIONAR EMOJIS
2. SER PRECISO NA DESCRIÇÃO DO PROBLEMA
3. FOCAR NA CORREÇÃO, NÃO EM NOVAS FUNCIONALIDADES
4. INCLUIR CRITÉRIOS DE VERIFICAÇÃO DA CORREÇÃO
5. NÃO DESCREVER O CONTEÚDO DAS IMAGENS - elas serão inseridas automaticamente depois
</critical_rules>

<input_data>
<titulo>{titulo}</titulo>
<descricao_bug>{descricao}</descricao_bug>
<passos_reproduzir>
{passos_formatados}
</passos_reproduzir>
<comportamento_esperado>{esperado}</comportamento_esperado>
<comportamento_atual>{atual}</comportamento_atual>
<ambiente_afetado>{ambiente}</ambiente_afetado>
<severidade>{severidade}</severidade>
<logs_evidencias>{logs}</logs_evidencias>
<complexidade>{complexidade}</complexidade>
{imagens_info}
</input_data>

<mandatory_structure>
## [Título]

### Descrição do Problema
Descreva o bug/incidente de forma clara e técnica.
Inclua contexto sobre quando foi identificado e impacto.

### Severidade e Impacto
**Severidade:** {severidade}
**Ambiente:** {ambiente}

Descreva o impacto:
- Usuários afetados
- Funcionalidades comprometidas
- Impacto no negócio

### Passos para Reproduzir
{passos_formatados if passos_formatados else "1. [Passo 1]\n2. [Passo 2]\n3. [Passo 3]"}

### Comportamento Esperado
{esperado}

### Comportamento Atual
{atual}

### Evidências
{"(As imagens de evidência serão inseridas automaticamente aqui)" + chr(10) + chr(10) if fix_images else ""}{"**Logs/Mensagens de Erro:**" + chr(10) + f"```{chr(10)}{logs}{chr(10)}```" if logs else ""}{"Nenhuma evidência adicional fornecida." if not logs and not fix_images else ""}

### Análise Técnica Sugerida
Baseado na descrição{" e nas imagens anexadas" if fix_images else ""}, sugira possíveis causas raiz:
- Causa potencial 1
- Causa potencial 2
- Área do código a investigar

### Critérios de Aceitação
CA1 - Bug Corrigido
Dado que o bug foi identificado
Quando a correção for aplicada
Então o comportamento esperado deve ocorrer

CA2 - Sem Regressão
Dado que a correção foi aplicada
Quando funcionalidades relacionadas forem testadas
Então não deve haver regressão

CA3 - Verificação em {ambiente}
Dado que a correção foi deployada em {ambiente}
Quando o cenário do bug for reproduzido
Então o sistema deve funcionar corretamente

### Cenários de Teste
1. Cenário de verificação: Reproduzir bug e confirmar correção
2. Cenário de regressão: Testar funcionalidades adjacentes
3. Cenário de carga (se aplicável): Verificar sob condições similares

### Complexidade
Pontos: {complexidade}
</mandatory_structure>

Retorne APENAS o Markdown da história, sem texto adicional.
"""
        return prompt.strip()
