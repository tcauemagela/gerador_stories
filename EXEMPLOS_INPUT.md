# Exemplos de Input para Testar o Gerador de Historias

Este documento contém exemplos de input para cada tipo de história disponível no sistema.

---

## 1. Business (Funcional) - Entrega de valor ao usuário

### Exemplo 1.1: API REST (GET)

**Título da Tarefa:**
```
DU Benefícios - Desenvolver API de Consulta de Bairros
```

**Regras de Negócio:**
```
1. A API deve retornar apenas bairros ativos no sistema
2. O resultado deve ser paginado com limite máximo de 100 registros por página
3. Deve ser possível filtrar por cidade e estado
```

**APIs/Serviços Necessários:**
```
1. Banco de dados PostgreSQL - tabela tb_bairros
2. Cache Redis para otimização de consultas frequentes
```

**Objetivos:**
- **Como:** Desenvolvedor do time de front-end
- **Quero:** Consumir uma API REST que retorne a lista de bairros cadastrados
- **Para que:** Preencher automaticamente o campo de bairro no formulário de endereço do usuário

**Complexidade:** 5

**Critérios de Aceitação:**
```
1. Dado que faço uma requisição GET para /api/v1/bairros, quando a requisição é bem-sucedida, então devo receber status 200 e uma lista de bairros
2. Dado que informo o parâmetro cidade_id, quando a requisição é processada, então devo receber apenas bairros daquela cidade
3. Dado que não existem bairros para o filtro informado, quando a requisição é processada, então devo receber uma lista vazia com status 200
```

**Esta tarefa envolve desenvolvimento de API?** Sim

- **Método HTTP:** GET
- **Endpoint:** /api/v1/bairros
- **Parâmetros de Consulta (Query Params):**
```
cidade_id=123&estado=SP&page=1&limit=50&status=ativo
```
- **Formato da Resposta:**
```json
{
  "sucesso": true,
  "dados": [
    {
      "id": 1,
      "nome": "Centro",
      "cidade_id": 123,
      "cep_inicial": "01000-000",
      "cep_final": "01999-999"
    }
  ],
  "paginacao": {
    "pagina_atual": 1,
    "total_paginas": 5,
    "total_registros": 245
  }
}
```

**Possui dependências?** Não

---

### Exemplo 1.2: API REST (POST)

**Título da Tarefa:**
```
Checkout - Criar endpoint de registro de pedidos
```

**Regras de Negócio:**
```
1. O pedido deve ter pelo menos 1 item
2. O valor total deve ser calculado automaticamente baseado nos itens
3. O estoque deve ser validado antes de confirmar o pedido
4. Cupons de desconto devem ser validados e aplicados se válidos
```

**APIs/Serviços Necessários:**
```
1. API de Estoque para validação de disponibilidade
2. API de Cupons para validação de descontos
3. Gateway de Pagamento Stripe
4. Serviço de Notificação por Email (SendGrid)
```

**Objetivos:**
- **Como:** Usuário autenticado na plataforma
- **Quero:** Finalizar minha compra com os itens do carrinho
- **Para que:** Receber os produtos em minha residência

**Complexidade:** 13

**Critérios de Aceitação:**
```
1. Dado que tenho itens no carrinho e estoque disponível, quando finalizo a compra, então o pedido deve ser criado com status "pendente_pagamento"
2. Dado que o pagamento é aprovado, quando o webhook do gateway notifica, então o pedido deve mudar para status "confirmado"
3. Dado que algum item não tem estoque, quando tento finalizar, então devo receber erro 422 indicando quais itens estão indisponíveis
4. Dado que aplico um cupom válido, quando finalizo a compra, então o desconto deve ser aplicado ao valor total
```

**Esta tarefa envolve desenvolvimento de API?** Sim

- **Método HTTP:** POST
- **Endpoint:** /api/v1/pedidos
- **Corpo da Requisição (Body):**
```json
{
  "itens": [
    {
      "produto_id": "SKU-12345",
      "quantidade": 2,
      "preco_unitario": 99.90
    }
  ],
  "endereco_entrega_id": 456,
  "cupom_desconto": "PROMO10",
  "metodo_pagamento": {
    "tipo": "cartao_credito",
    "token": "tok_visa_4242"
  }
}
```
- **Formato da Resposta:**
```json
{
  "sucesso": true,
  "pedido": {
    "id": "PED-2024-001234",
    "status": "pendente_pagamento",
    "valor_subtotal": 199.80,
    "valor_desconto": 19.98,
    "valor_frete": 15.00,
    "valor_total": 194.82,
    "data_criacao": "2024-01-15T14:30:00Z"
  }
}
```

