from flask import Blueprint, jsonify, request
from netmiko import ConnectHandler
main = Blueprint('baja_blueprint',__name__)

router = { 
    'host': '10.10.10.2',
    'username': 'root',
    'password': 'root',
    "device_type": "cisco_ios"
}

@main.route('/rip-delete', methods=['GET'])
def baja_rip():
    net_connect = ConnectHandler(**router)
    net_connect.send_config_set(['no router rip', 'end'])
    net_connect.save_config(cmd = 'write')

    return jsonify({"msg": "Protocolo rip eliminado con exito"})

@main.route('/ospf-delete', methods = ['GET'])
def baja_ospf():
    net_connect = ConnectHandler(**router)
    net_connect.send_config_set(['no router ospf 1', 'end'])
    net_connect.save_config(cmd = 'write')

    return jsonify({"msg": "Protocolo OSPF eliminado con exito"})

@main.route('/eigrp-delete', methods = ['GET'])
def baja_eigrp():
    net_connect = ConnectHandler(**router)
    net_connect.send_config_set(['no router eigrp 1', 'end'])
    net_connect.save_config(cmd = 'write')

    return jsonify({"msg": "Protocolo EIGRP eliminado con exito"})