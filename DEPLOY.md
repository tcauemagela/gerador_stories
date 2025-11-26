# 🚀 Guia de Deploy - Streamlit Cloud

## 📋 Informações do Repositório

**Repositório:** https://github.com/tcauemagela/gerador_historia_v2
**Branch:** master
**Arquivo principal:** `app.py`

---

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Acesse o Streamlit Cloud
1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub

### Passo 2: Criar Novo App
1. Clique em **"New app"** ou **"Deploy an app"**
2. Selecione **"From existing repo"**

### Passo 3: Configurar o App
Preencha os campos:

- **Repository:** `tcauemagela/gerador_historia_v2`
- **Branch:** `master`
- **Main file path:** `app.py`
- **App URL (custom):** Escolha um nome único (ex: `gerador-historias-v2`)

### Passo 4: Deploy
1. Clique em **"Deploy!"**
2. Aguarde o deploy (geralmente 2-5 minutos)
3. Seu app estará disponível em: `https://[seu-nome-escolhido].streamlit.app`

---

## 🔑 Configuração da API Key

### ⚠️ IMPORTANTE: Segurança

O arquivo `.env` com a API key está no repositório por conveniência, mas **NÃO é recomendado para produção**.

### ✅ Opção Recomendada: Usar Streamlit Secrets

Para maior segurança, configure a API key usando Streamlit Secrets:

1. No painel do Streamlit Cloud, acesse **"Settings"** → **"Secrets"**
2. Adicione:
```toml
ANTHROPIC_API_KEY = "sua-chave-api-aqui"
```
3. Salve as alterações
4. O app será redeployado automaticamente

### 📝 Ajustar o Código (Opcional)

Se usar Streamlit Secrets, modifique `config.py`:

```python
import streamlit as st

def get_api_key():
    # Prioriza Streamlit Secrets
    if hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
        return st.secrets['ANTHROPIC_API_KEY']
    # Fallback para .env
    return os.getenv("ANTHROPIC_API_KEY")
```

---

## 🔄 Atualizações Automáticas

O Streamlit Cloud está configurado para **auto-deploy**:

- ✅ Qualquer push para o branch `master` será deployado automaticamente
- ✅ O app será atualizado em poucos minutos
- ✅ Você receberá notificações sobre o status do deploy

---

## 📊 Monitoramento

### Logs e Métricas

1. Acesse o painel do Streamlit Cloud
2. Clique no seu app
3. Veja:
   - **Logs:** Erros e mensagens do sistema
   - **Metrics:** Uso de recursos, visitantes, etc.
   - **Settings:** Configurações, secrets, domínio customizado

---

## 🛠️ Troubleshooting

### App não está funcionando?

1. **Verifique os logs** no painel do Streamlit Cloud
2. **Confirme a API key** está configurada corretamente
3. **Verifique as dependências** em `requirements.txt`
4. **Teste localmente** primeiro: `streamlit run app.py`

### Erro de API Key?

```
❌ API Key inválida
```

**Solução:**
- Verifique se a API key está correta
- Use Streamlit Secrets ao invés do .env
- Obtenha nova chave em: https://console.anthropic.com/

### App muito lento?

- O plano gratuito tem recursos limitados
- Considere otimizar o código
- Upgrade para plano pago se necessário

---

## 🔗 Links Úteis

- **Repositório:** https://github.com/tcauemagela/gerador_historia_v2
- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Cloud:** https://share.streamlit.io/
- **Anthropic Console:** https://console.anthropic.com/

---

## 📞 Suporte

Se encontrar problemas:
1. Verifique este guia primeiro
2. Consulte a documentação oficial do Streamlit
3. Verifique os logs no painel do Streamlit Cloud

---

**✨ Seu app está pronto para o mundo! Boa sorte! 🚀**