**Possui dependências?** Sim
```
Depende da API de Estoque do time de Logística estar disponível em produção.
Depende da integração com Stripe já estar homologada.
```

---

### Exemplo 1.3: API REST (PUT)

**Título da Tarefa:**
```
Perfil - Atualização completa de dados cadastrais do usuário
```

**Regras de Negócio:**
```
1. Email não pode ser alterado (apenas via processo de verificação separado)
2. CPF deve ser validado antes de salvar
3. Telefone deve seguir formato brasileiro
4. Alterações sensíveis devem gerar log de auditoria
```

**APIs/Serviços Necessários:**
```
1. Serviço de validação de CPF (ReceitaWS)
2. Serviço de auditoria interno
```

**Objetivos:**
- **Como:** Usuário cadastrado
- **Quero:** Atualizar meus dados pessoais completos
- **Para que:** Manter meu cadastro atualizado para receber comunicações e entregas

**Complexidade:** 8

**Critérios de Aceitação:**
```
1. Dado que envio dados válidos, quando a atualização é processada, então todos os campos devem ser substituídos
2. Dado que o CPF informado é inválido, quando tento atualizar, então devo receber erro 422
3. Dado que a atualização é bem-sucedida, quando verifico o log, então deve existir registro de auditoria
```

**Esta tarefa envolve desenvolvimento de API?** Sim

