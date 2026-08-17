# Sistema de Gerenciamento de Biblioteca

Sistema desktop em Python para controle de acervo de um sebo: cadastro, edição e remoção de livros, empréstimo e devolução, com autenticação de usuário.

<br>

**Tela de login**

![Tela de Login](https://github.com/user-attachments/assets/5802a029-3927-4a49-8c8d-3adf3f849a6d)

**Tela principal**

![Tela do Programa](https://github.com/user-attachments/assets/058d25ca-61d7-4401-b1c3-8cfa14314c83)

<br>

## Descrição

Interface gráfica em Tkinter para operações de acervo: adição, remoção, edição, empréstimo e devolução de livros — com autenticação de usuário via bcrypt e persistência em MySQL.

## Linguagens e banco

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## Bibliotecas

- [tkinter](https://docs.python.org/pt-br/3/library/tkinter.html) — interface gráfica
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) — conexão com o banco
- [Pillow](https://pillow.readthedocs.io/en/stable/) — manipulação de imagens
- [bcrypt](https://pypi.org/project/bcrypt/) — hash de senha
- [datetime](https://docs.python.org/pt-br/3/library/datetime.html) — controle de datas de empréstimo

## Como configurar e rodar

### Pré-requisitos

- Python 3.10 ou superior
- MySQL Server 8+ rodando
- pip funcionando

### Instalar as dependências

```bash
pip install mysql-connector-python pillow bcrypt
```

### Configurar o banco de dados

```sql
CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    isbn VARCHAR(255),
    ano_publicacao INT,
    editora VARCHAR(255),
    estoque INT,
    status VARCHAR(50) DEFAULT 'Disponível'
);

CREATE TABLE emprestimos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INT,
    data_emprestimo DATE,
    data_devolucao DATE,
    pessoa_emprestimo VARCHAR(255),
    status VARCHAR(50),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);
```

(Opcional) Crie um usuário dedicado para a aplicação em vez de usar o root:

```sql
CREATE USER 'bibliotecario'@'localhost' IDENTIFIED BY 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON biblioteca.* TO 'bibliotecario'@'localhost';
FLUSH PRIVILEGES;
```

### Configurar a conexão

Em `database.py` (ou onde a conexão for feita), ajuste com suas credenciais:

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="bibliotecario",
    password="sua_senha_aqui",
    database="biblioteca"
)
```

---

Desenvolvido por **Gabriel Cortes Teixeira**.
[LinkedIn](https://www.linkedin.com/in/gabriel-cortes-teixeira-0b9a4722b/)
