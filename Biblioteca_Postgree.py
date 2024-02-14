from multiprocessing import connection
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from psycopg2 import connect
from psycopg2 import connect, Error
import psycopg2
import bcrypt

# Função para conectar ao banco de dados PostgreSQL
def connect_to_postgresql():
    try:
        conn = psycopg2.connect(
            dbname="Biblioteca",
            user="postgres",
            password="gerador8",
            host="localhost"
        )
        print("Conexão bem-sucedida ao banco de dados PostgreSQL!")
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")

# Função para registrar um novo usuário no banco de dados
def register_user(conn, username, password):
    try:
        cursor = conn.cursor()
        # Hash da senha antes de armazenar no banco de dados
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        print("Usuário registrado com sucesso!")
    except psycopg2.Error as e:
        print(f"Erro ao registrar usuário: {e}")

# Função para verificar as credenciais de um usuário no banco de dados
def verify_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        password_hash = cursor.fetchone()
        if password_hash:
            if bcrypt.checkpw(password.encode('utf-8'), password_hash[0].encode('utf-8')):
                print("Credenciais de usuário válidas. Login bem-sucedido!")
                return True
            else:
                print("Nome de usuário ou senha inválidos.")
                return False
        else:
            print("Usuário não encontrado.")
            return False
    except (psycopg2.Error, TypeError) as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

