import pexpect
import getpass
import logging
import time

class Router:
    def __init__(self, ip, name, user="root", password="root"):
        self.ip = ip
        self.name = name
        self.user = user
        self.password = password
    
    def buscarVecinos(self, routers = {}):
        print(routers.keys())
        print(self.name)
        print(self.ip)

        if self.name in routers.keys(): # Si ya fue obtenido, no lo volvemos a obtener
            print('si entra')
            return 1
        
        mensaje = "Conectando a " + self.name
        logging.debug(mensaje)

        """ Nos conectamos al router """
        child = pexpect.spawn('telnet '+ self.ip)
        child.expect('Username: ')
        child.sendline(self.user)
        child.expect('Password: ')
        child.sendline(self.password)
        print('Si pasa login')
        
        """Obtenemos la tabla de dispositivos conectados """
        child.expect(self.name+"#")
        child.sendline('show cdp ne | begin Device') # Obtenemos la tabla de dispositivos
        child.expect(self.name+"#")
        tabla_dispositivos = child.before.decode().split()
            
        print(tabla_dispositivos)
        conectados = [x for x in tabla_dispositivos if "enrutador" in x] # Agrega a la lista si tiene la palabra Enrutador
        interfaces = []
        [interfaces.append(x) for x in tabla_dispositivos if ("/" in x) and (x not in interfaces)] # Agrega a la lista si tiene / y no repetidos

        """ Registramos el router """  
        routers[self.name] = {"ip": self.ip, "user": self.user, "password": self.password, "conectados": [x.split(".")[0] for x in conectados], "interfaces": interfaces} # Guardamos la info del dispositivo
            

        """ Obtenemos la informacion de cada dispositivo conectado """
        for dispositivo in conectados:
            # Obtenemos la info del dispositivo
            child.sendline('sh cdp entry '+ dispositivo)
            child.expect(self.name+"#")
            info_dispositivo = child.before.decode().split()
                
                
            # Obtenemos la ip del dispositivo
            ip = None
            for linea in range(0, len(info_dispositivo)):
                if 'address:' == info_dispositivo[linea]:
                    ip = info_dispositivo[linea+1]
                
            # Examinamos los routers vecinos
            enrutador = Router(str(ip), dispositivo.split(".")[0], self.user, self.password)
            enrutador.buscarVecinos(routers)
        
        
    