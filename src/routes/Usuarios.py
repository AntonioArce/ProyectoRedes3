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
            cursor.execute("SELECT * from Usuarios")
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
                cursor.execute("INSERT INTO Usuarios(nombre_usuario,email,contrasena,is_admin,dispositivo) VALUES(%s,%s,%s,%s,%s)",
                (nombre,email,contrasena,isadmin,dispositivo))
                cursor.connection.commit()
            return jsonify({"msn":"Usuario comun creado con exito"})
        
        elif isadmin == 1:
            net_connect.send_config_set(["conf t"])
            out = net_connect.send_config_set(["username "+ nombre +" privilege 15 password "+ contrasena])
            print(out)
            net_connect.send_config_set(["write"])
            with conexion.cursor() as cursor:
                    cursor.execute("INSERT INTO Usuarios(nombre_usuario,email,contrasena,is_admin,dispositivo) VALUES(%s,%s,%s,%s,%s)",
                    (nombre,email,contrasena,isadmin,dispositivo))
                    cursor.connection.commit()
            return jsonify({"msn":"Usuario administrador creado con exito"})



"""Hice pruebas aqui de netmiko! jejejeje"""
@main.route('/prueba', methods = ['GET'])
def prueba():
    if request.method == 'GET':
        net_connect = ConnectHandler(**router)
        net_connect("conf t")
        out = net_connect.send_command("int fa 4/1")
        print(out)
        return jsonify({"mensaje":"bien"})