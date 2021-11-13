import sqlite3

conn = sqlite3.connect('database.db')
print('Opened database successfully')

conn.execute('CREATE TABLE IF NOT EXISTS voluntarios (nome TEXT, email TEXT, atividade TEXT, telefone TEXT)')
print("Table created successfully")
conn.close()