- **Método HTTP:** PUT
- **Endpoint:** /api/v1/usuarios/{id}
- **Parâmetro de Rota (Path Param):**
```
id (UUID do usuário, ex: 550e8400-e29b-41d4-a716-446655440000)
```
- **Corpo da Requisição (Body):**
```json
{
  "nome_completo": "João da Silva Santos",
  "cpf": "123.456.789-00",
  "data_nascimento": "1990-05-15",
  "telefone": "(11) 99999-8888",
  "endereco": {
    "logradouro": "Rua das Flores",
    "numero": "123",
    "complemento": "Apto 45",
    "bairro": "Centro",
    "cidade": "São Paulo",
    "estado": "SP",
    "cep": "01310-100"
  }
}
```
- **Formato da Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Dados atualizados com sucesso",
  "usuario": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "nome_completo": "João da Silva Santos",
    "atualizado_em": "2024-01-15T14:30:00Z"
  }
}
```

**Possui dependências?** Não

---

### Exemplo 1.4: API REST (PATCH)

**Título da Tarefa:**
```
Notificações - Atualizar preferências de comunicação
```

**Regras de Negócio:**
```
1. Usuário pode optar por receber ou não cada tipo de notificação
2. Pelo menos um canal de comunicação deve permanecer ativo
3. Alterações devem ser aplicadas imediatamente
```

**APIs/Serviços Necessários:**
```
1. Serviço de Mensageria (para atualizar filas de envio)
```

**Objetivos:**
- **Como:** Usuário da plataforma
- **Quero:** Modificar apenas minhas preferências de notificação
- **Para que:** Receber apenas comunicações relevantes para mim

**Complexidade:** 3

**Critérios de Aceitação:**
```
1. Dado que altero apenas o campo "email_marketing", quando a requisição é processada, então apenas esse campo deve ser modificado
2. Dado que tento desativar todos os canais, quando processo a requisição, então devo receber erro 422
```

**Esta tarefa envolve desenvolvimento de API?** Sim

- **Método HTTP:** PATCH
- **Endpoint:** /api/v1/usuarios/{id}/preferencias
- **Parâmetro de Rota (Path Param):**
```
id (UUID do usuário)
```
- **Corpo da Requisição (Body):**
```json
{
  "email_marketing": false,
  "push_promocoes": true
}
```
- **Formato da Resposta:**
```json
{
  "sucesso": true,
  "preferencias": {
    "email_marketing": false,
    "email_transacional": true,
    "push_promocoes": true,
    "push_pedidos": true,
    "sms": false
  }
}
```

**Possui dependências?** Não

---

### Exemplo 1.5: API REST (DELETE)

**Título da Tarefa:**
```
Endereços - Remover endereço de entrega
```

**Regras de Negócio:**
```
1. Não é possível remover o endereço principal se for o único cadastrado
2. Se o endereço removido era o principal, promover outro para principal
3. Endereços com pedidos em andamento não podem ser removidos
```

**APIs/Serviços Necessários:**
```
1. API de Pedidos para verificar pedidos em andamento
```

**Objetivos:**
- **Como:** Usuário com múltiplos endereços cadastrados
- **Quero:** Excluir um endereço que não uso mais
- **Para que:** Manter minha lista de endereços organizada

**Complexidade:** 5

**Critérios de Aceitação:**
```
1. Dado que o endereço não tem pedidos vinculados, quando solicito exclusão, então o endereço deve ser removido
2. Dado que o endereço tem pedido em andamento, quando solicito exclusão, então devo receber erro 409
3. Dado que excluo o endereço principal, quando há outros endereços, então o mais recente deve virar principal
```

**Esta tarefa envolve desenvolvimento de API?** Sim

- **Método HTTP:** DELETE
- **Endpoint:** /api/v1/usuarios/{usuario_id}/enderecos/{endereco_id}
- **Parâmetro de Rota (Path Param):**
```
usuario_id (UUID do usuário)
endereco_id (UUID do endereço)
```
- **Formato da Resposta:**
```json
{
  "sucesso": true,
  "mensagem": "Endereço removido com sucesso"
}
```

**Possui dependências?** Sim
```
Depende da API de Pedidos para consulta de pedidos em andamento
```

---

### Exemplo 1.6: Business SEM API

**Título da Tarefa:**
```
Dashboard - Implementar gráfico de vendas mensais
```

**Regras de Negócio:**
```
1. O gráfico deve exibir os últimos 12 meses de vendas
2. Deve ser possível alternar entre visualização por valor e por quantidade
3. Ao clicar em um mês, exibir detalhamento daquele período
```

**APIs/Serviços Necessários:**
```
1. API de relatórios existente (GET /api/v1/relatorios/vendas)
2. Biblioteca Chart.js para renderização
```

**Objetivos:**
- **Como:** Gerente de vendas
- **Quero:** Visualizar um gráfico com a evolução das vendas
- **Para que:** Acompanhar o desempenho e identificar tendências

**Complexidade:** 8

**Critérios de Aceitação:**
```
1. Dado que acesso o dashboard, quando a página carrega, então devo ver o gráfico com dados dos últimos 12 meses
2. Dado que clico no botão de alternar, quando mudo para quantidade, então o gráfico deve atualizar
3. Dado que clico em uma barra do gráfico, quando o mês é selecionado, então devo ver modal com detalhes
```

**Esta tarefa envolve desenvolvimento de API?** Não

**Possui dependências?** Não

---

## 2. Spike (Exploratória) - Investigação/pesquisa técnica

### Exemplo 2.1: Migração de Tecnologia

**Título da Investigação:**
```
Spike - Avaliar migração do banco de dados MySQL para PostgreSQL
```

**Pergunta/Hipótese a Validar:**
```
É viável migrar nosso banco MySQL 5.7 para PostgreSQL 15 sem perda de dados e com downtime inferior a 4 horas, mantendo compatibilidade com as queries existentes?
```

**Alternativas/Tecnologias a Investigar:**
```
1. pgLoader para migração automatizada
2. AWS DMS (Database Migration Service)
3. Migração manual com scripts customizados
4. Replicação lógica com Debezium
```

**Output Esperado:** Documento de decisão

**Critérios de Sucesso da Investigação:**
```
1. Identificar ferramenta que suporte todos os tipos de dados utilizados
2. Estimar tempo de migração para nosso volume de dados (500GB)
3. Mapear queries que precisarão de ajustes de sintaxe
4. Avaliar impacto no desempenho das principais consultas
5. Documentar riscos e plano de rollback
```

---

### Exemplo 2.2: Nova Arquitetura

**Título da Investigação:**
```
Spike - Viabilidade de implementar arquitetura de microsserviços
```

**Pergunta/Hipótese a Validar:**
```
A migração do monolito atual para microsserviços trará benefícios de escalabilidade e manutenibilidade que justifiquem o investimento, considerando o tamanho atual do time (8 desenvolvedores)?
```

**Alternativas/Tecnologias a Investigar:**
```
1. Kubernetes com service mesh Istio
2. AWS ECS com App Mesh
3. Arquitetura serverless com AWS Lambda
4. Manter monolito modular com melhorias incrementais
```

**Output Esperado:** Apresentação para o time

**Critérios de Sucesso da Investigação:**
```
1. Definir critérios objetivos para decisão (custo, complexidade, time-to-market)
2. Criar POC de um serviço isolado para medir overhead operacional
3. Estimar custo de infraestrutura para cada alternativa
4. Avaliar curva de aprendizado do time
```

---

### Exemplo 2.3: Integração com Serviço Externo

**Título da Investigação:**
```
Spike - Integração com gateway de pagamento PIX
```

**Pergunta/Hipótese a Validar:**
```
Qual gateway de pagamento PIX oferece melhor combinação de taxas, SLA de disponibilidade e facilidade de integração para nosso volume de transações (10.000 transações/mês)?
```

**Alternativas/Tecnologias a Investigar:**
```
1. Mercado Pago
2. PagSeguro
3. Stripe (PIX via parceiros)
4. Integração direta com banco via API DICT
```

**Output Esperado:** Relatório técnico

**Critérios de Sucesso da Investigação:**
```
1. Comparar taxas por transação de cada provider
2. Testar sandbox de cada solução com cenários reais
3. Avaliar qualidade da documentação e suporte técnico
4. Medir tempo médio de confirmação de pagamento
5. Verificar conformidade com LGPD
```

---

## 3. Kaizen (Melhoria Contínua) - Otimização de processos

### Exemplo 3.1: Pipeline de Deploy

**Título da Melhoria:**
```
Kaizen - Reduzir tempo de deploy em produção
```

**Processo/Área a Melhorar:**
```
Pipeline de CI/CD atual, desde o commit até a disponibilização em produção. Inclui build, testes, análise de código e deploy nos servidores.
```

**Situação Atual (Baseline):**
```
- Tempo médio de deploy: 45 minutos
- Taxa de falha no pipeline: 25%
- Rollbacks necessários: 3 por mês em média
- Build sequencial sem cache
- Testes rodam todos a cada commit (sem otimização)
```

**Meta Desejada:**
```
- Reduzir tempo de deploy para máximo 15 minutos
- Reduzir taxa de falha para menos de 5%
- Zero rollbacks por problemas de deploy
- Implementar builds incrementais com cache
```

**Métricas de Sucesso:**
```
1. Tempo médio de execução do pipeline (meta: < 15 min)
2. Taxa de sucesso de deploys (meta: > 95%)
3. Número de rollbacks mensais (meta: 0)
4. Satisfação do time com o processo (survey)
```

**Impacto Esperado no Time/Processo:**
```
Desenvolvedores terão feedback mais rápido sobre suas alterações, reduzindo o tempo de espera e aumentando a produtividade. Menos rollbacks significam menos interrupções e estresse para o time de operações.
```

**Complexidade:** 13

---

### Exemplo 3.2: Code Review

**Título da Melhoria:**
```
Kaizen - Otimizar processo de code review
```

**Processo/Área a Melhorar:**
```
Fluxo de revisão de código, desde a criação do PR até o merge. Atualmente os PRs ficam muito tempo aguardando revisão e frequentemente precisam de múltiplas rodadas de correção.
```

**Situação Atual (Baseline):**
```
- Tempo médio de PR aberto: 3 dias
- Média de 4 rodadas de revisão por PR
- 60% dos PRs são muito grandes (> 500 linhas)
- Não há guidelines claros de revisão
- Revisores não têm tempo dedicado para reviews
```

**Meta Desejada:**
```
- Tempo máximo de PR aberto: 1 dia
- Máximo de 2 rodadas de revisão por PR
- 90% dos PRs com menos de 200 linhas
- Guidelines documentados e seguidos
- Rotação de revisores com tempo dedicado
```

**Métricas de Sucesso:**
```
1. Lead time de PR (tempo até merge)
2. Número de rodadas de revisão
3. Tamanho médio dos PRs (linhas alteradas)
4. Tempo de resposta do primeiro review
```

**Impacto Esperado no Time/Processo:**
```
Entregas mais frequentes e previsíveis. Menos acúmulo de trabalho em PRs grandes. Desenvolvedores mais engajados com qualidade do código.
```

**Complexidade:** 8

---

### Exemplo 3.3: Qualidade de Testes

**Título da Melhoria:**
```
Kaizen - Aumentar cobertura de testes automatizados
```

**Processo/Área a Melhorar:**
```
Suite de testes automatizados do projeto principal. Atualmente a cobertura é baixa e os testes existentes são lentos e flaky (instáveis).
```

**Situação Atual (Baseline):**
```
- Cobertura de código: 35%
- Testes flaky: 15% dos testes falham intermitentemente
- Tempo de execução da suite completa: 25 minutos
- Apenas testes de integração, poucos testes unitários
- Nenhum teste E2E automatizado
```

**Meta Desejada:**
```
- Cobertura de código: 70%
- Testes flaky: < 1%
- Tempo de execução: < 10 minutos
- Pirâmide de testes balanceada (70% unit, 20% integration, 10% E2E)
- Testes E2E para fluxos críticos
```

**Métricas de Sucesso:**
```
1. Percentual de cobertura de código
2. Taxa de testes flaky
3. Tempo de execução da suite
4. Bugs encontrados em produção (redução esperada)
```

**Impacto Esperado no Time/Processo:**
```
Maior confiança para fazer refatorações e alterações. Menos bugs em produção. Desenvolvedores mais produtivos com feedback rápido dos testes.
```

**Complexidade:** 21

---

## 4. Fix/Bug/Incidente - Correção de bugs e incidentes

### Exemplo 4.1: Erro Crítico em Produção

**Título do Bug/Incidente:**
```
Fix - Erro 500 ao processar pagamentos com cartão internacional
```

**Descrição do Bug/Erro:**
```
Usuários não conseguem finalizar compras quando utilizam cartões de crédito emitidos fora do Brasil. O erro ocorre no momento da validação do pagamento, antes mesmo de enviar para o gateway.
```

**Passos para Reproduzir:**
```
1. Acessar a plataforma e adicionar produtos ao carrinho
2. Ir para a página de checkout
3. Selecionar pagamento com cartão de crédito
4. Informar dados de um cartão internacional (ex: emitido nos EUA)
5. Clicar em "Finalizar Compra"
```

**Comportamento Esperado:**
```
O pagamento deveria ser processado normalmente, enviado ao gateway Stripe, e retornar com status de aprovado ou recusado conforme resposta do gateway.
```

**Comportamento Atual (O que está acontecendo):**
```
A aplicação retorna erro 500 Internal Server Error imediatamente após clicar em finalizar. O erro ocorre antes de chegar ao gateway de pagamento. O usuário vê uma tela genérica de erro.
```

**Ambiente Afetado:** Produção

**Severidade:** Crítica

**Logs/Evidências:**
```
[2024-01-15 14:32:15] ERROR PaymentService - Unexpected error validating card
java.lang.NullPointerException: Cannot invoke "String.length()" because "countryCode" is null
    at com.app.payment.CardValidator.validateInternational(CardValidator.java:45)
    at com.app.payment.PaymentService.processPayment(PaymentService.java:123)
    at com.app.checkout.CheckoutController.finalize(CheckoutController.java:89)
