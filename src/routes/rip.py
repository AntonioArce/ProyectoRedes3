from flask import Blueprint, jsonify, request
from netmiko import ConnectHandler
main = Blueprint('rip_blueprint',__name__)

router = { 
    'host': '10.10.10.2',
    'username': 'root',
    'password': 'root',
    "device_type": "cisco_ios"
}



@main.route('/', methods=['POST'])
def rip():
    data = request.get_json()
    ip1 = data["ip1"]
    
    
    net_connect = ConnectHandler(**router)
    net_connect.send_config_set(['router rip', 'version 2',
    'no auto-summary', 'redistribute static', 
    'redistribute ospf 1 subnets',
    'redistribute eigrp 1 subnets', "network "+ ip1, "end"])
    net_connect.save_config(cmd = 'write')

    out = net_connect.send_command("show ip protocols")
    print(out)
    return jsonify({"ms": "Enrutamiento RIP Configurado con exito"})