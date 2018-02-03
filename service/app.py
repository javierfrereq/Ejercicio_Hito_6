from flask import Flask, jsonify 
from flask import Markup
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

db = SQLAlchemy()
db_preguntas = 'mysql://root:password@db/information_schema'
app.config['SQLALCHEMY_DATABASE_PREGUNTAS'] = db_preguntas
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def conexion():
    mysql_resultado = False
    
    db.session.query("1").from_statement("SELECT 1").all()
    try:
        if db.session.query("1").from_statement("SELECT 1").all():
            mysql_resultado = True
    except:
        pass

    if mysql_resultado:
        result = Markup('<span style="color: green;">Conexion exitosa a la Base</span>')
    else:
        result = Markup('<span style="color: red;">Error al conectarse a la Base</span>')

    return render_template('index.html', result=result)

@app.route('/status')
def statusok():
    return jsonify({"status":"OK"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