```

**Complexidade:** 5

---

### Exemplo 4.2: Bug de Interface

**Título do Bug/Incidente:**
```
Fix - Botão de submit fica desabilitado após erro de validação
```

**Descrição do Bug/Erro:**
```
No formulário de cadastro, quando o usuário comete um erro de validação (ex: email inválido) e corrige o campo, o botão de "Cadastrar" permanece desabilitado, impedindo o envio do formulário.
```

**Passos para Reproduzir:**
```
1. Acessar página de cadastro (/cadastro)
2. Preencher todos os campos corretamente, exceto o email
3. No campo email, digitar um valor inválido (ex: "teste@")
4. Clicar em "Cadastrar"
5. Observar mensagem de erro no campo email
6. Corrigir o email para um valor válido (ex: "teste@email.com")
7. Tentar clicar em "Cadastrar" novamente
```

**Comportamento Esperado:**
```
Após corrigir o campo com erro, o botão deveria voltar a ficar habilitado e permitir o envio do formulário.
```

**Comportamento Atual (O que está acontecendo):**
```
O botão "Cadastrar" permanece desabilitado (cinza) mesmo após corrigir o email. O usuário precisa recarregar a página e preencher tudo novamente para conseguir cadastrar.
```

**Ambiente Afetado:** Todos

**Severidade:** Média

**Logs/Evidências:**
```
Console do navegador mostra:
[React Warning] State update on unmounted component in FormValidator
O estado "isFormValid" não está sendo atualizado corretamente após onChange.
```

**Complexidade:** 3

---

### Exemplo 4.3: Problema de Performance

**Título do Bug/Incidente:**
```
Fix - Tela de listagem de produtos demora mais de 30 segundos para carregar
```

**Descrição do Bug/Erro:**
```
A página de listagem de produtos está extremamente lenta, chegando a timeout em alguns casos. O problema parece ter começado após a última atualização que adicionou filtros avançados.
```

**Passos para Reproduzir:**
```
1. Acessar a loja como usuário não logado
2. Clicar em "Produtos" no menu principal
3. Aguardar carregamento da página
4. Observar que a página demora mais de 30 segundos ou dá timeout
```

**Comportamento Esperado:**
```
A listagem de produtos deveria carregar em no máximo 3 segundos, exibindo os produtos com paginação de 20 itens por página.
```

**Comportamento Atual (O que está acontecendo):**
```
A página demora entre 30 segundos e 2 minutos para carregar. Em alguns casos, dá timeout (504 Gateway Timeout). O servidor fica com CPU alta durante a requisição.
```

**Ambiente Afetado:** Produção

**Severidade:** Alta

**Logs/Evidências:**
```
Query lenta identificada no slow query log:
SELECT * FROM produtos p
LEFT JOIN categorias c ON p.categoria_id = c.id
LEFT JOIN imagens i ON p.id = i.produto_id
LEFT JOIN precos pr ON p.id = pr.produto_id
WHERE p.ativo = 1
ORDER BY p.created_at DESC;

