from os import error
from flask import Flask, request, render_template
import database as database
import sqlite3 as db

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")


@app.route("/cadastrar", methods=['POST'])
def cadastrar():
    print('Clicou no cadastrar')

    nome = request.form['nome']
    email = request.form['email']
    atividade = request.form['atividade']

    if not nome and not email and not atividade:
        erro = 'nome, email e atividade são obrigatórios'
        return render_template("cadastro_erro.html", erro=erro)
    else:
        try:
            with db.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(f"SELECT * FROM voluntarios WHERE email = '{email}'")
                voluntario_cadastrado = cur.fetchone()
                if voluntario_cadastrado:
                    msg  = f'voluntario ja cadastrado com email {email}'
                    print(msg)
                    return render_template("cadastro_erro.html", erro=msg)

                cur.execute("INSERT INTO voluntarios (nome, email, atividade) VALUES (?,?,?)",(nome, email, atividade) )
                con.commit()
                return render_template("cadastro_sucesso.html")

        except Exception as e:
            print(f'Erro no cadastro {e}')
            return render_template("cadastro_erro.html")


@app.route("/admin", methods=['GET'])
def admin():
    with db.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM voluntarios ORDER BY ROWID DESC")
        voluntarios_db = cur.fetchall()
        voluntarios  = []
        for v in voluntarios_db:
            voluntarios.append({
                'nome': v[0],
                'email': v[1],
                'atividade': v[2]
            })
        return render_template("admin.html", voluntarios=voluntarios)


if __name__=="__main__":
    app.run(debug=True)
