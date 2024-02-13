-- Database biblioteca

CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
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