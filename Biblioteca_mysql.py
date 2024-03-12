import tkinter as tk
from tkinter import ttk
import mysql.connector
style = ttk.Style()
style.theme_use('clam')
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import bcrypt
import sys
from mysql.connector import Error
def on_closing():
    if messagebox.askokcancel("Fechar", "Tem certeza que deseja sair?"):
        root.destroy()  
        sys.exit(0)  

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="gerador8",
    database="biblioteca_mysql"
)
print("Conexão bem-sucedida ao banco de dados MySQL!")




def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="gerador8",
            database="biblioteca_mysql"
        )
        if conn.is_connected():
            print("Conexão bem-sucedida ao banco de dados MySQL!")
            return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")

def register_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
        conn.commit()
        print("Usuário registrado com sucesso!")
    except Error as e:
        print(f"Erro ao registrar usuário: {e}")

def verify_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        password_hash = cursor.fetchone()
        if password_hash:
            if password == password_hash[0]:
                print("Credenciais de usuário válidas. Login bem-sucedido!")
                return True
            else:
                print("Nome de usuário ou senha inválidos.")
                return False
        else:
            print("Usuário não encontrado.")
            return False
    except Error as e:
        print(f"Erro ao verificar usuário: {e}")
        return False

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

        conn = connect_to_mysql()
        register_user(conn, username, password)
        conn.close()
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

def login_user():
    username = username_var.get()
    password = password_var.get()

    if not (username and password):
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    conn = connect_to_mysql()
    if verify_user(conn, username, password):
        conn.close()
        root.destroy()

