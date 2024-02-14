-- Database: Biblioteca
CREATE TABLE livros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    isbn VARCHAR(20),
    ano_publicacao INTEGER,
    editora VARCHAR(100)
);


CREATE TABLE emprestimos (
    id SERIAL PRIMARY KEY,
    livro_id INTEGER,
    data_emprestimo DATE,
    data_devolucao DATE,
    pessoa_emprestimo VARCHAR(255),
    status VARCHAR(20),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
