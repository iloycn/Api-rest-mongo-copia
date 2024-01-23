from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from bson.objectid import ObjectId
app = Flask(__name__)

app.config["MONGO_URI"] = 'mongodb+srv://prueba:palomeras@cluster0.6hotbn8.mongodb.net/gestionjugadores'
mongo = PyMongo(app)

#GET de todos los jugadores
@app.route('/jugadores', methods=['GET'])
def get_jugadores():
    jugadores = mongo.db.jugadores.find()
    response = json_util.dumps(jugadores)
    return Response(response, mimetype='application/json') 

#GET un jugador por id
@app.route('/jugadores/<id>', methods=['GET'])
def get_jugador(id):
    jugador = mongo.db.jugadores.find_one({'_id': ObjectId(id)})
    
    if jugador:
        jugador_json = json_util.dumps(jugador)
        return Response(jugador_json, mimetype='application/json')
    else:
        return not_found()

#CREAR jugadores
@app.route('/jugadores', methods=['POST'])
def create_jugador():
    request_data = request.get_json()
    if 'nombre' in request_data and 'fecha' in request_data and 'detalles' in request_data and 'altura' in request_data:
        nombre = request_data['nombre']
        fecha = request_data['fecha']
        detalles = request_data['detalles']
        altura = request_data['altura']
    else:
        return datos_incompletos()

    id = mongo.db.jugadores.insert_one({'nombre': nombre, 'fecha': fecha, 'detalles': detalles, 'altura': altura})
    
    response = {
        'id': str(id.inserted_id),
        'nombre': nombre,
        'fecha': fecha,
        'detalles': detalles,
        'altura': altura
    }
    return response

#BORRAR jugadores
@app.route('/jugadores/<id>', methods=['DELETE'])
def delete_jugador(id):
    jugador = mongo.db.jugadores.find_one({'_id': ObjectId(id)})

    if jugador: # Encontrado para ser eliminado
        mongo.db.jugadores.delete_one({'_id': ObjectId(id)})
        response = jsonify({'mensaje': 'Jugador ' + id + 'fue eliminado satisfactoriamente'})
        return response
    else:
        return not_found()
   
#ACTUALIZAR jugadores
@app.route('/jugadores/<id>', methods=['PUT'])
def update_jugador(id):
    request_data = request.get_json()
    # Comprobando que se ha cada uno de los datos
    
    if 'nombre' in request_data and 'fecha' in request_data and 'detalles' in request_data and 'altura' in request_data:
        nombre = request_data['nombre']
        fecha = request_data['fecha']
        detalles = request_data['detalles']
        altura = request_data['altura']
    else:
        return datos_incompletos()

    jugador = mongo.db.jugadores.find_one({'_id': ObjectId(id)})

    if jugador:
        mongo.db.jugadores.update_one({'_id': ObjectId(id)}, {'$set': {
            'nombre': nombre,
            'fecha': fecha,
            'detalles': detalles,
            'altura': altura
        }})
        response = jsonify({'mensaje': 'Jugador ' + id + ' fue actualizado satisfactoriamente'})
        return response
    else:
        return not_found()

#ERROR no encontrado
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'mensaje': 'Recurso no encontrado: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

#ERROR datos incompletos
@app.errorhandler(400)
def datos_incompletos(error=None):
    response = jsonify({
        'mensaje': 'Datos incompletos: nombre, fecha, detalles y/o altura',
        'status': 400
    })
    response.status_code = 400
    return response

if __name__ == "__main__":
    app.run(debug=True)