Tempo de execução: 45.234s
Rows examined: 2.500.000

APM mostra:
- Endpoint: GET /api/produtos
- P95 latency: 35000ms
- Memory usage spike durante a query
```

**Complexidade:** 8

---

### Exemplo 4.4: Bug de Integração

**Título do Bug/Incidente:**
```
Fix - Webhook do Stripe não está atualizando status dos pedidos
```

**Descrição do Bug/Erro:**
```
Após o cliente realizar pagamento via cartão, o status do pedido não está sendo atualizado de "pendente_pagamento" para "pago". O webhook do Stripe está retornando 200, mas o pedido não é processado.
```

**Passos para Reproduzir:**
```
1. Criar um pedido na plataforma
2. Realizar pagamento com cartão de teste do Stripe (4242 4242 4242 4242)
3. Aguardar confirmação do pagamento no Stripe Dashboard
4. Verificar status do pedido na plataforma
```

**Comportamento Esperado:**
```
Quando o Stripe envia o webhook "payment_intent.succeeded", o sistema deveria atualizar o pedido para status "pago" e enviar email de confirmação ao cliente.
```

**Comportamento Atual (O que está acontecendo):**
```
O webhook é recebido (retorna 200), mas o pedido permanece como "pendente_pagamento". O cliente não recebe email de confirmação. No Stripe Dashboard, o evento aparece como "delivered" com sucesso.
```

**Ambiente Afetado:** Homologação

**Severidade:** Alta

**Logs/Evidências:**
```
[2024-01-15 10:15:32] INFO WebhookController - Received Stripe webhook: payment_intent.succeeded
[2024-01-15 10:15:32] INFO WebhookController - Payment Intent ID: pi_3MqRnK2eZvKYlo2C1234abcd
[2024-01-15 10:15:32] DEBUG OrderService - Searching order by payment_intent_id
[2024-01-15 10:15:32] WARN OrderService - No order found for payment_intent_id: pi_3MqRnK2eZvKYlo2C1234abcd
[2024-01-15 10:15:32] INFO WebhookController - Webhook processed successfully

Observação: O pedido está salvo com campo "stripe_payment_intent" ao invés de "payment_intent_id"
```

**Complexidade:** 5

---

## Dicas de Uso

1. **Copie e cole** os exemplos diretamente nos campos do formulário
2. **Adapte os exemplos** para o contexto real do seu projeto
3. **Teste diferentes combinações** de campos opcionais
4. **Use exemplos simples primeiro** para validar o funcionamento
5. **Aumente a complexidade** gradualmente para testar limites

---

## Checklist de Testes

- [ ] Business com API GET
- [ ] Business com API POST
- [ ] Business com API PUT
- [ ] Business com API PATCH
- [ ] Business com API DELETE
- [ ] Business SEM API
- [ ] Business com dependências
- [ ] Spike com output "Documento de decisão"
- [ ] Spike com output "POC funcional"
- [ ] Spike com output "Relatório técnico"
- [ ] Kaizen com alta complexidade
- [ ] Kaizen com baixa complexidade
- [ ] Fix/Bug severidade Crítica
- [ ] Fix/Bug severidade Alta
- [ ] Fix/Bug severidade Média
- [ ] Fix/Bug severidade Baixa
- [ ] Fix/Bug em ambiente Produção
- [ ] Fix/Bug em ambiente Homologação
