import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Imprime uma mensagem no início para verificar se o script foi iniciado
print("Iniciando execução do script...")

# Tenta conectar ao banco de dados
try:
    conn = sqlite3.connect('bd_Prefeituras.sql')  # Substitua 'example.db' pelo caminho do seu banco
    cursor = conn.cursor()
    print("Conexão com o banco de dados realizada com sucesso.")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

# Função para cadastrar usuário
def cadastrar_usuario(usuario, email, cpf, senha, id_empresa):
    print("Executando cadastro do usuário...")
    cursor.execute('''
        INSERT INTO Usuarios (usuario, email, cpf, senha, id_empresa, situacao, primeiroAcesso, limiteacesso)
        VALUES (?, ?, ?, ?, ?, 1, 1, 200)
    ''', (usuario, email, cpf, senha, id_empresa))
    conn.commit()
    print(f"Usuário '{usuario}' cadastrado com sucesso!")

# Função de login e controle de primeiro acesso e limite de acessos
def login(usuario, senha):
    print(f"Tentando login para o usuário: {usuario}")
    cursor.execute('''
        SELECT id, primeiroAcesso, limiteacesso FROM Usuarios WHERE usuario = ? AND senha = ? AND situacao = 1
    ''', (usuario, senha))
    user = cursor.fetchone()
    
    if user:
        user_id, primeiro_acesso, limite_acesso = user

        if primeiro_acesso == 1:
            print("Redefinição de senha necessária.")
            redefinir_senha(user_id, senha)
        elif limite_acesso <= 0:
            print("Limite de acesso esgotado. Redefinição de senha necessária.")
            redefinir_senha(user_id, senha)
        else:
            cursor.execute('''
                UPDATE Usuarios SET limiteacesso = limiteacesso - 1 WHERE id = ?
            ''', (user_id,))
            conn.commit()
            print(f"Bem-vindo, {usuario}! Limite de acesso restante: {limite_acesso - 1}")
    else:
        print("Usuário ou senha incorretos ou conta inativa.")

# Função para redefinir senha
def redefinir_senha(user_id, senha_atual):
    nova_senha = input("Digite sua nova senha: ")
    
    # Salvar senha atual no histórico
    cursor.execute('''
        INSERT INTO HistoricoSenhasUsuarios (senha_anterior, senha_Atual, dataAlteracao, id_usuario)
        VALUES (?, ?, ?, ?)
    ''', (senha_atual, nova_senha, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id))
    
    # Atualizar senha e resetar limite de acesso
    cursor.execute('''
        UPDATE Usuarios 
        SET senha = ?, primeiroAcesso = 0, limiteacesso = 200 
        WHERE id = ?
    ''', (nova_senha, user_id))
    
    conn.commit()
    print("Senha redefinida com sucesso.")

# Teste do cadastro e login ao iniciar o script
if __name__ == "__main__":
    print("Iniciando teste de cadastro e login...")
    cadastrar_usuario("admin", "admin@example.com", "12345678900", "senha123", 1)
    login("admin", "senha123")
    print("Teste finalizado.")
