# Trabalho de Back-end - Rede Raízes do Nordeste
**nome:** TIAGO HENRIQUE DOS SANTOS TIBURCIO
**RU:** 4692699

Esse projeto é uma API desenvolvida em Python com FastAPI para gerenciar os pedidos da lanchonete, focando na multicanalidade (App, Totem, etc) e segurança dos dados (LGPD).

## Como rodar o projeto na sua máquina:

1. **Criar o ambiente virtual:**
   ```bash
   python -m venv venv
   ```
2. **Ativar o ambiente:**
   * Windows: `.\venv\Scripts\activate`
   * Linux/Mac: `source venv/bin/activate`

3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Iniciar o servidor:**
   ```bash
   uvicorn main:app --reload
   ```

O banco de dados SQLite vai ser gerado automaticamente assim que o servidor ligar. Para testar os endpoints e fazer os fluxos, acesse: `http://127.0.0`.

Esse projeto foi desenvolvido para aprender FastAPI, autenticação JWT e integração com banco de dados.

## Tecnologias
- Python
- FastAPI
- SQLAlchemy
- JWT
- SQLite

## O que aprendi
- Criar rotas REST
- Fazer login com token
- Hash de senha
- Organização backend
