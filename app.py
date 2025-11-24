import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Função para criar o Banco de Dados ---
def init_db():
    conn = sqlite3.connect('meubairro.db')
    cursor = conn.cursor()
    # Cria a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prestadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            contato TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Rota da Página Inicial (Mostra os serviços) ---
@app.route('/')
def index():
    conn = sqlite3.connect('meubairro.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prestadores ORDER BY id DESC")
    prestadores = cursor.fetchall()
    conn.close()
    return render_template('index.html', prestadores=prestadores)

# --- Rota de Cadastro (Salva novos serviços) ---
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Pega os dados que a pessoa digitou no formulário
        nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        contato = request.form['contato']

        # Salva no banco de dados
        conn = sqlite3.connect('meubairro.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO prestadores (nome, categoria, descricao, contato) VALUES (?, ?, ?, ?)",
                       (nome, categoria, descricao, contato))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('cadastro.html')

# --- Inicia o Site ---
if __name__ == '__main__':
    init_db() # Garante que o banco existe antes de começar
    app.run(debug=True)