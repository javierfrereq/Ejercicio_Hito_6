from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

class index(Resource):
    def get(self):
        return {'Hito6': 'Freddy'}

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


api.add_resource(index, '/')
api.add_resource(EstatoLista, '/status')
api.add_resource(Estado, '/status/<status_id>')

if __name__ == '__main__':
    app.run(debug=True)
