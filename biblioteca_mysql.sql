CREATE TABLE livros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    isbn VARCHAR(20),
    ano_publicacao INTEGER,
    editora VARCHAR(100),
    estoque INT,
    status VARCHAR(50)
);

CREATE TABLE emprestimos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    livro_id INTEGER,
    data_emprestimo DATE,
    data_devolucao DATE,
    pessoa_emprestimo VARCHAR(255),
    status VARCHAR(20),
    FOREIGN KEY (livro_id) REFERENCES livros(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