root = tk.Tk()
root.title("Autenticação de Usuário")
username_var = tk.StringVar(root)
password_var = tk.StringVar(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
ttk.Label(root, text="Nome de Usuário:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=username_var).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(root, text="Senha:").grid(row=1, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=5)

ttk.Button(root, text="Login", command=login_user).grid(row=2, columnspan=2, pady=10)
ttk.Button(root, text="Registrar Novo Usuário", command=register_new_user).grid(row=3, columnspan=2, pady=10)

root.mainloop()








mycursor = mydb.cursor()


root = tk.Tk()
root.title("Biblioteca Gabriel")


tree = ttk.Treeview(root, columns=("ID", "Título", "Status", "Ano de Publicação", "Editora"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Título", text="Título")
tree.heading("Status", text="Status")
tree.heading("Ano de Publicação", text="Ano de Publicação")
tree.heading("Editora", text="Editora")
tree.pack(padx=10, pady=10)




def exibir_detalhes():
    selected_item = tree.focus()
    
    if not selected_item:
        tk.messagebox.showwarning("Aviso", "Por favor, selecione um livro")
        return
    
    livro_id = int(tree.item(selected_item)['text'])
    
    sql = "SELECT * FROM livros WHERE id = %s"
    mycursor.execute(sql, (livro_id,))
    livro = mycursor.fetchone()
    
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

  
    sql_check_emprestimos = "SELECT * FROM emprestimos WHERE livro_id = %s AND status = 'pendente'"
    mycursor.execute(sql_check_emprestimos, (livro_id,))
    emprestimos_pendentes = mycursor.fetchall()

    if emprestimos_pendentes:
        tk.messagebox.showwarning("Aviso", "Este livro está emprestado e não pode ser removido.")
        return

   
    sql_remove_livro = "DELETE FROM livros WHERE id = %s"
    mycursor.execute(sql_remove_livro, (livro_id,))
    mydb.commit()
    
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
        mycursor.execute(sql, val)
        mydb.commit()
        
        tree.insert("", "end", text=str(mycursor.lastrowid), values=(mycursor.lastrowid, titulo, "Disponível", ano, editora))
        
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
        messagebox.showwarning("Aviso", "Por favor, selecione um livro para editar.")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]
    livro_ano = tree.item(selected_item)['values'][3]
    livro_editora = tree.item(selected_item)['values'][4]

    
    editar_janela = tk.Toplevel(root)
    editar_janela.title("Editar Livro")

    
    novo_titulo_var = tk.StringVar(editar_janela, value=livro_titulo)
    novo_ano_var = tk.StringVar(editar_janela, value=livro_ano)
    nova_editora_var = tk.StringVar(editar_janela, value=livro_editora)

    
    def aplicar():
        novo_titulo = novo_titulo_var.get()
        novo_ano = novo_ano_var.get()
        nova_editora = nova_editora_var.get()

        
        sql = "UPDATE livros SET titulo = %s, ano_publicacao = %s, editora = %s WHERE id = %s"
        val = (novo_titulo, novo_ano, nova_editora, livro_id)
        mycursor.execute(sql, val)
        mydb.commit()

        
        tree.item(selected_item, values=(livro_id, novo_titulo, "Disponível", novo_ano, nova_editora))

        messagebox.showinfo("Sucesso", "Livro editado com sucesso.")
        editar_janela.destroy()

    # Elementos da janela de edição
    ttk.Label(editar_janela, text="Novo Título:").grid(row=0, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=novo_titulo_var).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(editar_janela, text="Novo Ano de Publicação:").grid(row=1, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=novo_ano_var).grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(editar_janela, text="Nova Editora:").grid(row=2, column=0, padx=5, pady=5)
    ttk.Entry(editar_janela, textvariable=nova_editora_var).grid(row=2, column=1, padx=5, pady=5)

    ttk.Button(editar_janela, text="Aplicar", command=aplicar).grid(row=3, columnspan=2, pady=10)

def emprestar_livro():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Por favor, selecione um livro para emprestar.")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]

    sql = "SELECT * FROM emprestimos WHERE livro_id = %s AND status = 'pendente'"
    mycursor.execute(sql, (livro_id,))
    emprestimos_pendentes = mycursor.fetchall()

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
        mycursor.execute(sql, val)
        mydb.commit()

        messagebox.showinfo("Sucesso", "Empréstimo realizado com sucesso.")
        emprestar_janela.destroy()

        for item in tree.get_children():
            if tree.item(item)['text'] == str(livro_id):
                tree.item(item, values=(tree.item(item)['values'][0], livro_titulo, "Emprestado", tree.item(item)['values'][3], tree.item(item)['values'][4]))

        
        sql_update_status = "UPDATE livros SET status = 'Emprestado' WHERE id = %s"
        mycursor.execute(sql_update_status, (livro_id,))
        mydb.commit()

    ttk.Button(emprestar_janela, text="Realizar Empréstimo", command=realizar_emprestimo).grid(row=4, columnspan=2, pady=10)



def devolver_livro():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Aviso", "Por favor, selecione um livro para devolver.")
        return

    livro_id = int(tree.item(selected_item)['text'])
    livro_titulo = tree.item(selected_item)['values'][1]

    
    sql_update_status = "UPDATE livros SET status = 'Disponível' WHERE id = %s"
    mycursor.execute(sql_update_status, (livro_id,))
    mydb.commit()
    
    sql_remove_emprestimo = "DELETE FROM emprestimos WHERE livro_id = %s"
    mycursor.execute(sql_remove_emprestimo, (livro_id,))
    mydb.commit()
    
    messagebox.showinfo("Sucesso", f"O livro '{livro_titulo}' foi devolvido com sucesso.")
    tree.item(selected_item, values=(tree.item(selected_item)['values'][0], livro_titulo, "Disponível", tree.item(selected_item)['values'][3], tree.item(selected_item)['values'][4]))


btn_devolver_livro = ttk.Button(root, text="Devolver Livro", command=devolver_livro)
btn_devolver_livro.pack(side=tk.LEFT, padx=5, pady=10)  




def exibir_emprestimos_pendentes():
    pendentes_janela = tk.Toplevel(root)
    pendentes_janela.title("Empréstimos Pendentes")

    sql = "SELECT * FROM emprestimos WHERE status = 'pendente'"
    mycursor.execute(sql)
    emprestimos = mycursor.fetchall()

    ttk.Label(pendentes_janela, text="Empréstimos Pendentes:", font=("Helvetica", 14, "bold")).pack(pady=5)

    for emprestimo in emprestimos:
        livro_id = emprestimo[1]
        sql = "SELECT titulo FROM livros WHERE id = %s"
        mycursor.execute(sql, (livro_id,))
        livro_titulo = mycursor.fetchone()[0]

        ttk.Label(pendentes_janela, text=f"Livro: {livro_titulo} | Pessoa: {emprestimo[4]} | Data de Devolução: {emprestimo[3]}").pack(pady=2)


sql = "SELECT * FROM livros"
mycursor.execute(sql)
livros = mycursor.fetchall()
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

btn_emprestimos_pendentes = ttk.Button(root, text="Empréstimos Pendentes", command=exibir_emprestimos_pendentes)
btn_emprestimos_pendentes.pack(side=tk.LEFT, padx=5, pady=10)





root.mainloop()
