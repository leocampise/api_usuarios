"""Prueba de una api con conexion mysql y sincronizada con GitHub"""

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json

from config import config

app=Flask(__name__)
CORS(app)

conexion=MySQL(app)

trad = {'tradicional':{'1':11,'2':12,'3':13,'4':14,'5':15,'6':16}}

@app.route('/quini6', methods=['GET'])
# trae resultado de la ultima jugada
def quini6():
    try:
        sorteo=trad['tradicional']
        return jsonify(sorteo['1'])
        #return jsonify(sorteo)
        
    except Exception as ex:
        return jsonify({'mensaje':'Error '})

@app.route('/usuarios', methods=['GET'])
# trae todas las filas de la tabla 'obras'
def listar_obras():
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id_obras, nombre, zona FROM obras"
        cursor.execute(sql)
        datos=cursor.fetchall()
        usuarios=[]
        for fila in datos:
            usuario={'id':fila[0],'nombre':fila[1],'zona':fila[2]}
            usuarios.append(usuario)
        return jsonify({'usuarios':usuarios,'mensaje':'usuarios listados'})
        
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'})

# trae solo la fila especificada por el id_obras
@app.route('/usuarios/<id>', methods=['GET'])
def listar_obra(id):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT id_obras, nombre, zona FROM obras WHERE id_obras='{0}'".format(id) #format('variable')
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            usuario={'id':datos[0],'nombre':datos[1],'zona':datos[2]}
            return jsonify({'usuario':usuario,'mensaje':'usuario encontrado'})
        else:
            return jsonify({'mensaje':'usuario no encontrado'})
        
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'})


# regitrar nuevo usuario
@app.route('/usuarios', methods=['POST'])

def registrar_usuario():
    try:
        #print(request.json)
        cursor = conexion.connection.cursor()
        sql="INSERT INTO obras (id_obras,nombre,zona) VALUES('{0}','{1}','{2}')".format(request.json['id_obras'],request.json['nombre'],request.json['zona'])
        cursor.execute(sql)
        conexion.connection.commit() # confirma la accion de ingresar nuevo registro
        return 'Usuario registrado'
    
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'})


# borrar un registro
@app.route('/usuarios/<id>', methods=['DELETE'])

def borrar_usuario(id):
    try:
       cursor = conexion.connection.cursor()
       sql="DELETE FROM obras WHERE id_obras = '{0}'".format(id)
       cursor.execute(sql)
       conexion.connection.commit()
       return 'registro borrado'
   
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'})


# actualizar un registro mediante su id_obras
@app.route('/usuarios/<id>', methods=['PUT'])

def actualizar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        sql="UPDATE obras SET nombre='{0}', zona='{1}' WHERE id_obras='{2}'".format(request.json['nombre'],request.json['zona'],id)
        cursor.execute(sql)
        conexion.connection.commit() # confirma la accion de ingresar nuevo registro
        return 'Usuario actualizado'
    
    except Exception as ex:
        return jsonify({'mensaje':'Error de conexion'})
    
def pagina_no_encontrada(error):
    return '<h3>la pagina que buscas no existe...</h3>',404  #codigo de pagina no encontrada
    
    
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()