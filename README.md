# 🥗 Daily Diet API

API RESTful para controle de dieta diária, desenvolvida com Flask como parte do desafio da [Rocketseat](https://www.rocketseat.com.br/). Permite que usuários registrem, editem e acompanhem suas refeições, com controle de autenticação e persistência em banco de dados MySQL.

---

## 🚀 Tecnologias

- **Python 3.13**
- **Flask** — framework web
- **Flask-SQLAlchemy** — ORM para banco de dados
- **Flask-Login** — gerenciamento de sessão e autenticação
- **bcrypt** — hash seguro de senhas
- **MySQL** — banco de dados relacional
- **Docker / Docker Compose** — containerização do banco de dados

---

## 📋 Funcionalidades

- Cadastro e autenticação de usuários
- Registro de refeições com nome, descrição, data/hora e indicador de dieta (`on_diet`)
- Listagem de todas as refeições do usuário autenticado
- Visualização de uma refeição específica
- Edição e exclusão de refeições
- Isolamento de dados por usuário (cada usuário acessa apenas suas próprias refeições)
- Controle de acesso por roles (`user` / `admin`)


---

## ⚙️ Como rodar localmente

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose

### 1. Clone o repositório

```bash
git clone https://github.com/leonardoprokopowiskii/daily-diet-api.git
cd daily-diet-api
```

### 2. Suba o banco de dados com Docker

```bash
docker compose up -d
```

### 3. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Inicie a aplicação

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

> **Nota:** Na primeira execução, crie as tabelas no banco rodando no shell Python:
> ```python
> from app import app
> from database import db
> with app.app_context():
>     db.create_all()
> ```

---

## 🔌 Endpoints

### Usuários

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `POST` | `/user` | Cria um novo usuário | ❌ |
| `GET` | `/user/<id>` | Busca dados de um usuário | ✅ |
| `PUT` | `/user` | Atualiza senha do usuário autenticado | ✅ |
| `DELETE` | `/user/<id>` | Remove um usuário (somente admin) | ✅ |
| `POST` | `/login` | Autentica o usuário | ❌ |
| `GET` | `/logout` | Encerra a sessão | ✅ |

### Refeições

| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| `POST` | `/meal` | Registra uma nova refeição | ✅ |
| `GET` | `/meal` | Lista todas as refeições do usuário | ✅ |
| `GET` | `/meal/<id>` | Detalha uma refeição específica | ✅ |
| `PUT` | `/meal/<id>` | Atualiza uma refeição | ✅ |
| `DELETE` | `/meal/<id>` | Remove uma refeição | ✅ |

---

## 📦 Exemplos de requisição

### Criar usuário
```json
POST /user
{
  "username": "joao",
  "password": "senha123"
}
```

### Criar refeição
```json
POST /meal
{
  "name": "Almoço saudável",
  "description": "Arroz integral, frango e salada",
  "date_meal": "2025-04-27T12:00:00",
  "on_diet": true
}
```

---

## 🔒 Autenticação

A API utiliza sessões via `Flask-Login`. Faça login em `/login` antes de acessar as rotas protegidas. As senhas são armazenadas com hash bcrypt.

---

## 📌 Observações

- O campo `on_diet` indica se a refeição está dentro da dieta (`true`) ou não (`false`).
- Cada usuário só tem acesso às suas próprias refeições.
- A role `admin` é necessária para deletar outros usuários.

---

Feito com 💜 como parte do desafio da [Rocketseat](https://www.rocketseat.com.br/).