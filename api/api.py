from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
#from django.shortcuts import render_to_response
#import sys
from random import randint


#reload(sys)  
#sys.setdefaultencoding('utf8')

import MySQLdb
import json

app = Flask(__name__)
api = Api(app)

class Pregunta(Resource):
  def get(self):
    json = '[{';
    #1 consultar el numero de preguntas
    sql = ('select count(*) from pregunta;')
    db = MySQLdb.connect(user='root', db='db', passwd='123456', host='localhost')
    cursor = db.cursor()
    cursor.execute(sql)
    for row in cursor:
	count = row[0]

    #2 generar un numero aleatorio, para elegir una pregunta aleatoria.
    rand = randint(0, count)
    
    #3 extraer la pregunta y la respuesta correcta de la base de datos.
    sql2 = 'SELECT pregunta,respuesta FROM pregunta,Respuesta WHERE pregunta.id = pregunta_id AND pregunta_id = ' + str(rand) + ';'
    cursor = db.cursor()
    cursor.execute(sql2)
    for row in cursor:
        json2 = '\"pregunta\":\"' + row[0] + '\",'
        json2 = json2 + '\"respuesta\":\"' + row[1] + '\",'
    
    json = json + json2
    
    #4 extraer 3 respuestas incorrectas
    sql3 = 'SELECT respuesta FROM pregunta,Respuesta WHERE pregunta.id != pregunta_id AND pregunta_id !=' + str(rand) + ' ORDER BY rand() LIMIT 3;'
    cursor = db.cursor()
    cursor.execute(sql3)
    row in cursor.fetchall()
    #respuestas_incorrecta = [row[0] for row in cursor.fetchall()]
    i=1;
    for row in cursor:
        json = json + '\"incorrecta'+str(i)+'\":\"' + str(row[0]) + '\",'
        i = i + 1
    
    json = json + '}]';

    db.close()

    return json


STATUS = {
    'status1': {'status': 'ok'},
    'status2': {'proyecto': 'hacer el Hito6'},
    'status3': {'proyecto': 'esperar que este bien '},
    'status4': {'proyecto': 'recibir el 10 en CC!'},
}


def abort_if_status_doesnt_exist(status_id):
    if status_id not in STATUS:
        abort(404, message="Estado {} No existe".format(status_id))

parser = reqparse.RequestParser()
parser.add_argument('proyecto')



class Estado(Resource):
    def get(self, status_id):
        abort_if_status_doesnt_exist(status_id)
        return STATUS[status_id]

    def delete(self, status_id):
        abort_if_status_doesnt_exist(status_id)
        del STATUS[status_id]
        return '', 204

    def put(self, status_id):
        args = parser.parse_args()
        proyecto = {'proyecto': args['proyecto']}
        STATUS[status_id] = proyecto
        return proyecto, 201

class EstatoLista(Resource):
    def get(self):
        return STATUS

    def post(self):
        args = parser.parse_args()
        status_id = int(max(STATUS.keys()).lstrip('status')) + 1
        status_id = 'status%i' % status_id
        STATUS[status_id] = {'proyecto': args['proyecto']}
        return STATUS[status_id], 201


api.add_resource(Pregunta, '/')
api.add_resource(EstatoLista, '/status')
api.add_resource(Estado, '/status/<status_id>')

if __name__ == '__main__':
    app.run(debug=True)