# Função para lidar com o registro de um novo usuário
def register_new_user():
    def register():
        username = username_var.get()
        password = password_var.get()
        confirm_password = confirm_password_var.get()

        if not (username and password and confirm_password):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        if password != confirm_password:
            messagebox.showwarning("Aviso", "As senhas não coincidem.")
            return

        # Conectar ao banco de dados
        conn = connect_to_postgresql()

        # Registrar o novo usuário
        register_user(conn, username, password)

        # Fechar a conexão com o banco de dados
        conn.close()

        # Fechar a janela de registro
        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Registrar Novo Usuário")

    username_var = tk.StringVar(register_window)
    password_var = tk.StringVar(register_window)
    confirm_password_var = tk.StringVar(register_window)

    ttk.Label(register_window, text="Nome de Usuário:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(register_window, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(register_window, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(register_window, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(register_window, text="Confirmar Senha:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(register_window, textvariable=confirm_password_var, show="*").grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(register_window, text="Registrar", command=register).grid(row=3, columnspan=2, pady=10)


# Função para verificar as credenciais de um usuário no banco de dados
def verify_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        password_hash = cursor.fetchone()
        if password_hash:
            if bcrypt.checkpw(password.encode('utf-8'), password_hash[0].encode('utf-8')):
                print("Credenciais de usuário válidas. Login bem-sucedido!")
                return True
            else:
                print("Nome de usuário ou senha inválidos.")
                return False
        else:
            print("Usuário não encontrado.")
            return False
    except (psycopg2.Error, TypeError) as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

# Função para lidar com o login de usuário
def login_user():
    username = username_var.get()
    password = password_var.get()

    if not (username and password):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    # Conectar ao banco de dados
    conn = connect_to_postgresql()

    # Verificar as credenciais do usuário
    if verify_user(conn, username, password):
        # Fechar a conexão com o banco de dados
        conn.close()
        root.destroy()

# Criar a janela de login
root = tk.Tk()
root.title("Autenticação de Usuário")

username_var = tk.StringVar(root)
password_var = tk.StringVar(root)

ttk.Label(root, text="Nome de Usuário:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(root, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

ttk.Button(root, text="Login", command=login_user).grid(row=2, columnspan=2, pady=10)
ttk.Button(root, text="Registrar Novo Usuário", command=register_new_user).grid(row=3, columnspan=2, pady=10)

root.mainloop()
    


def exibir_detalhes():
    selected_item = tree.focus()
    if not selected_item:
        tk.messagebox.showwarning("Aviso", "Por favor, selecione um livro")
        return

    livro_id = int(tree.item(selected_item)['text'])

    sql = "SELECT * FROM livros WHERE id = %s"
    postgres_cursor.execute(sql, (livro_id,))
    livro = postgres_cursor.fetchone()

    if not livro:
        tk.messagebox.showwarning("Aviso", "Livro selecionado inválido")
        return

    detalhes_janela = tk.Toplevel(root)
    detalhes_janela.title("Detalhes do Livro")

    ttk.Label(detalhes_janela, text="ID: " + str(livro[0]), font=("Helvetica", 12)).pack(pady=5)
    ttk.Label(detalhes_janela, text="Título: " + livro[1], font=("Helvetica", 14, "bold")).pack(pady=5)
    ttk.Label(detalhes_janela, text="ISBN: " + livro[2], font=("Helvetica", 12)).pack(pady=5)
    ttk.Label(detalhes_janela, text="Ano de Publicação: " + str(livro[3]), font=("Helvetica", 12)).pack(pady=5)
    ttk.Label(detalhes_janela, text="Editora: " + livro[4], font=("Helvetica", 12)).pack(pady=5)


def remover_livro():
    selected_item = tree.focus()
    if not selected_item:
        tk.messagebox.showwarning("Aviso", "Por favor, selecione um livro")
        return

    livro_id = int(tree.item(selected_item)['text'])

    
    sql_remove_livro = "DELETE FROM livros WHERE id = %s"
    postgres_cursor.execute(sql_remove_livro, (livro_id,))
    conn.commit()

    tree.delete(selected_item)


def adicionar_livro():
    adicionar_janela = tk.Toplevel(root)
    adicionar_janela.title("Adicionar Livro")

    titulo_var = tk.StringVar(adicionar_janela)
    isbn_var = tk.StringVar(adicionar_janela)
    ano_var = tk.StringVar(adicionar_janela)
    editora_var = tk.StringVar(adicionar_janela)

    def adicionar():
        titulo = titulo_var.get()
        isbn = isbn_var.get()
        ano = ano_var.get()
        editora = editora_var.get()

        if not (titulo and isbn and ano and editora):
            tk.messagebox.showwarning("Aviso", "Por favor, preencha todos os campos")
            return

        sql = "INSERT INTO livros (titulo, isbn, ano_publicacao, editora) VALUES (%s, %s, %s, %s)"
        val = (titulo, isbn, int(ano), editora)
        postgres_cursor.execute(sql, val)
        conn.commit()

        tree.insert("", "end", text=str(postgres_cursor.lastrowid),
                    values=(postgres_cursor.lastrowid, titulo, "Disponível", ano, editora))

        adicionar_janela.destroy()

    ttk.Label(adicionar_janela, text="Título:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(adicionar_janela, textvariable=titulo_var).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(adicionar_janela, text="ISBN:").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(adicionar_janela, textvariable=isbn_var).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(adicionar_janela, text="Ano de Publicação:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(adicionar_janela, textvariable=ano_var).grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(adicionar_janela, text="Editora:").grid(row=3, column=0, padx=5, pady=5)
    ttk.Entry(adicionar_janela, textvariable=editora_var).grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(adicionar_janela, text="Adicionar", command=adicionar).grid(row=4, columnspan=2, pady=10)
    
    
def editar_livro():
    selected_item = tree.focus()
    if not selected_item:
        tk.messagebox.showwarning("Aviso", "Por favor, selecione um livro para editar")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]
    livro_isbn = tree.item(selected_item)['values'][2]
    livro_ano = tree.item(selected_item)['values'][3]
    livro_editora = tree.item(selected_item)['values'][4]

    editar_janela = tk.Toplevel(root)
    editar_janela.title("Editar Livro")

    titulo_var = tk.StringVar(editar_janela, value=livro_titulo)
    isbn_var = tk.StringVar(editar_janela, value=livro_isbn)
    ano_var = tk.StringVar(editar_janela, value=livro_ano)
    editora_var = tk.StringVar(editar_janela, value=livro_editora)

    def atualizar():
        novo_titulo = titulo_var.get()
        novo_isbn = isbn_var.get()
        novo_ano = ano_var.get()
        nova_editora = editora_var.get()

        if not (novo_titulo and novo_isbn and novo_ano and nova_editora):
            tk.messagebox.showwarning("Aviso", "Por favor, preencha todos os campos")
            return

        sql_update_livro = "UPDATE livros SET titulo = %s, isbn = %s, ano_publicacao = %s, editora = %s WHERE id = %s"
        val = (novo_titulo, novo_isbn, novo_ano, nova_editora, livro_id)
        postgres_cursor.execute(sql_update_livro, val)
        conn.commit()

        messagebox.showinfo("Sucesso", "Informações do livro atualizadas com sucesso.")
        editar_janela.destroy()

        
        tree.item(selected_item, values=(livro_id, novo_titulo, "Disponível", novo_ano, nova_editora))

    ttk.Label(editar_janela, text="Título:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=titulo_var).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(editar_janela, text="ISBN:").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=isbn_var).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(editar_janela, text="Ano de Publicação:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=ano_var).grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(editar_janela, text="Editora:").grid(row=3, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=editora_var).grid(row=3, column=1, padx=5, pady=5)

    ttk.Button(editar_janela, text="Atualizar", command=atualizar).grid(row=4, columnspan=2, pady=10)


def emprestar_livro():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Por favor, selecione um livro para emprestar.")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]

    sql = "SELECT * FROM emprestimos WHERE livro_id = %s AND status = 'pendente'"
    postgres_cursor.execute(sql, (livro_id,))
    emprestimos_pendentes = postgres_cursor.fetchall()

    if emprestimos_pendentes:
        messagebox.showwarning("Aviso", "Este livro já está emprestado.")
        return

    emprestar_janela = tk.Toplevel(root)
    emprestar_janela.title("Empréstimo de Livro")

    ttk.Label(emprestar_janela, text="Título do Livro:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Label(emprestar_janela, text=livro_titulo).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(emprestar_janela, text="Data do Empréstimo:").grid(row=1, column=0, padx=5, pady=5)
    data_emprestimo_entry = ttk.Entry(emprestar_janela)
    data_emprestimo_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(emprestar_janela, text="Data de Devolução:").grid(row=2, column=0, padx=5, pady=5)
    data_devolucao_entry = ttk.Entry(emprestar_janela)
    data_devolucao_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(emprestar_janela, text="Pessoa que está emprestando:").grid(row=3, column=0, padx=5, pady=5)
    pessoa_entry = ttk.Entry(emprestar_janela)
    pessoa_entry.grid(row=3, column=1, padx=5, pady=5)

    def realizar_emprestimo():
        data_emprestimo = data_emprestimo_entry.get()
        data_devolucao = data_devolucao_entry.get()
        pessoa = pessoa_entry.get()

        data_emprestimo = datetime.strptime(data_emprestimo, "%d/%m/%Y").strftime("%Y-%m-%d")
        data_devolucao = datetime.strptime(data_devolucao, "%d/%m/%Y").strftime("%Y-%m-%d")

        if not (data_emprestimo and data_devolucao and pessoa):
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        sql = "INSERT INTO emprestimos (livro_id, data_emprestimo, data_devolucao, pessoa_emprestimo, status) VALUES (%s, %s, %s, %s, %s)"
        val = (livro_id, data_emprestimo, data_devolucao, pessoa, "pendente")
        postgres_cursor.execute(sql, val)
        conn.commit()

        messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso.")
        emprestar_janela.destroy()

        for item in tree.get_children():
            if tree.item(item)['text'] == str(livro_id):
                tree.item(item, values=(tree.item(item)['values'][0], livro_titulo, "Emprestado", tree.item(item)['values'][3], tree.item(item)['values'][4]))

        
        sql_update_status = "UPDATE livros SET status = 'Emprestado' WHERE id = %s"
        postgres_cursor.execute(sql_update_status, (livro_id,))
        conn.commit()

    ttk.Button(emprestar_janela, text="Realizar Empréstimo", command=realizar_emprestimo).grid(row=4, columnspan=2, pady=10)


def devolver_livro():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Por favor, selecione um livro para devolver.")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]

    
    sql_update_status = "UPDATE livros SET status = 'Disponível' WHERE id = %s"
    postgres_cursor.execute(sql_update_status, (livro_id,))
    conn.commit()

    sql_remove_emprestimo = "DELETE FROM emprestimos WHERE livro_id = %s"
    postgres_cursor.execute(sql_remove_emprestimo, (livro_id,))
    conn.commit()

    messagebox.showinfo("Sucesso", f"O livro '{livro_titulo}' foi devolvido com sucesso.")
    tree.item(selected_item, values=(tree.item(selected_item)['values'][0], livro_titulo, "Disponível", tree.item(selected_item)['values'][3], tree.item(selected_item)['values'][4]))


def exibir_emprestimos_pendentes():
    pendentes_janela = tk.Toplevel(root)
    pendentes_janela.title("Empréstimos Pendentes")

    sql = "SELECT * FROM emprestimos WHERE status = 'pendente'"
    postgres_cursor.execute(sql)
    emprestimos = postgres_cursor.fetchall()

    ttk.Label(pendentes_janela, text="Empréstimos Pendentes:", font=("Helvetica", 14, "bold")).pack(pady=5)

    for emprestimo in emprestimos:
        livro_id = emprestimo[1]
        sql = "SELECT titulo FROM livros WHERE id = %s"
        postgres_cursor.execute(sql, (livro_id,))
        livro_titulo = postgres_cursor.fetchone()[0]

        ttk.Label(pendentes_janela, text=f"Livro: {livro_titulo} | Pessoa: {emprestimo[4]} | Data de Devolução: {emprestimo[3]}").pack(pady=2)


try:
    conn = psycopg2.connect(
        dbname="Biblioteca",
        user="postgres",
        password="gerador8",
        host="localhost"
    )
    print("Conexão bem-sucedida ao banco de dados PostgreSQL!")

    
    postgres_cursor = conn.cursor()

    
    root = tk.Tk()
    root.title("Biblioteca Gabriel")

    tree = ttk.Treeview(root, columns=("ID", "Título", "Status", "Ano de Publicação", "Editora"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Título", text="Título")
    tree.heading("Status", text="Status")
    tree.heading("Ano de Publicação", text="Ano de Publicação")
    tree.heading("Editora", text="Editora")
    tree.pack(padx=10, pady=10)

  
    sql = "SELECT * FROM livros"
    postgres_cursor.execute(sql)
    livros = postgres_cursor.fetchall()
    for livro in livros:
        tree.insert("", "end", text=str(livro[0]), values=(livro[0], livro[1], "Disponível", livro[3], livro[4]))

    
    btn_exibir_detalhes = ttk.Button(root, text="Exibir Detalhes", command=exibir_detalhes)
    btn_exibir_detalhes.pack(side=tk.LEFT, padx=5, pady=10)

    btn_remover_livro = ttk.Button(root, text="Remover Livro", command=remover_livro)
    btn_remover_livro.pack(side=tk.LEFT, padx=5, pady=10)

    btn_adicionar_livro = ttk.Button(root, text="Adicionar Livro", command=adicionar_livro)
    btn_adicionar_livro.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_editar_livro = ttk.Button(root, text="Editar Livro", command=editar_livro)
    btn_editar_livro.pack(side=tk.LEFT, padx=5, pady=10)
    
    btn_emprestar_livro = ttk.Button(root, text="Emprestar Livro", command=emprestar_livro)
    btn_emprestar_livro.pack(side=tk.LEFT, padx=5, pady=10)

    btn_devolver_livro = ttk.Button(root, text="Devolver Livro", command=devolver_livro)
    btn_devolver_livro.pack(side=tk.LEFT, padx=5, pady=10)

    btn_emprestimos_pendentes = ttk.Button(root, text="Empréstimos Pendentes", command=exibir_emprestimos_pendentes)
    btn_emprestimos_pendentes.pack(side=tk.LEFT, padx=5, pady=10)

    root.mainloop()

except psycopg2.Error as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")
