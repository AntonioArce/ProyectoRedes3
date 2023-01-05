from flask import Blueprint, jsonify, request
from netmiko import ConnectHandler
main = Blueprint('ospf_blueprint',__name__)

router = { 
    'host': '192.168.0.1',
    'username': 'root',
    'password': 'root',
    "device_type": "cisco_ios"
}

@main.route('/', methods = ["POST"])
def ospf():
    data = request.get_json()
    ip1 = data["ip1"]
    wild1 = data["wild1"]
    ip2 = data["ip2"]
    wild2 = data["wild2"]


    net_connect = ConnectHandler(**router)
    net_connect.send_config_set(['router ospf 1',
    'redistribute rip subnets', 'redistribute static subnets',
    'redistribute eigrp 1 subnets',
    "network "+ ip1 + " " + wild1 + " area 0",
    "network "+ ip2 + " " + wild2 + " area 0", "end"])
    net_connect.save_config(cmd = 'write')

    out = net_connect.send_command("show ip protocols")
    print(out)
    return jsonify({"ms": "Enrutamiento ospf Configurado con exito"})