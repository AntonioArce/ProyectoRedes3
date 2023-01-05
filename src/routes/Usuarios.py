from app import app
import os
from flask import Blueprint, jsonify, request
from config import obtener_conexion
from netmiko import ConnectHandler

router = { 
    'host': '10.10.10.2',
    'username': 'root',
    'password': 'root',
    "device_type": "cisco_ios"
}


main = Blueprint('usuarios_blueprint',__name__)


@main.route('/', methods=['POST', 'GET'])
def get_usuarios():
    if request.method == 'GET':
        conexion = obtener_conexion()
        #us = []
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * from Usuarios where is_active = 1")
            us = cursor.fetchall()
        conexion.close()
        return jsonify(us)
    
    if request.method == 'POST':
        data = request.get_json()
        nombre = data['nombre_usuario'].lower()
        email = data['email'].lower()
        contrasena = data['contrasena'].lower()
        isadmin = data['isadmin']
        dispositivo = data['dispositivo']
        conexion = obtener_conexion()

        net_connect = ConnectHandler(**router)

        if isadmin == 0:
            net_connect.send_config_set(["conf t"])
            out = net_connect.send_config_set(["username "+ nombre +" privilege 1 password "+ contrasena])
            print(out)
            net_connect.send_config_set(["write"])
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO Usuarios(nombre_usuario,email,contrasena,is_admin,dispositivo,is_active) VALUES(%s,%s,%s,%s,%s,1)",
                (nombre,email,contrasena,isadmin,dispositivo))
                cursor.connection.commit()
            return jsonify({"msn":"Usuario comun creado con exito"})
        
        elif isadmin == 1:
            net_connect.send_config_set(["conf t"])
            out = net_connect.send_config_set(["username "+ nombre +" privilege 15 password "+ contrasena])
            print(out)
            net_connect.send_config_set(["write"])
            with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Usuarios(nombre_usuario,email,contrasena,is_admin,dispositivo,is_active) VALUES(%s,%s,%s,%s,%s,1)",
                    (nombre,email,contrasena,isadmin,dispositivo))
                    cursor.connection.commit()
            return jsonify({"msn":"Usuario administrador creado con exito"})

@main.route('/<int:id_u>', methods = ['DELETE'])
def delete_usuario(id_u):
    name = ''
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
            cursor.execute("SELECT nombre_usuario from Usuarios where id_usuario = "+ str(id_u))
            name = cursor.fetchall()

            nombre = ''.join(str(name))
            print(nombre)
            new_string = ''.join(char for char in nombre if char.isalnum())
            print(new_string)


            net_connect = ConnectHandler(**router)
            net_connect.send_config_set(['no username '+ new_string])
            net_connect.save_config(cmd = 'write')

            cursor.execute("update Usuarios SET is_active = 0 where id_usuario = "+ str(id_u))
            cursor.connection.commit()
            
            cursor.close()


    return jsonify({"msg": "Usuario "+ new_string +" eliminado con exito"})

